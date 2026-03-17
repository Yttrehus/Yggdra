# Solo Dev Research: Google Maps, Cloud, AI + Logistik
*15. marts 2026*

---

## 1. Google Maps Platform — hvad kan én person bygge?

**Route Optimization API** — Google har en dedikeret VRP-solver (Vehicle Routing Problem). Den tager køretøjer, stops, tidsvinduer og kapacitet som input og returnerer optimerede ruter. Der findes en klar reference-app: [js-route-optimization-app](https://github.com/googlemaps/js-route-optimization-app).

**Routes API** (erstatter Distance Matrix) — beregner afstande/tid mellem N origins og M destinations. Perfekt til at bygge en matrice over alle stops på en rute og finde den optimale rækkefølge. 10.000 gratis requests/måned (Essentials).

**Geocoding** — oversæt adresser til GPS-koordinater og omvendt. $5 per 1.000 requests, men $200 gratis kredit/måned dækker ~40.000 requests.

**Heatmaps** — Google Maps JS API har built-in heatmap layer. Kombineret med dine GPS-data kan du visualisere: hvor bruger I mest tid, hvilke områder har flest stop, trafikflaskehalse.

**Geofencing** — definer virtuelle zoner (f.eks. "deponi", "genbrugsstation") og trigger events når køretøjet krydser grænsen. Relevant for automatisk tidsregistrering.

**Konkrete projekt-idéer:**
- Heatmap over alle stops farvekodet efter tidsforbrrug per stop
- Distance matrix: "hvad koster det at omsortere ruten?"
- Geofence-baseret automatisk "ankommet depot" / "forladt depot"
- Sammenlign planlagt vs. faktisk rute (GPS-tracking overlay)

**Priser med $300 kredit:** Routes API Essentials = $5/1000 elem. $300 = 60.000 route matrix-elementer. Rigeligt til eksperimenter.

Sources: [Route Optimization API](https://developers.google.com/maps/documentation/route-optimization), [Pricing](https://developers.google.com/maps/billing-and-pricing/pricing), [Routes API](https://developers.google.com/maps/documentation/routes/usage-and-billing)

---

## 2. Google Cloud Console — hvad er reelt brugbart?

**Cloud Run** — serverless containers. Deploy en Python API (Flask/FastAPI) der besvarer forespørgsler. 2 mio. invocations/måned GRATIS (ud over $300 kredit). Perfekt til en rute-API eller et dashboard-backend.

**BigQuery** — 1 TB queries + 10 GB storage gratis/måned. Smid historisk rutedata, GPS-logs, tidsregistrering ind. Kør SQL-analyser: "gennemsnitlig tid per stop", "hvilken dag er langsomst", "sæsonvariation".

**Vertex AI + Gemini** — din $300 kredit kan brændes på Gemini API til embedding, billedgenerering, multimodal analyse. Opgrader til betalt for højere kvoter — kredit bruges først.

**Cloud Functions** — lightweight serverless. Triggeres af HTTP, Pub/Sub, Cloud Scheduler. God til: "kør hver morgen kl. 06:00, hent dagens rute, optimer, send til telefon."

**Realistisk $300-budget:**
- Cloud Run API backend: ~$5-10/måned
- BigQuery analytics: gratis (under 1 TB)
- Gemini API eksperimenter: $50-100
- Maps API: $50-100
- **Holdbarhed: 3-6 måneder med moderat brug**

Sources: [Free Tier](https://cloud.google.com/free), [2026 Developer Guide](https://dev.to/behruamm/the-2026-developers-guide-to-free-google-cloud-credits-for-ai-side-projects-1ac5)

---

## 3. Navigation APIs — kan du bygge custom turn-by-turn?

**Ja.** Tre realistiske muligheder:

**GraphHopper** (open source, Java) — routing engine ovenpå OpenStreetMap. Turn-by-turn instrukser på 45+ sprog. Truck-profiler built-in. Self-hostable. Har også Route Optimization (baseret på jsprit). GitHub: [graphhopper/graphhopper](https://github.com/graphhopper/graphhopper)

**OpenRouteService** (open source) — bygget på OSM, understøtter truck-profiler med køretøjsdimensioner og vejrestriktioner. Bruger VROOM til VRP-solving. Gratis hosted API med begrænsede kvoter.

**VROOM + OSRM i Docker** — den mest realistiske self-hosted stack:
```
OSRM (routing engine) + VROOM (VRP solver) + din webapp
```
Docker-setup på 2 minutter: [vroom-docker](https://github.com/VROOM-Project/vroom-docker). Løser VRP i millisekunder. Bruges i produktion af kommuner til affaldsindsamling.

**Google Navigation SDK** — kun til Android/iOS, kræver enterprise-aftale. Ikke relevant for solo dev.

**Konklusion:** GraphHopper eller VROOM+OSRM i Docker er den realistiske vej. Kører på din VPS.

Sources: [GraphHopper](https://www.graphhopper.com/), [VROOM Docker](https://github.com/VROOM-Project/vroom-docker), [OpenRouteService](https://openrouteservice.org/), [VROOM+OSRM Guide](https://medium.com/@fbaierl1/setting-up-vroom-osrm-with-docker-compose-c8dc48d0cb2a)

---

## 4. LLM + Geospatial — "vis mig alle stops hvor vi brugte >10 min"

**Akademisk front:** Forskningsfeltet eksploderer. GeoGPT (2024) oversætter naturligt sprog til GIS-operationer. LLM-Geo (GitHub: [gladcolor/LLM-Geo](https://github.com/gladcolor/LLM-Geo)) genererer Python-kode til spatial analyse fra naturligt sprog. Fine-tunet GPT-4o-mini opnår 89.7% accuracy på spatial queries.

**Praktisk tilgang for dig:**
1. Dine route-data ligger i Qdrant + JSON
2. Claude kan generere Python/SQL der filtrerer, aggregerer, plotter
3. Resultat vises på Mapbox/Leaflet kort i din webapp

**Konkret flow:**
```
Bruger: "Vis alle stops på rute 256 hvor vi holder mere end 8 minutter"
→ Claude parser → Python filtrerer GPS-data → GeoJSON output
→ Leaflet/Mapbox heatmap i browseren
```

**Eksisterende eksempel:** [Walker Data AI Location Explorer](https://walker-data.com/posts/ai-location-explorer/) — Shiny + Claude API til interaktiv lokationsanalyse. Én person byggede det.

**Mapbox GL JS** — gratis tier, heatmaps, custom markers, 3D terrain, 60fps. Perfekt til at visualisere rutedata. [Heatmap tutorial](https://docs.mapbox.com/help/tutorials/make-a-heatmap-with-mapbox-gl-js/)

Sources: [GeoGPT](https://www.sciencedirect.com/science/article/pii/S1569843224003303), [LLM-Geo](https://github.com/gladcolor/LLM-Geo), [GeoBenchX](https://arxiv.org/html/2503.18129v2)

---

## 5. "Holy shit, én person byggede det?" — solo dev projekter

**AI Coding Agent Dashboard** — Marc Nuri byggede et dashboard der orkestrerer 5-10 Claude Code sessions på tværs af maskiner. Én person, ét dashboard, fuld kontrol. [Blog](https://blog.marcnuri.com/ai-coding-agent-dashboard)

**Cuneiform Chat** — Bikash byggede en enterprise AI chatbot-platform solo på 4 måneder: 6 microservices, 7 kanaler (Telegram, WhatsApp, Discord, Slack, web). Claude Code som co-developer. [Indie Hackers](https://www.indiehackers.com/post/i-built-an-enterprise-ai-chatbot-platform-solo-6-microservices-7-channels-and-claude-code-as-my-co-developer-5bafd24c20)

**Solo SaaS >$500K/år** — anonym HN-bruger kører en B2B-platform med API der driver kendte virksomheder. Helt alene. [HN](https://news.ycombinator.com/item?id=42561176)

**OpenClaw** — Peter Steinberger. 0 → 210.000 GitHub stars. Workflow automation, personlig produktivitet, browser automation. Principperne (heartbeat, hybrid search, temporal decay) er allerede i din MEMORY.md.

**Dify** — open source agentic AI workflow platform med visual builder, RAG pipelines, 100+ LLM providers. [GitHub](https://github.com/langgenius/dify)

**Relevant for dig:** Du har allerede Qdrant + Claude Code + Docker + cron + webapp. Du er tættere på disse projekter end de fleste.

Sources: [Marc Nuri Dashboard](https://blog.marcnuri.com/ai-coding-agent-dashboard), [Claude Code Personal AI](https://www.theneuron.ai/explainer-articles/how-to-turn-claude-code-into-your-personal-ai-assistant/), [Top AI GitHub 2026](https://dev.to/nocobase/top-20-ai-projects-on-github-to-watch-in-2026-not-just-openclaw-4878)

---

## 6. Affaldsindsamling & logistik — kan du slå kommerciel software?

**VROOM** — open source, C++20, løser VRP i millisekunder. Docker-ready. Brugt af brasilianske kommuner til affaldsrute-optimering i peer-reviewed studie (ScienceDirect 2026). GitHub: [VROOM-Project/vroom](https://github.com/VROOM-Project/vroom) — 1.2K stars.

**Google OR-Tools** — Googles gratis optimeringssuite. Python API. Løser CVRP (Capacitated VRP) med tidsvinduer, kapacitetsbegrænsninger, multiple køretøjer. Officiel tutorial: [VRP docs](https://developers.google.com/optimization/routing/vrp). Perfekt til "givet 80 stops og 1 lastbil, hvad er den korteste rute?"

**VeRyPy** — Python-bibliotek med 15 klassiske VRP-heuristikker. Akademisk kvalitet. [GitHub](https://github.com/yorak/VeRyPy)

**Kommercielle konkurrenter:**
- OptimoRoute: $35-50/køretøj/måned. Supports affaldsindsamling specifikt.
- NextBillion.ai: 50+ constraints, turn-by-turn, men enterprise pricing.
- SmartRoutes: fokuseret på solid waste collection.

**Kan du slå dem?** Ikke på features — men på *fit*. Kommerciel software er generisk. Du kender rute 256, du har GPS-historik, du ved hvor lang tid hvert stop tager. En custom løsning med OR-Tools/VROOM + dine data kan give bedre resultater for din specifikke rute end en generisk solver.

**Realistisk build:**
```
1. VROOM i Docker på VPS (2 min setup)
2. Feed dine stops fra TransportIntra API (getRute)
3. Sammenlign VROOM-output med faktisk rækkefølge
4. Vis besparelse i km/tid på Mapbox kort
```

Sources: [VROOM](https://github.com/VROOM-Project/vroom), [OR-Tools VRP](https://developers.google.com/optimization/routing/vrp), [CVRP Medium](https://medium.com/@nag96.chidara/capacitated-vehicle-routing-problem-cvrp-optimization-using-google-or-tools-and-python-7848fb5ffd16), [Waste Collection Study](https://www.sciencedirect.com/science/article/pii/S2950024926000028)

---

## Anbefalet prioritering for dig

| # | Projekt | Indsats | Wow-faktor |
|---|---------|---------|------------|
| 1 | VROOM i Docker → sammenlign med faktisk rute | 2 timer | Høj |
| 2 | Mapbox heatmap over GPS-stop data | 3 timer | Høj |
| 3 | "Spørg din rute" — Claude + rutedata → kort | 1 dag | Meget høj |
| 4 | Cloud Run API med rute-analytics | ½ dag | Medium |
| 5 | OR-Tools custom optimizer med historisk data | 2-3 dage | Meget høj |
| 6 | Geofence auto-tidsstempel | 1 dag | Praktisk |
