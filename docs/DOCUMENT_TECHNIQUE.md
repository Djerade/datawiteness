# DataWitness Africa — Document technique

> Rendre les chiffres publics **vérifiables, comparables et explicables**.
> Hackathon *L'Aube de l'Intelligence Artificielle — Édition 2* · 14 novembre 2026 · HESTIM, Casablanca

| | |
|---|---|
| **Version** | 0.1 — 13 octobre 2026 |
| **Équipe** | DJERADE GOLBE Parfait (Data & Qualité) · KOMOSSI Sosso (IA & Analyse) · YENDONGOU Damtoti (Technique & Chef de projet) |
| **Établissement** | UCAO-UUT — Togo · COTIA |
| **Documents sources** | [`sources/DataWitness_AubeIA2026.pdf`](sources/DataWitness_AubeIA2026.pdf) · [`sources/Proposition_1_DataWitness_Africa_Dossier.docx`](sources/Proposition_1_DataWitness_Africa_Dossier.docx) |

Les diagrammes sont en **Mermaid** (rendus nativement par GitHub, GitLab, VS Code).

---

## Sommaire

1. [Synthèse des documents](#1-synthèse-des-documents)
2. [Exigences](#2-exigences)
3. [Contexte et acteurs](#3-contexte-et-acteurs)
4. [Architecture](#4-architecture)
5. [Pipeline de traitement](#5-pipeline-de-traitement)
6. [Modèle de données](#6-modèle-de-données)
7. [Logique de vérification](#7-logique-de-vérification)
8. [Diagrammes de séquence](#8-diagrammes-de-séquence)
9. [Cycles de vie (états)](#9-cycles-de-vie-états)
10. [API REST](#10-api-rest)
11. [Interface web](#11-interface-web)
12. [Déploiement](#12-déploiement)
13. [Choix technologiques](#13-choix-technologiques)
14. [Qualité, tests et garde-fous](#14-qualité-tests-et-garde-fous)
15. [Limites et risques](#15-limites-et-risques)

---

## 1. Synthèse des documents

**Problème.** Les décisions publiques s'appuient sur des rapports, annuaires, PDF, Excel et bases de données hétérogènes. Le problème n'est pas l'absence de données, mais la difficulté à savoir rapidement si plusieurs chiffres **désignent la même chose**, s'ils sont **à jour**, **comment ils ont été calculés** et **pourquoi ils diffèrent**. Les IA génératives aggravent le risque : elles produisent une réponse fluide à partir de sources incompatibles sans signaler la contradiction.

**Proposition.** Un assistant de vérification qui, à partir de plusieurs documents :

1. extrait les **affirmations quantitatives** et leurs métadonnées ;
2. **rapproche** les indicateurs susceptibles de désigner la même réalité ;
3. **détecte** les écarts significatifs ;
4. **distingue** contradiction réelle / différence de périmètre ou de méthode / comparaison invalide ;
5. attribue un **niveau de confiance expliqué** ;
6. permet de **remonter à la source** (document, page, tableau, passage).

**Principe directeur : la « preuve active ».** L'IA sert à l'extraction, au rapprochement sémantique et à l'explication ; les **règles déterministes** et la **traçabilité** empêchent qu'une réponse générée soit prise pour une preuve.

**Périmètre du prototype.** Un domaine (éducation au Togo), un corpus restreint (annuaires INSEED, publications ministérielles, open data) et **trois cas de démonstration** :

| Cas | Situation | Verdict attendu |
|---|---|---|
| 1 | Deux valeurs concordantes | `concordant` |
| 2 | Deux valeurs différentes expliquées par période / périmètre / méthode | `explained_difference` |
| 3 | Écart inexpliqué à soumettre à un humain | `unexplained_contradiction` |

> Les valeurs 18,2 % / 23,7 % du dossier sont **illustratives** : chaque valeur affichée par le prototype devra provenir d'une source réelle vérifiable.

---

## 2. Exigences

### 2.1 Fonctionnelles

| ID | Exigence | Priorité |
|---|---|---|
| F1 | Déposer / sélectionner des sources PDF, XLSX, CSV | Must |
| F2 | Extraire texte, tableaux, valeurs, unités, dates (+ OCR des pages scannées) | Must |
| F3 | Conserver pour chaque valeur : source, date, page/emplacement, indicateur, période, unité, zone, population, contexte | Must |
| F4 | Normaliser indicateurs, périodes, zones, unités via des référentiels | Must |
| F5 | Rapprocher sémantiquement les indicateurs (formulations différentes) | Must |
| F6 | Contrôler la comparabilité (période, unité, zone, population, définition, méthode) | Must |
| F7 | Détecter les écarts et produire un verdict parmi 4 | Must |
| F8 | Calculer un niveau de confiance **accompagné de raisons** | Must |
| F9 | Générer une explication textuelle **ancrée uniquement dans les extraits** | Should |
| F10 | Fiche de preuve : valeurs côte à côte, passages, lien vers la page source | Must |
| F11 | Tableau des divergences filtrable | Must |
| F12 | Graphe des relations indicateur–valeur–source–période–territoire | Should |
| F13 | Validation/correction humaine d'une valeur, tracée dans le journal | Should |
| F14 | Export de la fiche de preuve (JSON / PDF) | Could |

### 2.2 Non fonctionnelles

| ID | Exigence |
|---|---|
| NF1 | **Traçabilité totale** : toute valeur affichée est reliée à un fragment source ; aucune valeur sans preuve |
| NF2 | **Non-hallucination** : le LLM ne reçoit et ne cite que les extraits ; une preuve absente est signalée comme telle |
| NF3 | **Explicabilité** : le verdict est issu de règles lisibles, pas du LLM |
| NF4 | **Reproductibilité** : empreinte SHA-256 des fichiers, journal d'audit horodaté |
| NF5 | **Respect des licences** des documents publics |
| NF6 | Démarrage complet en une commande (`make up`) ; démo hors-ligne possible (sauf explication LLM) |
| NF7 | Interface en français, temps de réponse < 2 s sur les vues de consultation |

---

## 3. Contexte et acteurs

### 3.1 Diagramme de contexte (C4 — niveau 1)

```mermaid
flowchart LR
    subgraph Utilisateurs
        U1([Analyste / Institut statistique])
        U2([Journaliste / Fact-checker])
        U3([Chercheur / Étudiant])
        U4([ONG / Partenaire])
        U5([Équipe Data / IA])
    end

    DW[["<b>DataWitness Africa</b><br/>Extraction · Rapprochement<br/>Détection · Preuve"]]

    subgraph Sources publiques
        S1[(INSEED Togo<br/>annuaires)]
        S2[(Ministères<br/>publications)]
        S3[(Open data<br/>BAD / AIH, SDMX)]
    end

    LLM{{Service LLM<br/>explication encadrée}}

    U1 & U2 & U3 & U4 & U5 -->|déposent, consultent, valident| DW
    S1 & S2 & S3 -->|PDF · XLSX · CSV| DW
    DW -->|extraits + métadonnées uniquement| LLM
    LLM -->|texte d'explication| DW
```

### 3.2 Cas d'utilisation

```mermaid
flowchart LR
    A([Utilisateur])
    R([Relecteur humain])

    subgraph DataWitness
        UC1((Créer un dossier d'analyse))
        UC2((Déposer des sources))
        UC3((Consulter les affirmations extraites))
        UC4((Lancer le rapprochement))
        UC5((Filtrer les divergences))
        UC6((Ouvrir une fiche de preuve))
        UC7((Voir la page source))
        UC8((Explorer le graphe))
        UC9((Valider / corriger une valeur))
        UC10((Trancher une contradiction))
        UC11((Exporter la preuve))
    end

    A --- UC1 & UC2 & UC3 & UC4 & UC5 & UC6 & UC8 & UC11
    UC6 -. inclut .-> UC7
    R --- UC9 & UC10
    UC10 -. étend .-> UC6
```

---

## 4. Architecture

### 4.1 Architecture en couches

```mermaid
flowchart TB
    subgraph L1["① Présentation — frontend/ (React + Vite)"]
        P1[Tableau de bord] --- P2[Sources] --- P3[Divergences] --- P4[Fiche de preuve] --- P5[Graphe]
    end

    subgraph L2["② API — backend/app/api (FastAPI)"]
        A1[/workspaces/] --- A2[/sources/] --- A3[/claims/] --- A4[/comparisons/] --- A5[/graph/]
    end

    subgraph L3["③ Services — backend/app/services"]
        SV[AnalysisService<br/>orchestration du pipeline]
    end

    subgraph L4["④ Pipeline métier — backend/app/pipeline"]
        direction LR
        I[ingestion] --> E[extraction] --> N[normalization] --> M[matching] --> D[detection] --> X[explanation] --> V[evidence]
    end

    subgraph L5["⑤ Domaine — backend/app/domain"]
        DM[Claim · Comparison · Verdict<br/>ConfidenceAssessment · EvidenceLocation]
    end

    subgraph L6["⑥ Persistance — backend/app/db"]
        DB[(PostgreSQL 16<br/>+ pgvector)]
        FS[(Stockage fichiers<br/>data/raw)]
        REF[(Référentiels YAML<br/>data/referentiels)]
    end

    L1 -->|HTTP / JSON| L2 --> L3 --> L4
    L4 --> L5
    L3 --> L6
    L4 --> REF
```

**Règle de dépendance** : chaque couche ne dépend que des couches inférieures. Le **domaine** est pur (dataclasses, aucune dépendance à FastAPI ou SQLAlchemy) → les règles de comparabilité et de verdict sont testables unitairement.

### 4.2 Diagramme de conteneurs (C4 — niveau 2)

```mermaid
flowchart LR
    User([Navigateur])

    subgraph Docker Compose
        FE["<b>frontend</b><br/>React · Vite · Cytoscape<br/>:5173"]
        BE["<b>backend</b><br/>FastAPI · SQLAlchemy<br/>pipeline Python<br/>:8000"]
        BG["tâches de fond<br/>(extraction, OCR, embeddings)"]
        PG[("<b>db</b><br/>PostgreSQL 16 + pgvector<br/>:5432")]
        VOL[("volume ./data")]
    end

    EMB["Modèle d'embeddings<br/>multilingue (local)"]
    LLM{{API LLM}}

    User --> FE -->|REST| BE
    BE --> BG
    BE & BG --> PG
    BE & BG --> VOL
    BG --> EMB
    BE -->|extraits uniquement| LLM
```

### 4.3 Arborescence du dépôt

```
datawiteness/
├── backend/
│   ├── app/
│   │   ├── api/v1/routes/      # ② endpoints REST
│   │   ├── services/           # ③ orchestration
│   │   ├── pipeline/           # ④ les 7 étapes de traitement
│   │   │   ├── ingestion/  extraction/  normalization/  matching/
│   │   │   └── detection/  explanation/  evidence/
│   │   ├── domain/             # ⑤ objets métier purs + enums
│   │   ├── db/                 # ⑥ ORM, session, repositories
│   │   ├── schemas/            # DTO Pydantic
│   │   ├── core/               # config, logs
│   │   └── workers/            # tâches longues
│   ├── migrations/             # Alembic
│   ├── tests/{unit,integration}
│   └── scripts/                # seed des référentiels…
├── frontend/src/{pages,components,api,hooks,types}
├── data/{raw,interim,processed,corpus,referentiels}
├── notebooks/                  # exploration corpus, évaluation
├── infra/postgres/init.sql
├── docs/
└── docker-compose.yml · Makefile · .env.example
```

---

## 5. Pipeline de traitement

Le dossier décrit 8 étapes ; l'étape 8 (Interface) est portée par la couche présentation.

```mermaid
flowchart LR
    S[(PDF · XLSX · CSV)] --> I

    I["<b>1. Ingestion</b><br/>format, SHA-256,<br/>métadonnées source"]
    E["<b>2. Extraction</b><br/>texte, tableaux, OCR<br/>→ RawClaim + Fragment"]
    N["<b>3. Normalisation</b><br/>indicateur, période,<br/>zone, unité"]
    M["<b>4. Rapprochement</b><br/>embeddings + règles<br/>de comparabilité"]
    D["<b>5. Détection</b><br/>écart relatif,<br/>verdict, confiance"]
    X["<b>6. Explication</b><br/>LLM ancré<br/>sur les extraits"]
    P["<b>7. Preuve</b><br/>fiche, provenance,<br/>journal"]
    UI["<b>8. Interface</b><br/>divergences, filtres,<br/>graphe"]

    I --> E --> N --> M --> D --> X --> P --> UI

    REF[(Référentiels<br/>indicateurs · zones · unités)] -.-> N
    REF -.-> M
    N -->|non normalisable| RV{{À revoir<br/>humain}}
    E -->|OCR peu fiable| RV
```

| Étape | Module | Entrée → Sortie | Techniques | Responsable |
|---|---|---|---|---|
| 1 Ingestion | `pipeline/ingestion` | fichier → `Source` | détection de format, SHA-256 (dédoublonnage) | Damtoti |
| 2 Extraction | `pipeline/extraction` | `Source` → `Fragment` + `RawClaim` | PyMuPDF (texte + bbox), pdfplumber (tableaux), Tesseract (OCR fra), pandas/openpyxl, regex des nombres FR | Parfait |
| 3 Normalisation | `pipeline/normalization` | `RawClaim` → `Claim` | référentiels YAML, parsing de périodes (« 2019-2020 », « année scolaire »), conversions d'unités, hiérarchie géographique | Parfait |
| 4 Rapprochement | `pipeline/matching` | `Claim` × pool → paires candidates + contrôles | embeddings multilingues (pgvector, cosinus), RapidFuzz sur libellés, règles de comparabilité | Sosso |
| 5 Détection | `pipeline/detection` | paire → `ComparisonResult` + `ConfidenceAssessment` | écart relatif, arbre de décision, score de confiance pondéré | Sosso |
| 6 Explication | `pipeline/explanation` | résultat → texte | LLM avec prompt contraint, citations [A]/[B], température 0 | Sosso |
| 7 Preuve | `pipeline/evidence` | résultat → fiche | assemblage provenance, `AuditEvent` | Damtoti |
| 8 Interface | `frontend/` | API → vues | React, React Query, Cytoscape | Damtoti |

### 5.1 Détail de l'extraction

```mermaid
flowchart TD
    F[Fichier] --> T{Format ?}
    T -->|PDF| P1[Pour chaque page]
    P1 --> Q{Texte natif<br/>exploitable ?}
    Q -->|oui| P2[PyMuPDF : blocs + bbox]
    Q -->|non : scan| P3[Tesseract OCR fra<br/>confiance par mot]
    P2 & P3 --> P4[pdfplumber : détection de tableaux]
    P4 --> TB[Tableau → cellules<br/>en-têtes ligne/colonne = contexte]
    P2 & P3 --> TX[Texte → phrases contenant<br/>un nombre + indicateur]
    T -->|XLSX / CSV| X1[pandas : feuilles,<br/>en-têtes multi-niveaux]
    X1 --> TB
    TB & TX --> RC["RawClaim<br/>(libellé, valeur, unité, période,<br/>zone, population, contexte, page, bbox,<br/>méthode, confiance d'extraction)"]
    RC --> FR[(Fragment + Claim<br/>en base)]
```

---

## 6. Modèle de données

### 6.1 Diagramme entité-association

```mermaid
erDiagram
    WORKSPACE ||--o{ SOURCE : contient
    SOURCE ||--o{ FRAGMENT : "découpée en"
    FRAGMENT ||--o{ CLAIM : "prouve"
    INDICATOR |o--o{ CLAIM : "normalise"
    CLAIM ||--o{ COMPARISON : "claim_a"
    CLAIM ||--o{ COMPARISON : "claim_b"
    AUDIT_EVENT }o--|| CLAIM : "trace (polymorphe)"

    WORKSPACE {
        uuid id PK
        string name
        string domain
        datetime created_at
    }
    SOURCE {
        uuid id PK
        uuid workspace_id FK
        string title
        string publisher
        date published_on
        string url
        string license
        enum format "pdf|xlsx|csv|html"
        string file_path
        string sha256 UK
        enum status
    }
    FRAGMENT {
        uuid id PK
        uuid source_id FK
        int page
        string table_ref
        json bbox
        text text
        enum method "text|table|ocr|spreadsheet"
        vector embedding
    }
    INDICATOR {
        string code PK
        string label
        json synonyms
        text definition
        string unit
        vector embedding
    }
    CLAIM {
        uuid id PK
        uuid fragment_id FK
        string indicator_code FK
        string indicator_label_raw
        float value
        string value_raw
        string unit
        date period_start
        date period_end
        string zone_code
        string population
        text definition
        text method_note
        float extraction_confidence
        enum status
        vector embedding
    }
    COMPARISON {
        uuid id PK
        uuid claim_a_id FK
        uuid claim_b_id FK
        float similarity
        float relative_gap
        json checks
        json causes
        enum verdict
        enum confidence_level
        float confidence_score
        json confidence_reasons
        text explanation
    }
    AUDIT_EVENT {
        uuid id PK
        string entity_type
        uuid entity_id
        string action
        string actor
        json payload
        datetime created_at
    }
```

Implémentation : [`backend/app/db/models.py`](../backend/app/db/models.py).

### 6.2 Diagramme de classes du domaine

```mermaid
classDiagram
    class EvidenceLocation {
        +str source_id
        +int page
        +str table_ref
        +str snippet
        +tuple bbox
    }
    class RawClaim {
        +str indicator_label
        +str value_text
        +str unit_text
        +str period_text
        +str zone_text
        +str population_text
        +str context
        +ExtractionMethod method
        +float extraction_confidence
    }
    class Claim {
        +str id
        +str indicator_code
        +float value
        +str unit
        +str period_start
        +str period_end
        +str zone_code
        +str population
        +str definition
        +float extraction_confidence
    }
    class ComparabilityCheck {
        +DifferenceCause dimension
        +bool compatible
        +str detail
    }
    class ComparisonResult {
        +float similarity
        +float relative_gap
        +Verdict verdict
        +list~DifferenceCause~ causes
    }
    class ConfidenceAssessment {
        +ConfidenceLevel level
        +float score
        +list~str~ reasons
    }
    class Verdict {
        <<enumeration>>
        CONCORDANT
        EXPLAINED_DIFFERENCE
        UNEXPLAINED_CONTRADICTION
        INVALID_COMPARISON
    }
    class DifferenceCause {
        <<enumeration>>
        PERIOD
        GEOGRAPHY
        POPULATION
        DEFINITION
        METHOD
        UNIT
        REVISION
    }
    class Extractor {
        <<interface>>
        +extract(path, source_id) list~RawClaim~
    }
    class Normalizer {
        +normalize(RawClaim) Claim
    }
    class SemanticMatcher {
        +candidates(Claim, pool, top_k) list
    }
    class Explainer {
        +explain(ComparisonResult) str
    }

    RawClaim --> EvidenceLocation
    Claim --> EvidenceLocation
    ComparisonResult --> "2" Claim
    ComparisonResult --> "*" ComparabilityCheck
    ComparisonResult --> Verdict
    ComparabilityCheck --> DifferenceCause
    ComparisonResult ..> ConfidenceAssessment : évaluée par
    Extractor ..> RawClaim : produit
    Normalizer ..> Claim : produit
    SemanticMatcher ..> Claim
    Explainer ..> ComparisonResult
    Extractor <|.. PdfExtractor
    Extractor <|.. SpreadsheetExtractor
```

Implémentation : [`backend/app/domain/`](../backend/app/domain/).

---

## 7. Logique de vérification

### 7.1 Contrôles de comparabilité

Avant toute comparaison de valeurs, six dimensions sont contrôlées (règles déterministes, `pipeline/matching/comparability.py`) :

| Dimension | Compatible si… | Exemple d'incompatibilité |
|---|---|---|
| Période | intervalles identiques (ou chevauchement total) | 2019-2020 vs 2021-2022 |
| Territoire | même code zone | National vs Région Savanes |
| Population | même population cible | Filles vs Ensemble |
| Unité | même unité après conversion | % vs effectif |
| Définition | même code indicateur et définition non contradictoire | Abandon *intra-annuel* vs *cumulé* |
| Méthode | même méthode ou méthode inconnue (→ baisse de confiance) | Enquête ménages vs données administratives |

### 7.2 Arbre de décision du verdict

```mermaid
flowchart TD
    A[Paire candidate A, B] --> S{Similarité sémantique<br/>≥ seuil ?}
    S -->|non| Z[Pas de comparaison]
    S -->|oui| U{Unités<br/>convertibles ?}
    U -->|non| INV["<b>invalid_comparison</b><br/>ne mesurent pas la même chose"]
    U -->|oui| G["Écart relatif<br/>|a−b| / max(|a|,|b|)"]
    G --> T{Écart ≤ tolérance ?}
    T -->|oui| C["<b>concordant</b>"]
    T -->|non| K{Au moins un contrôle<br/>incompatible ?<br/>période, zone, population,<br/>définition, méthode}
    K -->|oui| EXP["<b>explained_difference</b><br/>+ causes listées"]
    K -->|non| CON["<b>unexplained_contradiction</b><br/>→ revue humaine"]

    style C fill:#d4edda,stroke:#2e7d32
    style EXP fill:#fff3cd,stroke:#b58900
    style CON fill:#f8d7da,stroke:#c62828
    style INV fill:#e2e3e5,stroke:#555
```

Implémentation de référence : `decide_verdict()` dans [`backend/app/pipeline/detection/detector.py`](../backend/app/pipeline/detection/detector.py) (testé dans `tests/unit/test_detection.py`).

### 7.3 Niveau de confiance expliqué

Le score n'est **jamais présenté seul** : il est toujours accompagné de ses raisons.

```mermaid
flowchart LR
    Q1["Qualité d'extraction<br/>(texte natif > tableau > OCR)"] --> W
    Q2["Similarité sémantique<br/>des indicateurs"] --> W
    Q3["Complétude des métadonnées<br/>(période, zone, unité, définition)"] --> W
    Q4["Nature de la source<br/>(officielle, date, révision)"] --> W
    Q5["Validation humaine"] --> W
    W(("Score pondéré<br/>0 – 1")) --> L{Seuils}
    L -->|≥ 0,75| H[Élevé]
    L -->|0,45 – 0,75| M[Moyen]
    L -->|< 0,45| B[Faible]
    W --> R["Raisons lisibles<br/>ex. « valeur B issue d'OCR »,<br/>« méthode de calcul absente »"]
```

Pondérations initiales (à calibrer sur le jeu de démo) : extraction 0,30 · similarité 0,20 · complétude 0,25 · source 0,15 · validation humaine 0,10.

### 7.4 Explication encadrée (anti-hallucination)

```mermaid
flowchart LR
    CR[ComparisonResult<br/>+ checks + causes] --> PB[Construction du prompt]
    FA[Extrait A<br/>page, tableau] --> PB
    FB[Extrait B<br/>page, tableau] --> PB
    PB --> LLM{{LLM<br/>température 0}}
    LLM --> VAL{Post-contrôle :<br/>chaque nombre cité<br/>existe dans A ou B ?}
    VAL -->|oui| OK[Explication publiée]
    VAL -->|non| KO[Rejet → explication<br/>par gabarit déterministe]
```

Le verdict est **calculé avant** l'appel au LLM ; celui-ci ne fait que le formuler. Si le LLM est indisponible, un gabarit textuel construit à partir des `checks` est utilisé.

### 7.5 Graphe de provenance (exemple)

```mermaid
flowchart LR
    IND{{EDU_TAUX_ABANDON<br/>Taux d'abandon scolaire}}
    V1([18,2 %])
    V2([23,7 %])
    S1[Annuaire INSEED A<br/>p. 42, tableau 3.1]
    S2[Rapport ministériel B<br/>p. 17]
    P1[/2019-2020/]
    P2[/2021-2022/]
    Z1[(Togo)]

    IND --- V1 & V2
    V1 -->|extrait de| S1
    V2 -->|extrait de| S2
    V1 -->|période| P1
    V2 -->|période| P2
    V1 & V2 -->|territoire| Z1
    V1 -.-|explained_difference : période| V2
```

*(valeurs illustratives)*

---

## 8. Diagrammes de séquence

### 8.1 Dépôt et extraction d'une source

```mermaid
sequenceDiagram
    autonumber
    actor U as Utilisateur
    participant FE as Frontend
    participant API as API /sources
    participant SV as AnalysisService
    participant BG as Tâche de fond
    participant EX as Extractor
    participant NO as Normalizer
    participant DB as PostgreSQL

    U->>FE: Dépose rapport.pdf
    FE->>API: POST /sources (multipart)
    API->>SV: ingest(workspace, fichier)
    SV->>SV: SHA-256, détection format
    SV->>DB: INSERT source (status=uploaded)
    SV-->>API: source_id
    API-->>FE: 201 + source
    API->>BG: extract(source_id)
    BG->>DB: status=extracting
    BG->>EX: extract(path)
    EX-->>BG: Fragments + RawClaims
    loop Pour chaque RawClaim
        BG->>NO: normalize(raw)
        NO-->>BG: Claim (ou TO_REVIEW)
    end
    BG->>DB: INSERT fragments, claims, embeddings
    BG->>DB: status=extracted + AuditEvent
    FE->>API: GET /sources (polling)
    API-->>FE: status=extracted
```

### 8.2 Rapprochement, détection et fiche de preuve

```mermaid
sequenceDiagram
    autonumber
    actor U as Utilisateur
    participant FE as Frontend
    participant API as API /comparisons
    participant MA as Matcher
    participant DE as Detector
    participant XP as Explainer
    participant LLM as LLM
    participant DB as PostgreSQL

    U->>FE: « Lancer l'analyse »
    FE->>API: POST /comparisons/run
    API->>DB: claims du workspace
    loop Pour chaque claim
        API->>MA: candidates(claim, pool)
        MA->>DB: recherche vectorielle (pgvector)
        MA-->>API: paires + similarité
        API->>MA: check_comparability(a, b)
        API->>DE: compare + assess
        DE-->>API: verdict, causes, confiance
        opt verdict ≠ concordant
            API->>XP: explain(résultat, extraits)
            XP->>LLM: prompt contraint
            LLM-->>XP: texte
            XP-->>API: explication validée
        end
        API->>DB: INSERT comparison + AuditEvent
    end
    API-->>FE: 202
    U->>FE: Ouvre une divergence
    FE->>API: GET /comparisons/{id}/evidence
    API-->>FE: fiche (A, B, contrôles, explication, extraits)
    U->>FE: « Voir la source »
    FE->>API: GET /sources/{id}/file (page 42)
```

### 8.3 Validation humaine

```mermaid
sequenceDiagram
    actor R as Relecteur
    participant FE as Frontend
    participant API as API /claims
    participant DB as PostgreSQL
    R->>FE: Corrige 23,7 → 21,7 (erreur OCR)
    FE->>API: PATCH /claims/{id}
    API->>DB: UPDATE claim (status=validated)
    API->>DB: AuditEvent(action=corrected, avant/après, acteur)
    API->>API: recalcul des comparaisons liées
    API-->>FE: claim mis à jour
```

---

## 9. Cycles de vie (états)

### 9.1 Source

```mermaid
stateDiagram-v2
    [*] --> uploaded: dépôt
    uploaded --> extracting: tâche lancée
    extracting --> extracted: succès
    extracting --> failed: erreur (format, PDF protégé…)
    failed --> extracting: relance
    extracted --> [*]
```

### 9.2 Affirmation (Claim)

```mermaid
stateDiagram-v2
    [*] --> extracted
    extracted --> normalized: référentiels OK
    extracted --> to_review: OCR douteux / unité ou zone inconnue
    normalized --> to_review: signalée par un utilisateur
    to_review --> validated: correction humaine
    normalized --> validated: confirmation humaine
    to_review --> rejected: valeur erronée
    validated --> [*]
    rejected --> [*]
```

### 9.3 Comparaison

```mermaid
stateDiagram-v2
    computed: calculée
    in_review: en revue
    confirmed: contradiction confirmée
    [*] --> computed
    computed --> concordant
    computed --> explained_difference
    computed --> invalid_comparison
    computed --> unexplained_contradiction
    unexplained_contradiction --> in_review: assignée
    in_review --> explained_difference: cause trouvée
    in_review --> confirmed: contradiction réelle
```

---

## 10. API REST

Base : `/api/v1` — documentation interactive : `http://localhost:8000/docs`.

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/health` | État de l'API |
| POST / GET | `/workspaces` | Créer / lister les dossiers d'analyse |
| POST | `/sources?workspace_id=` | Déposer un fichier (multipart) |
| GET | `/sources?workspace_id=` | Lister les sources et leur statut |
| GET | `/sources/{id}/file` | Fichier original (affichage de la page de preuve) |
| GET | `/claims?workspace_id=&indicator_code=` | Affirmations extraites |
| PATCH | `/claims/{id}` | Validation / correction humaine |
| POST | `/comparisons/run?workspace_id=` | Lancer rapprochement + détection |
| GET | `/comparisons?workspace_id=&verdict=` | Tableau des divergences |
| GET | `/comparisons/{id}/evidence` | Fiche de preuve complète |
| GET | `/graph?workspace_id=&indicator_code=` | Graphe de provenance (format Cytoscape) |

Exemple de fiche de preuve (`GET /comparisons/{id}/evidence`) :

```json
{
  "comparison": {
    "verdict": "explained_difference",
    "causes": ["period"],
    "relative_gap": 0.232,
    "confidence_level": "medium",
    "confidence_reasons": ["valeur B issue d'un tableau", "méthode de calcul absente dans A"],
    "explanation": "Les deux valeurs portent sur des années scolaires différentes [A] 2019-2020, [B] 2021-2022…",
    "claim_a": { "value": 18.2, "unit": "PCT", "period_start": "2019-09-01", "zone_code": "TG" },
    "claim_b": { "value": 23.7, "unit": "PCT", "period_start": "2021-09-01", "zone_code": "TG" }
  },
  "evidence_a": { "source_title": "Annuaire A", "page": 42, "table_ref": "T3.1", "snippet": "…" },
  "evidence_b": { "source_title": "Rapport B", "page": 17, "table_ref": null, "snippet": "…" }
}
```

---

## 11. Interface web

### 11.1 Navigation

```mermaid
flowchart LR
    D[Tableau de bord<br/>compteurs par verdict] --> S[Sources<br/>dépôt + statut]
    D --> V[Divergences<br/>tableau filtrable]
    V --> F[Fiche de preuve]
    F --> PDF[Page source<br/>surlignée]
    D --> G[Graphe de provenance]
    G --> F
```

### 11.2 Maquette de la fiche de preuve

```
┌───────────────────────────────────────────────────────────────────────┐
│  Taux d'abandon scolaire — Togo          ⚠ DIFFÉRENCE EXPLIQUÉE      │
│  Confiance : MOYENNE  (valeur B issue d'un tableau ; méthode A absente)│
├──────────────────────────────────┬────────────────────────────────────┤
│  SOURCE A                        │  SOURCE B                          │
│  18,2 %                          │  23,7 %                            │
│  Période  2019-2020        ✗     │  Période  2021-2022                │
│  Zone     Togo             ✓     │  Zone     Togo                     │
│  Unité    %                ✓     │  Unité    %                        │
│  Annuaire A · p.42 · T3.1 [voir] │  Rapport B · p.17        [voir]    │
│  « …extrait… »                   │  « …extrait… »                     │
├──────────────────────────────────┴────────────────────────────────────┤
│  Explication : les deux valeurs portent sur des années scolaires      │
│  différentes [A][B] ; la comparaison directe n'est pas valide.        │
│                              [Valider]  [Signaler]  [Exporter]        │
└───────────────────────────────────────────────────────────────────────┘
```

Code de couleur des verdicts : vert = concordant · orange = différence expliquée · rouge = contradiction inexpliquée · gris = comparaison invalide.

---

## 12. Déploiement

```mermaid
flowchart TB
    subgraph Poste["Poste de démo (Linux / macOS)"]
        subgraph DC["docker compose"]
            FE["frontend<br/>node:20-alpine<br/>:5173"]
            BE["backend<br/>python:3.11-slim + tesseract-fra<br/>:8000"]
            DB[("db<br/>pgvector/pgvector:pg16<br/>:5432")]
        end
        VOL[("./data<br/>raw · processed")]
        PGV[("volume pgdata")]
    end
    NAV([Navigateur]) --> FE
    FE --> BE --> DB
    BE --- VOL
    DB --- PGV
    BE -. HTTPS .-> LLM{{API LLM}}
```

```bash
cp .env.example .env      # renseigner ANTHROPIC_API_KEY (optionnel)
make up                   # db + backend + frontend
# ou en développement :
make db && make install-back && make migrate && make back
make install-front && make front
```

**Plan B démo** : base pré-remplie (dump SQL du corpus de démonstration) + explications pré-calculées, pour une démonstration sans réseau.

---

## 13. Choix technologiques

| Besoin | Choix | Justification | Alternative |
|---|---|---|---|
| Langage pipeline | Python 3.10+ | écosystème data/IA, compétences de l'équipe | — |
| API | FastAPI | typage Pydantic, OpenAPI auto, async | Flask |
| Base de données | PostgreSQL 16 + pgvector | relationnel + vectoriel dans un seul moteur | SQLite + FAISS |
| Texte PDF | PyMuPDF | rapide, coordonnées (bbox) pour surligner la preuve | pdfminer |
| Tableaux PDF | pdfplumber | tableaux à bordures fréquents dans les annuaires | Camelot |
| OCR | Tesseract (fra) | libre, local | docTR, EasyOCR |
| Excel / CSV | pandas + openpyxl | standard | — |
| Embeddings | `paraphrase-multilingual-MiniLM-L12-v2` (384 d) | multilingue FR, léger, CPU | bge-m3 |
| Similarité de libellés | RapidFuzz | robuste aux variantes orthographiques | — |
| Explication | LLM via API (Claude), température 0 | qualité en français, suivi des consignes | LLM local (Ollama) |
| Frontend | React 18 + Vite + TypeScript | interface riche (fiche, graphe) | Streamlit (plan B rapide) |
| Graphe | Cytoscape.js | graphe interactif de provenance | vis-network |
| Migrations | Alembic | versionnement du schéma | — |
| Packaging | uv · npm · Docker Compose | installation reproductible | — |

---

## 14. Qualité, tests et garde-fous

| Niveau | Contenu | Outil |
|---|---|---|
| Unitaires | parsing des nombres FR, périodes, unités, règles de comparabilité, verdict, score de confiance | pytest |
| Intégration | endpoints API, pipeline complet sur 2-3 fichiers d'exemple | pytest + TestClient |
| Évaluation extraction | précision / rappel sur un échantillon annoté manuellement (≥ 50 valeurs) | notebook |
| Évaluation rapprochement | précision des paires sur les indicateurs du référentiel | notebook |
| Démo | les 3 cas (concordant, expliqué, inexpliqué) reproduits de bout en bout | script de démo |
| Lint | style et imports | ruff, tsc |

**Garde-fous éthiques et techniques**

- Aucune valeur sans `fragment_id` → contrainte en base (FK non nulle).
- Le LLM ne produit **jamais** de verdict ni de chiffre ; post-contrôle des nombres cités.
- Toute correction humaine est journalisée (avant / après / acteur).
- Licence et URL de chaque source conservées et affichées.

---

## 15. Limites et risques

| Risque | Impact | Mitigation |
|---|---|---|
| OCR erroné sur tableaux scannés | valeurs fausses | confiance d'extraction, statut `to_review`, validation humaine des valeurs critiques |
| Une divergence n'est pas une erreur | faux positifs | contrôles de comparabilité **avant** verdict ; vocabulaire prudent (« possible ») |
| Documents eux-mêmes erronés ou révisés | confusion | cause `REVISION`, date de publication affichée |
| Peu d'indicateurs communs entre sources | démo pauvre | sélection volontaire du corpus dès la phase 1 |
| LLM indisponible le jour J | pas d'explication | gabarit déterministe + explications pré-calculées |
| Temps limité (≈ 1 mois) | périmètre non tenu | MVP strict = 3 cas sur 1 domaine ; Streamlit en plan B UI |
| Droits de réutilisation | juridique | vérifier les licences INSEED / ministères à l'ingestion |

---

*Planification détaillée : voir [`PLANIFICATION.md`](PLANIFICATION.md).*
