import pytest
import metallurgy as mg


def test_price():
    assert mg.price.price("Cu") == 6.0
    assert mg.price.price("Cu50Zr50") == pytest.approx(24.330854816824964)
