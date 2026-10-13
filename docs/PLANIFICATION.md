# DataWitness Africa — Planification

**Période** : 13 octobre → 14 novembre 2026 (≈ 4,5 semaines) · **Échéance** : démonstration au hackathon, HESTIM Casablanca, **14/11/2026**.

| Rôle | Membre | Couches principales |
|---|---|---|
| **Data & Qualité** | DJERADE GOLBE Parfait | Corpus · Référentiels · Ingestion · Extraction · Normalisation |
| **IA & Analyse** | KOMOSSI Sosso | Rapprochement · Détection · Confiance · Explication |
| **Technique & Chef de projet** | YENDONGOU Damtoti | Architecture · Base · API · Interface · Intégration · Démo |

---

## 1. Vue d'ensemble

```mermaid
gantt
    title DataWitness Africa — du 13 octobre au 14 novembre 2026
    dateFormat YYYY-MM-DD
    axisFormat %d/%m

    section P0 Cadrage
    Setup projet, doc technique           :done,    p0a, 2026-10-13, 2d
    Choix indicateurs + corpus            :active,  p0b, 2026-10-14, 3d
    Jalon J0 - socle prêt                 :milestone, m0, 2026-10-16, 0d

    section P1 Données
    Collecte corpus INSEED / ministères   :p1a, 2026-10-15, 4d
    Référentiels indicateurs, zones, unités:p1b, 2026-10-17, 4d
    Annotation jeu de vérité (50 valeurs) :p1c, 2026-10-20, 4d

    section P2 Ingestion & Extraction
    Ingestion + stockage + SHA-256        :p2a, 2026-10-17, 2d
    Extraction PDF texte + tableaux       :p2b, 2026-10-19, 5d
    Extraction XLSX / CSV                 :p2c, 2026-10-21, 2d
    OCR pages scannées                    :p2d, 2026-10-23, 3d
    Jalon J1 - claims extraits en base    :milestone, m1, 2026-10-26, 0d

    section P3 Normalisation
    Périodes, unités, zones               :p3a, 2026-10-24, 4d
    Mapping indicateurs canoniques        :p3b, 2026-10-26, 3d

    section P4 Intelligence
    Embeddings + recherche pgvector       :p4a, 2026-10-24, 4d
    Règles de comparabilité               :p4b, 2026-10-27, 3d
    Détection + verdict                   :p4c, 2026-10-29, 3d
    Score de confiance expliqué           :p4d, 2026-10-31, 3d
    Explication LLM encadrée              :p4e, 2026-11-02, 4d
    Jalon J2 - 3 cas détectés             :milestone, m2, 2026-11-04, 0d

    section P5 API & Interface
    Base + migrations + repositories      :p5a, 2026-10-17, 4d
    Endpoints sources / claims            :p5b, 2026-10-21, 4d
    Endpoints comparisons / evidence      :p5c, 2026-10-30, 4d
    UI Sources + Divergences              :p5d, 2026-10-26, 6d
    UI Fiche de preuve + page source      :p5e, 2026-11-01, 5d
    UI Graphe de provenance               :p5f, 2026-11-04, 3d

    section P6 Intégration
    Intégration bout en bout              :p6a, 2026-11-05, 3d
    Tests + évaluation + calibrage        :p6b, 2026-11-06, 3d
    Gel fonctionnel                       :milestone, m3, 2026-11-09, 0d

    section P7 Démo
    Scénario, dump base, plan B           :p7a, 2026-11-09, 3d
    Pitch + répétitions                   :p7b, 2026-11-10, 4d
    Hackathon HESTIM                      :crit, milestone, m4, 2026-11-14, 0d
```

---

## 2. Organisation par couches

Le projet est découpé en **6 couches** qui avancent en parallèle, synchronisées par 4 jalons.

```mermaid
flowchart TB
    C1["<b>Couche 1 — Données</b><br/>corpus, référentiels, vérité terrain<br/><i>Parfait</i>"]
    C2["<b>Couche 2 — Ingestion & Extraction</b><br/>PDF, tableaux, OCR, Excel<br/><i>Parfait</i>"]
    C3["<b>Couche 3 — Normalisation</b><br/>périodes, unités, zones, indicateurs<br/><i>Parfait + Sosso</i>"]
    C4["<b>Couche 4 — Intelligence</b><br/>rapprochement, détection, confiance, explication<br/><i>Sosso</i>"]
    C5["<b>Couche 5 — Persistance & API</b><br/>PostgreSQL, pgvector, FastAPI<br/><i>Damtoti</i>"]
    C6["<b>Couche 6 — Interface & Démo</b><br/>React, fiche de preuve, graphe<br/><i>Damtoti</i>"]

    C1 --> C2 --> C3 --> C4
    C5 -. contrat de données .- C2
    C5 -. contrat de données .- C4
    C4 --> C5 --> C6
```

**Contrat d'interface entre membres** : les dataclasses de [`backend/app/domain/claim.py`](../backend/app/domain/claim.py) (`RawClaim`, `Claim`, `ComparisonResult`, `ConfidenceAssessment`) et les schémas Pydantic de [`backend/app/schemas/`](../backend/app/schemas/). Les modifier = prévenir l'équipe.

---

## 3. Détail des phases

### P0 — Cadrage et socle · 13 → 16 oct.

| Tâche | Resp. | Livrable | Statut |
|---|---|---|---|
| Lecture des dossiers, synthèse | Tous | `DOCUMENT_TECHNIQUE.md` §1 | ✅ |
| Architecture, diagrammes | Damtoti | `DOCUMENT_TECHNIQUE.md` | ✅ |
| Squelette backend / frontend / docker | Damtoti | dépôt actuel | ✅ |
| Choisir 3 à 5 indicateurs éducation présents dans ≥ 2 sources | Parfait + Sosso | liste validée | ☐ |
| Clé API LLM, accès machines, dépôt GitHub partagé | Damtoti | `.env` | ☐ |

**J0 (16/10)** : `make up` fonctionne chez les 3 membres ; indicateurs pilotes choisis.

### P1 — Couche Données · 15 → 23 oct. · *Parfait*

| Tâche | Livrable | Critère de fin |
|---|---|---|
| Télécharger annuaires INSEED + rapports ministériels éducation | `data/corpus/` + fiche source (URL, date, licence) | ≥ 6 documents, ≥ 2 formats |
| Compléter `indicateurs.yaml` (définitions, synonymes) | référentiel | indicateurs pilotes définis |
| Compléter `zones.yaml`, `unites.yaml` | référentiels | régions + préfectures si utiles |
| Annoter manuellement ≥ 50 valeurs (vérité terrain) | `data/processed/verite_terrain.csv` | colonnes = champs `Claim` + page |
| **Identifier les 3 cas de démo réels** | fiche « cas de démo » | 1 concordant, 1 expliqué, 1 inexpliqué |

### P2 — Ingestion & Extraction · 17 → 26 oct. · *Parfait (Damtoti en appui ingestion)*

| Tâche | Module | Critère de fin |
|---|---|---|
| Upload, SHA-256, dédoublonnage | `pipeline/ingestion` | test unitaire |
| Texte PDF + bbox (PyMuPDF) | `pdf_extractor.py` | fragments en base avec page |
| Tableaux (pdfplumber) avec en-têtes comme contexte | `pdf_extractor.py` | tableaux pilotes extraits |
| XLSX / CSV | `spreadsheet_extractor.py` | 1 fichier pilote extrait |
| OCR fallback | `pdf_extractor.py` | confiance d'extraction renseignée |
| Parser de quantités FR | `quantity_parser.py` | tests (« 18,2 % », « 1 234 ») ✅ |

**J1 (26/10)** : les claims du corpus pilote sont en base, avec page et extrait ; précision ≥ 80 % sur la vérité terrain.

### P3 — Normalisation · 24 → 29 oct. · *Parfait + Sosso*

| Tâche | Critère de fin |
|---|---|
| Périodes (« 2019-2020 », « année scolaire 2019/2020 », « 2021 ») → dates | tests unitaires |
| Unités + conversions (%, ‰, effectifs, FCFA) | tests unitaires |
| Zones (libellés → codes hiérarchiques) | tests unitaires |
| Libellé brut → `indicator_code` (fuzzy + embeddings sur synonymes) | ≥ 85 % de bons mappings sur la vérité terrain |
| Statut `to_review` si non normalisable | visible dans l'API |

### P4 — Intelligence · 24 oct. → 5 nov. · *Sosso*

| Tâche | Module | Critère de fin |
|---|---|---|
| Embeddings claims/indicateurs + index pgvector | `matching/matcher.py` | top-k pertinent sur indicateurs pilotes |
| Règles de comparabilité (6 dimensions) | `matching/comparability.py` | tests par dimension |
| Verdict (arbre de décision) | `detection/detector.py` | tests ✅ + 3 cas de démo corrects |
| Score de confiance + raisons | `detection/confidence.py` | raisons lisibles pour chaque cas |
| Explication LLM + post-contrôle des nombres + gabarit de repli | `explanation/explainer.py` | 0 chiffre inventé sur les cas de démo |
| Calibrage seuils (similarité, tolérance) | notebook | valeurs fixées dans `.env` |

**J2 (04/11)** : `POST /comparisons/run` produit les 3 verdicts attendus sur le corpus réel.

### P5 — Persistance, API, Interface · 17 oct. → 7 nov. · *Damtoti*

| Tâche | Critère de fin |
|---|---|
| Première migration Alembic, seed des référentiels | `make migrate` OK |
| Repositories + endpoints workspaces / sources / claims | testés via `/docs` |
| Endpoints comparisons / evidence / graph | fiche de preuve JSON complète |
| Page Sources (dépôt, statut) | upload → statut `extracted` |
| Page Divergences (tableau + filtres verdict/indicateur) | 3 cas visibles |
| Fiche de preuve + ouverture du PDF à la bonne page | clic → page source |
| Graphe Cytoscape | nœuds indicateur/valeur/source/période/zone |
| Validation humaine (PATCH claim + audit) | correction visible + tracée |

### P6 — Intégration et tests · 5 → 9 nov. · *Tous*

- Parcours complet : dépôt → extraction → analyse → fiche → source.
- Rapport d'évaluation : précision extraction, mapping, verdicts.
- Correction des bugs bloquants uniquement.
- **Gel fonctionnel le 09/11** : plus aucune nouvelle fonctionnalité.

### P7 — Démo et présentation · 9 → 14 nov. · *Damtoti (lead), tous*

- Scénario de 5 min autour des 3 cas réels.
- Dump SQL du corpus de démo + explications pré-calculées (plan B hors-ligne).
- Vidéo de secours de la démo.
- Pitch : problème → démo → « preuve active » → impact → suite.
- 2 répétitions chronométrées minimum.

---

## 4. Jalons

```mermaid
timeline
    title Jalons DataWitness
    16 oct : J0 Socle prêt : make up chez les 3 membres : indicateurs pilotes choisis
    26 oct : J1 Extraction : claims en base avec page et extrait : précision ≥ 80 %
    04 nov : J2 Détection : 3 verdicts corrects sur corpus réel
    09 nov : J3 Gel : parcours complet dans l'interface : plan B prêt
    14 nov : Hackathon : démonstration HESTIM Casablanca
```

---

## 5. Périmètre MVP (MoSCoW)

| Must (démo impossible sans) | Should | Could | Won't (cette édition) |
|---|---|---|---|
| Ingestion PDF + XLSX | OCR | Export PDF de la fiche | Multi-pays |
| Extraction avec page + extrait | Explication LLM | Import SDMX | Comptes utilisateurs |
| Normalisation période / unité / zone | Graphe de provenance | Recherche plein texte | Crawling automatique |
| Rapprochement + règles de comparabilité | Validation humaine | | Prédiction / recommandation |
| 4 verdicts + confiance expliquée | | | |
| Tableau des divergences + fiche de preuve | | | |

---

## 6. Rituels d'équipe

| Rituel | Fréquence | Durée | Contenu |
|---|---|---|---|
| Point quotidien | chaque jour | 15 min | fait / à faire / bloquant |
| Revue de jalon | à chaque J | 45 min | démo interne, go / no-go |
| Revue de code | chaque PR | — | 1 relecteur minimum, tests verts |

**Branches Git** : `main` (toujours démontrable) ← `feat/<couche>-<sujet>` (ex. `feat/extraction-tableaux`).

---

## 7. Risques planning

| Risque | Probabilité | Parade |
|---|---|---|
| Sources INSEED difficiles à extraire (scans) | Élevée | choisir en P1 les documents les plus propres ; saisie manuelle assistée en dernier recours |
| Pas de vraie contradiction trouvée dans le corpus | Moyenne | élargir à 2ᵉ source (open data BAD) ; un cas « inexpliqué » peut être un vrai doute à soumettre |
| Retard UI | Moyenne | plan B Streamlit branché sur la même API |
| Indisponibilité d'un membre | Moyenne | contrats d'interface stables + docstrings → reprise possible |
| Réseau absent sur place | Moyenne | démo hors-ligne (dump + explications pré-calculées) |
