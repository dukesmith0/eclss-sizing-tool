"""Tests for EclssSystem hardware model."""

import pytest
from eclss.system import EclssSystem


class TestDefaults:
    def test_default_unlimited(self):
        sys = EclssSystem()
        assert sys.o2_generation_capacity_kg_hr is None
        assert sys.co2_removal_capacity_kg_hr is None
        assert sys.heat_rejection_capacity_w is None

    def test_default_water_recovery(self):
        assert EclssSystem().water_recovery_efficiency == 0.93

    def test_iss_bpa_water_recovery(self):
        from eclss.constants import WATER_RECOVERY_EFFICIENCY_ISS_BPA
        sys = EclssSystem(water_recovery_efficiency=WATER_RECOVERY_EFFICIENCY_ISS_BPA)
        assert sys.water_recovery_efficiency == 0.98

    def test_frozen(self):
        with pytest.raises(AttributeError):
            EclssSystem().o2_generation_capacity_kg_hr = 0.5

    def test_unlimited_classmethod(self):
        sys = EclssSystem.unlimited()
        assert sys.o2_generation_capacity_kg_hr is None
        assert sys.co2_removal_capacity_kg_hr is None

    def test_zero_classmethod(self):
        sys = EclssSystem.zero()
        assert sys.o2_generation_capacity_kg_hr == 0.0
        assert sys.co2_removal_capacity_kg_hr == 0.0
        assert sys.heat_rejection_capacity_w == 0.0
        assert sys.water_recovery_efficiency == 0.0

    def test_zero_cannot_meet_any_demand(self):
        sys = EclssSystem.zero()
        assert sys.can_meet_o2_demand(0.01) is False
        assert sys.can_meet_co2_demand(0.01) is False
        assert sys.can_meet_thermal_demand(1.0) is False


class TestEffectiveRates:
    def test_unlimited_returns_demand(self):
        sys = EclssSystem()
        assert sys.effective_o2_rate(0.5) == pytest.approx(0.5)
        assert sys.effective_co2_rate(1.0) == pytest.approx(1.0)
        assert sys.effective_heat_rate(5000) == pytest.approx(5000)

    def test_capped_at_capacity(self):
        sys = EclssSystem(o2_generation_capacity_kg_hr=0.2)
        assert sys.effective_o2_rate(0.5) == pytest.approx(0.2)

    def test_under_capacity_returns_demand(self):
        sys = EclssSystem(o2_generation_capacity_kg_hr=0.2)
        assert sys.effective_o2_rate(0.1) == pytest.approx(0.1)

    def test_exact_capacity(self):
        sys = EclssSystem(co2_removal_capacity_kg_hr=0.3)
        assert sys.effective_co2_rate(0.3) == pytest.approx(0.3)

    def test_zero_returns_zero(self):
        sys = EclssSystem.zero()
        assert sys.effective_o2_rate(0.5) == pytest.approx(0.0)


class TestCanMeetDemand:
    def test_unlimited_always_meets(self):
        sys = EclssSystem()
        assert sys.can_meet_o2_demand(999.0) is True
        assert sys.can_meet_co2_demand(999.0) is True
        assert sys.can_meet_thermal_demand(999999.0) is True

    def test_adequate_capacity(self):
        sys = EclssSystem(o2_generation_capacity_kg_hr=0.5)
        assert sys.can_meet_o2_demand(0.3) is True

    def test_undersized(self):
        sys = EclssSystem(o2_generation_capacity_kg_hr=0.2)
        assert sys.can_meet_o2_demand(0.5) is False

    def test_thermal_undersized(self):
        sys = EclssSystem(heat_rejection_capacity_w=5000)
        assert sys.can_meet_thermal_demand(8000) is False


class TestRepr:
    def test_repr_shows_capacities(self):
        sys = EclssSystem(o2_generation_capacity_kg_hr=0.2, co2_removal_capacity_kg_hr=0.3)
        r = repr(sys)
        assert "0.2" in r
        assert "0.3" in r

    def test_repr_unlimited(self):
        assert "unlimited" in repr(EclssSystem())

    def test_repr_zero(self):
        assert "=0" in repr(EclssSystem.zero())
