import pytest

from src.bending_stress import total_area, centroidal_coords, sec_mom_area

@pytest.fixture
def example_section():
    return ([
        {'b': 120.0, 'h': 8.0, 'area': 960.0, 'x_prime': 24.0, 'y_prime': -4.0}, 
        {'b': 8.0, 'h': 80.0, 'area': 640.0, 'x_prime': 4.0, 'y_prime': -48.0}
    ])

def test_area(example_section):
    assert total_area(example_section) == 1600

def test_xy_bar(example_section):
    assert centroidal_coords(example_section, total_area(example_section)) == (16, -21.6)

def test_I(example_section):
    x_bar, y_bar = centroidal_coords(example_section, total_area(example_section))
    assert sec_mom_area(example_section, x_bar, y_bar) == (pytest.approx(1089877.33), pytest.approx(1309013.33), pytest.approx(337920.0))