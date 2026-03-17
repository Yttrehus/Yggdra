#!/usr/bin/env python3
"""
Yggdra Memory Architecture v1
To collections: knowledge (hvad vi ved) + episodes (hvad der skete).
Hybrid search (dense + sparse), temporal decay, content hashing.

Brug:
    python scripts/memory.py setup                    # Opret collections fra scratch
    python scripts/memory.py ingest <fil/mappe>       # Ingest markdown-filer
    python scripts/memory.py search "query"            # Søg med hybrid search + decay
    python scripts/memory.py status                    # Vis collection-stats
    python scripts/memory.py nuke                      # Slet knowledge + episodes (IKKE routes)
"""

import os
import sys
import json
import hashlib
import argparse
import uuid
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, SparseVectorParams, SparseIndexParams,
    PointStruct, SparseVector, NamedVector, NamedSparseVector,
    Prefetch, FusionQuery, Fusion, SearchParams,
    models,
)
from openai import OpenAI

# --- Config ---

QDRANT_URL = "http://localhost:6333"
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "REDACTED")
EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536
CHUNK_SIZE = 800  # tokens (ca. 3200 chars)
CHUNK_OVERLAP = 100  # tokens overlap

COLLECTIONS = {
    "knowledge": "Alt vi ved: research, docs, etableret viden, projektbeskrivelser",
    "episodes": "Alt der skete: sessions, voice memos, beslutninger, handlinger",
}

# --- Data model ---

@dataclass
class Doc:
    id: str              # source_prefix + hash
    source: str          # "markdown", "voice_memo", "session"
    source_file: str     # original filsti
    text: str            # chunk-tekst
    title: str           # fil-titel eller heading
    chunk_index: int     # chunk nr i filen
    created_at: str      # ISO datetime
    indexed_at: str      # ISO datetime
    content_hash: str    # SHA256 af text
    confidence: str      # "established", "research", "draft", "unknown"
    references: list     # kilder hvis tilgængelige


# --- Sparse vector (BM25-approksimation) ---

def text_to_sparse(text: str) -> dict:
    """Simpel term-frequency sparse vector til BM25-approksimation."""
    words = text.lower().split()
    # Fjern korte ord og stop words
    stop = {"og", "i", "er", "en", "et", "den", "det", "de", "at", "på", "til",
            "med", "for", "af", "som", "kan", "har", "fra", "the", "a", "an",
            "is", "in", "to", "of", "and", "that", "it", "be", "was", "are"}
    words = [w for w in words if len(w) > 2 and w not in stop]

    # Term frequency
    tf = {}
    for w in words:
        h = hash(w) % 50000  # Hash til fast indeks-rum
        tf[h] = tf.get(h, 0) + 1

    if not tf:
        return {"indices": [0], "values": [0.1]}

    # Normaliser
    max_tf = max(tf.values())
    return {
        "indices": list(tf.keys()),
        "values": [v / max_tf for v in tf.values()],
    }


# --- Chunking ---

def chunk_markdown(text: str, source_file: str, max_chars: int = 2400, overlap_chars: int = 400) -> list[dict]:
    """Chunk markdown med heading-awareness. Respekterer ## og ### grænser.
    For tekst uden newlines (f.eks. Whisper-output): splitter på sætninger."""
    # Hvis teksten har meget få newlines, split på sætninger først
    if text.count("\n") < len(text) / 2000:
        import re
        # Split på sætningsgrænser (. ! ? efterfulgt af mellemrum)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        lines = []
        current = ""
        for s in sentences:
            if len(current) + len(s) > 200:
                if current:
                    lines.append(current)
                current = s
            else:
                current = f"{current} {s}".strip() if current else s
        if current:
            lines.append(current)
    else:
        lines = text.split("\n")
    chunks = []
    current_chunk = []
    current_heading = ""
    current_len = 0

    # Find titel (første # heading)
    title = Path(source_file).stem
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            title = line.lstrip("# ").strip()
            break

    for line in lines:
        # Ny heading = potentielt ny chunk
        if line.startswith("## ") or line.startswith("### "):
            if current_len > 200:  # Gem nuværende chunk hvis den har substans
                chunks.append({
                    "text": "\n".join(current_chunk),
                    "heading": current_heading,
                    "title": title,
                })
                # Overlap: behold sidste par linjer
                overlap_lines = current_chunk[-3:] if len(current_chunk) > 3 else []
                current_chunk = overlap_lines
                current_len = sum(len(l) for l in current_chunk)
            current_heading = line.lstrip("#").strip()

        current_chunk.append(line)
        current_len += len(line)

        # Hard split ved max_chars
        if current_len >= max_chars:
            chunks.append({
                "text": "\n".join(current_chunk),
                "heading": current_heading,
                "title": title,
            })
            overlap_lines = current_chunk[-3:] if len(current_chunk) > 3 else []
            current_chunk = overlap_lines
            current_len = sum(len(l) for l in current_chunk)

    # Sidste chunk
    if current_len > 50:
        chunks.append({
            "text": "\n".join(current_chunk),
            "heading": current_heading,
            "title": title,
        })

    return chunks


def detect_confidence(text: str, filepath: str) -> str:
    """Heuristisk confidence-detection baseret på indhold."""
    lower = text.lower()
    fp = filepath.lower()

    if "destillat" in fp or "deep_study" in fp:
        return "research"
    if "red_team" in fp or "evaluering" in fp:
        return "research"
    if any(w in lower for w in ["[solid]", "peer-reviewed", "replikeret"]):
        return "established"
    if any(w in lower for w in ["[vendor", "[anekdotisk", "draft", "udkast"]):
        return "draft"
    if any(w in lower for w in ["kilde:", "source:", "ref:", "reference"]):
        return "research"
    return "unknown"


def detect_collection(filepath: str) -> str:
    """Bestem collection baseret på filsti."""
    fp = filepath.lower()
    if any(w in fp for w in ["voice_memo", "session", "chatlog", "episode", "progress"]):
        return "episodes"
    return "knowledge"


# --- Core operations ---

def setup_collections(client: QdrantClient):
    """Opret knowledge og episodes med hybrid vector config."""
    for name, desc in COLLECTIONS.items():
        # Slet hvis den eksisterer
        try:
            client.delete_collection(name)
            print(f"  Slettet gammel '{name}'")
        except Exception:
            pass

        client.create_collection(
            collection_name=name,
            vectors_config={
                "dense": VectorParams(
                    size=EMBED_DIM,
                    distance=Distance.COSINE,
                ),
            },
            sparse_vectors_config={
                "sparse": SparseVectorParams(
                    index=SparseIndexParams(on_disk=False),
                ),
            },
        )
        print(f"  Oprettet '{name}': {desc}")

    print("\nCollections klar. Hybrid search (dense + sparse) aktiveret.")


def embed_texts(openai_client: OpenAI, texts: list[str]) -> list[list[float]]:
    """Batch-embed tekster via OpenAI. Truncate til max 8000 tokens (~32000 chars)."""
    # Truncate lange tekster (8192 token limit, ~4 chars/token)
    truncated = [t[:6000] for t in texts]
    # Batch i grupper af 20 for at undgå rate limits
    all_embeddings = []
    for i in range(0, len(truncated), 20):
        batch = truncated[i:i+20]
        response = openai_client.embeddings.create(
            model=EMBED_MODEL,
            input=batch,
        )
        all_embeddings.extend([d.embedding for d in response.data])
    return all_embeddings


def ingest_file(filepath: str, client: QdrantClient, openai_client: OpenAI, force: bool = False) -> int:
    """Ingest én markdown-fil. Returnerer antal points upserted."""
    path = Path(filepath)
    if not path.exists():
        print(f"  SKIP: {filepath} eksisterer ikke")
        return 0
    if path.suffix.lower() not in {".md", ".txt"}:
        print(f"  SKIP: {filepath} er ikke markdown/txt")
        return 0

    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text.strip()) < 100:
        print(f"  SKIP: {filepath} for kort ({len(text)} chars)")
        return 0

    collection = detect_collection(filepath)
    confidence = detect_confidence(text, filepath)
    chunks = chunk_markdown(text, filepath)

    if not chunks:
        return 0

    # Embed alle chunks
    chunk_texts = [c["text"] for c in chunks]

    # Kontekstuel prefix: titel + heading for bedre embeddings
    enriched_texts = []
    for c in chunks:
        prefix = f"Dokument: {c['title']}"
        if c["heading"]:
            prefix += f" — {c['heading']}"
        enriched_texts.append(f"{prefix}\n\n{c['text']}")

    embeddings = embed_texts(openai_client, enriched_texts)

    # Byg points
    points = []
    now = datetime.now(timezone.utc).isoformat()
    file_mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        content_hash = hashlib.sha256(chunk["text"].encode()).hexdigest()[:16]
        doc_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"yggdra:{filepath}:{i}"))

        # Check om uændret (skip)
        if not force:
            try:
                existing = client.retrieve(collection, [doc_id])
                if existing and existing[0].payload.get("content_hash") == content_hash:
                    continue  # Uændret, skip
            except Exception:
                pass

        sparse = text_to_sparse(chunk["text"])

        point = PointStruct(
            id=doc_id,
            vector={
                "dense": embedding,
            },
            payload={
                "source": "markdown",
                "source_file": str(path.name),
                "source_path": str(path),
                "title": chunk["title"],
                "heading": chunk["heading"],
                "text": chunk["text"],
                "chunk_index": i,
                "total_chunks": len(chunks),
                "created_at": file_mtime,
                "indexed_at": now,
                "content_hash": content_hash,
                "confidence": confidence,
                "collection": collection,
            },
        )
        points.append((point, sparse))

    if not points:
        print(f"  SKIP: {path.name} — alle chunks uændrede")
        return 0

    # Upsert med dense + sparse i én operation
    client.upsert(
        collection_name=collection,
        points=[
            PointStruct(
                id=p.id,
                vector={
                    "dense": p.vector["dense"],
                    "sparse": SparseVector(
                        indices=sparse["indices"],
                        values=sparse["values"],
                    ),
                },
                payload=p.payload,
            )
            for p, sparse in points
        ],
    )

    print(f"  {path.name} -> {collection}: {len(points)} chunks ({confidence})")
    return len(points)


def ingest_path(target: str, client: QdrantClient, openai_client: OpenAI, force: bool = False) -> int:
    """Ingest fil eller mappe (rekursivt for .md filer)."""
    path = Path(target)
    total = 0

    if path.is_file():
        total = ingest_file(str(path), client, openai_client, force)
    elif path.is_dir():
        md_files = sorted(path.rglob("*.md"))
        print(f"Fundet {len(md_files)} markdown-filer i {path}")
        for f in md_files:
            # Skip node_modules, .git, archive
            if any(skip in str(f) for skip in [".git", "node_modules", "9_archive", "__pycache__"]):
                continue
            total += ingest_file(str(f), client, openai_client, force)
    else:
        print(f"FEJL: {target} er hverken fil eller mappe")

    return total


def search(query: str, client: QdrantClient, openai_client: OpenAI,
           collection: str = None, limit: int = 10, decay_rate: float = 0.005) -> list:
    """Hybrid search med temporal decay."""
    # Embed query
    query_embedding = embed_texts(openai_client, [query])[0]
    query_sparse = text_to_sparse(query)

    collections = [collection] if collection else ["knowledge", "episodes"]
    all_results = []

    for col in collections:
        try:
            # Hybrid search med RRF
            results = client.query_points(
                collection_name=col,
                prefetch=[
                    Prefetch(
                        query=query_embedding,
                        using="dense",
                        limit=30,
                    ),
                    Prefetch(
                        query=SparseVector(
                            indices=query_sparse["indices"],
                            values=query_sparse["values"],
                        ),
                        using="sparse",
                        limit=30,
                    ),
                ],
                query=FusionQuery(fusion=Fusion.RRF),
                limit=limit,
            )

            for point in results.points:
                # Temporal decay
                created = point.payload.get("created_at", "")
                try:
                    created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    age_days = (datetime.now(timezone.utc) - created_dt).days
                    decay = 1 / (1 + age_days * decay_rate)
                except Exception:
                    decay = 0.5

                all_results.append({
                    "score": point.score * decay if point.score else decay,
                    "collection": col,
                    "title": point.payload.get("title", ""),
                    "heading": point.payload.get("heading", ""),
                    "source_file": point.payload.get("source_file", ""),
                    "confidence": point.payload.get("confidence", ""),
                    "created_at": created,
                    "text": point.payload.get("text", "")[:500],
                    "id": point.id,
                })
        except Exception as e:
            print(f"  Søgefejl i {col}: {e}")

    # Sortér efter decayed score
    all_results.sort(key=lambda r: r["score"], reverse=True)
    return all_results[:limit]


def status(client: QdrantClient):
    """Vis status for alle collections."""
    print("Qdrant Collections:\n")
    for col in client.get_collections().collections:
        info = client.get_collection(col.name)
        vectors = "hybrid" if hasattr(info.config.params, 'sparse_vectors') and info.config.params.sparse_vectors else "dense-only"
        print(f"  {col.name}: {info.points_count} points ({vectors})")


def nuke(client: QdrantClient):
    """Slet knowledge + episodes. Rør IKKE routes eller andre."""
    for name in COLLECTIONS:
        try:
            client.delete_collection(name)
            print(f"  Slettet: {name}")
        except Exception:
            print(f"  {name} eksisterede ikke")


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="Yggdra Memory Architecture v1")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("setup", help="Opret collections fra scratch")
    sub.add_parser("status", help="Vis collection-stats")
    sub.add_parser("nuke", help="Slet knowledge + episodes")

    p_ingest = sub.add_parser("ingest", help="Ingest markdown-filer")
    p_ingest.add_argument("path", help="Fil eller mappe")
    p_ingest.add_argument("--force", action="store_true", help="Re-ingest uændrede filer")

    p_search = sub.add_parser("search", help="Hybrid search med decay")
    p_search.add_argument("query", help="Søgestreng")
    p_search.add_argument("--collection", "-c", help="Søg kun i denne collection")
    p_search.add_argument("--limit", "-n", type=int, default=5, help="Max resultater")
    p_search.add_argument("--decay", type=float, default=0.005, help="Temporal decay rate")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    client = QdrantClient(url=QDRANT_URL, timeout=120)
    openai_client = OpenAI(api_key=OPENAI_KEY)

    if args.command == "setup":
        print("Opretter collections...\n")
        setup_collections(client)

    elif args.command == "status":
        status(client)

    elif args.command == "nuke":
        confirm = input("Slet knowledge + episodes? (ja/nej): ")
        if confirm.lower() == "ja":
            nuke(client)
        else:
            print("Afbrudt.")

    elif args.command == "ingest":
        print(f"Ingesting: {args.path}\n")
        total = ingest_path(args.path, client, openai_client, args.force)
        print(f"\nFærdig: {total} chunks indexed")

    elif args.command == "search":
        results = search(args.query, client, openai_client,
                        collection=args.collection, limit=args.limit,
                        decay_rate=args.decay)
        if not results:
            print("Ingen resultater.")
            return

        for i, r in enumerate(results, 1):
            # Sanitize for Windows console (cp1252)
            def safe(s):
                return str(s).encode("ascii", errors="replace").decode("ascii")
            print(f"\n{'='*60}")
            print(f"[{i}] {safe(r['title'])}")
            if r['heading']:
                print(f"    {safe(r['heading'])}")
            print(f"    {safe(r['source_file'])} | {r['collection']} | {r['confidence']}")
            print(f"    Score: {r['score']:.4f} | {r['created_at'][:10]}")
            print(f"    {safe(r['text'][:300])}...")


if __name__ == "__main__":
    main()
