import pytest
from pytest import approx 
from tesla_app import cels_to_fahr
from tesla_app import fahr_to_cels


def test_cels_to_fahr():
    assert cels_to_fahr(75) == "167°F"
    assert cels_to_fahr(5) == "41°F"
    assert cels_to_fahr(32) == "89.6°F"
    assert cels_to_fahr(-2) == "28.4°F"
    assert cels_to_fahr(40) == "104°F"
    assert cels_to_fahr(22) == "71.6°F"
    1
def test_fahr_to_cels():
    assert fahr_to_cels(75) == pytest.approx(23.8889, .01)
    assert fahr_to_cels("75°F") == pytest.approx(23.8889, .01)
    assert fahr_to_cels("60") == pytest.approx(15.5556)
    assert fahr_to_cels(90) == pytest.approx(32.2222)
    assert fahr_to_cels("7m9h") == pytest.approx(26.1111)
    assert fahr_to_cels(105) == pytest.approx(40.5556)
    assert fahr_to_cels(-7) == pytest.approx(-21.6667)

pytest.main(["test_tesla_app.py"])