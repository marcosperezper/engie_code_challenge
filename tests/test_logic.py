import pytest
from schemas import ProductionRequest, Fuels, PowerPlant
from logic import compute_production_request

@pytest.fixture
def payload_wind_60():
    return ProductionRequest(
        load=480,
        fuels=Fuels(
            gas_euro_mwh=13.4,
            kerosine_euro_mwh=50.8,
            co2_euro_ton=20,
            wind_percentage=60
        ),
        powerplants=[
            PowerPlant(name="gasfiredbig1", type="gasfired", efficiency=0.53, pmin=100, pmax=460),
            PowerPlant(name="gasfiredbig2", type="gasfired", efficiency=0.53, pmin=100, pmax=460),
            PowerPlant(name="gasfiredsomewhatsmaller", type="gasfired", efficiency=0.37, pmin=40, pmax=210),
            PowerPlant(name="tj1", type="turbojet", efficiency=0.3, pmin=0, pmax=16),
            PowerPlant(name="windpark1", type="windturbine", efficiency=1, pmin=0, pmax=150),
            PowerPlant(name="windpark2", type="windturbine", efficiency=1, pmin=0, pmax=36),
        ]
    )

def test_compute_wind_60(payload_wind_60):
    result = compute_production_request(payload_wind_60)
    total = round(sum(r.p for r in result), 1)
    assert total == 480
    # Optionally, check wind production is correct
    wind_total = sum(r.p for r in result if "windpark" in r.name)
    assert round(wind_total, 1) == round(150*0.6 + 36*0.6, 1)


@pytest.fixture
def payload_wind_0():
    return ProductionRequest(
        load=480,
        fuels=Fuels(
            gas_euro_mwh=13.4,
            kerosine_euro_mwh=50.8,
            co2_euro_ton=20,
            wind_percentage=0
        ),
        powerplants=[
            PowerPlant(name="gasfiredbig1", type="gasfired", efficiency=0.53, pmin=100, pmax=460),
            PowerPlant(name="gasfiredbig2", type="gasfired", efficiency=0.53, pmin=100, pmax=460),
            PowerPlant(name="gasfiredsomewhatsmaller", type="gasfired", efficiency=0.37, pmin=40, pmax=210),
            PowerPlant(name="tj1", type="turbojet", efficiency=0.3, pmin=0, pmax=16),
            PowerPlant(name="windpark1", type="windturbine", efficiency=1, pmin=0, pmax=150),
            PowerPlant(name="windpark2", type="windturbine", efficiency=1, pmin=0, pmax=36),
        ]
    )

def test_compute_wind_0(payload_wind_0):
    result = compute_production_request(payload_wind_0)
    total = round(sum(r.p for r in result), 1)
    assert total == 480
    wind_total = sum(r.p for r in result if "windpark" in r.name)
    assert wind_total == 0.0
