"""Étape 6 — Explication : IA générative limitée aux éléments extraits et aux sources retrouvées."""

from app.domain.claim import ComparisonResult

SYSTEM_PROMPT = """Tu expliques l'écart entre deux valeurs statistiques.
Règles strictes :
- N'utilise QUE les métadonnées et extraits fournis.
- N'invente aucun chiffre, aucune page, aucune citation.
- Si l'information manque, écris « information absente des sources ».
- Cite chaque affirmation avec [A] ou [B]."""


class Explainer:
    def explain(self, result: ComparisonResult) -> str:
        raise NotImplementedError
