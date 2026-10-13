"""Integration checks for the updated World3-03 model."""
import numpy as np
import pytest

from pyworld3 import World3
from pyworld3.specials import Smooth


def run_model(fast=False):
    world = World3()
    world.init_world3_constants()
    world.init_world3_variables()
    world.set_world3_table_functions()
    world.set_world3_delay_functions()
    world.run_world3(fast=fast)
    return world


def test_simulation_is_finite_and_fast_matches_checked():
    checked = run_model()
    fast = run_model(fast=True)
    for name in ("pop", "ppolx", "nr", "io", "al", "fpc", "hwi", "ef"):
        values = getattr(checked, name)
        assert values.shape == checked.time.shape
        assert np.isfinite(values).all(), name
        np.testing.assert_allclose(getattr(fast, name), values, rtol=1e-10)


@pytest.mark.parametrize("kwargs", [
    {"dt": 0}, {"dt": -1}, {"dt": float("nan")},
    {"year_max": 1800}, {"year_max": float("inf")}, {"dt": 0.3},
])
def test_invalid_time_parameters(kwargs):
    with pytest.raises(ValueError):
        World3(**kwargs)


def test_fractional_time_grid_and_verbose():
    world = World3(year_min=1900, year_max=1901, dt=0.1, verbose=True)
    assert world.n == len(world.time) == 11
    assert world.time[-1] == 1901
    assert world.verbose


def test_smooth_odeint_scalar_assignment():
    times = np.arange(3)
    smooth = Smooth(np.ones(3), 1, times, method="odeint")
    assert smooth(0, 2, 0) == 0
    assert smooth(1, 2, 0) == pytest.approx(1 - np.exp(-0.5))
