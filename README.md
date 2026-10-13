# DataWitness Africa

> Rendre les chiffres publics **vérifiables, comparables et explicables**.

Assistant de vérification des données publiques : il extrait les affirmations quantitatives de rapports, annuaires et tableaux (PDF, XLSX, CSV), rapproche les indicateurs qui désignent la même réalité, détecte les écarts, distingue **contradiction réelle / différence de périmètre / comparaison invalide**, et remonte jusqu'à la page source.

Hackathon *L'Aube de l'Intelligence Artificielle — Édition 2* · 14 novembre 2026 · HESTIM, Casablanca
Équipe UCAO-UUT / COTIA : DJERADE GOLBE Parfait · KOMOSSI Sosso · YENDONGOU Damtoti

## Documentation

| Document | Contenu |
|---|---|
| [docs/DOCUMENT_TECHNIQUE.md](docs/DOCUMENT_TECHNIQUE.md) | Exigences, architecture, pipeline, modèle de données, logique de vérification, séquences, états, API, UI, déploiement — 20 diagrammes |
| [docs/PLANIFICATION.md](docs/PLANIFICATION.md) | Gantt, phases, couches, responsables, jalons, MVP, risques |
| [docs/sources/](docs/sources/) | Dossier de candidature et dossier de concept d'origine |

## Démarrage

Prérequis : Docker, [uv](https://docs.astral.sh/uv/), Node 20.

```bash
cp .env.example .env
make up                      # tout en Docker : http://localhost:5173 · API http://localhost:8000/docs
```

En développement :

```bash
make db                      # PostgreSQL + pgvector
make install-back migrate back
make install-front front
make test lint
```

Extras Python : `uv sync --extra extraction --extra ai` pour les dépendances PDF/OCR et IA.

## Structure

```
backend/   API FastAPI + pipeline (ingestion → extraction → normalization → matching → detection → explanation → evidence)
frontend/  Interface React (sources, divergences, fiche de preuve, graphe)
data/      corpus, données intermédiaires, référentiels (indicateurs, zones, unités)
notebooks/ exploration et évaluation
infra/     initialisation PostgreSQL
docs/      documentation technique et planification
```
