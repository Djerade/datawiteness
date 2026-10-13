"""Repérage des quantités dans un texte : « 18,2 % », « 1 234 élèves », « 2019-2020 »."""

import re

# Nombre au format français : séparateur de milliers espace / point, décimale virgule
NUMBER_FR = re.compile(r"(?<![\w,.])(\d{1,3}(?:[  .]\d{3})+|\d+)(?:,(\d+))?(?![\w])")


def parse_fr_number(text: str) -> float | None:
    m = NUMBER_FR.search(text)
    if not m:
        return None
    integer = re.sub(r"[  .]", "", m.group(1))
    decimals = m.group(2)
    return float(f"{integer}.{decimals}") if decimals else float(integer)
