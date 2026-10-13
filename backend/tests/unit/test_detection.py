from app.domain.claim import ComparabilityCheck
from app.domain.enums import DifferenceCause, Verdict
from app.pipeline.detection.detector import decide_verdict, relative_gap
from app.pipeline.extraction.quantity_parser import parse_fr_number


def test_parse_fr_number():
    assert parse_fr_number("taux de 18,2 %") == 18.2
    assert parse_fr_number("1 234 élèves") == 1234.0


def test_relative_gap():
    assert round(relative_gap(18.2, 23.7), 3) == 0.232


def test_verdicts():
    ok = [ComparabilityCheck(DifferenceCause.PERIOD, True, "")]
    ko = [ComparabilityCheck(DifferenceCause.PERIOD, False, "2019 vs 2021")]
    assert decide_verdict(0.01, ok, 0.02) is Verdict.CONCORDANT
    assert decide_verdict(0.23, ko, 0.02) is Verdict.EXPLAINED_DIFFERENCE
    assert decide_verdict(0.23, ok, 0.02) is Verdict.UNEXPLAINED_CONTRADICTION
