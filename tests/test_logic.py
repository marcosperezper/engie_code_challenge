import pytest
from schemas import ProductionRequest, Fuels, PowerPlant
from logic import compute_production_request


def test_compute_production_request():
    payload = ProductionRequest(
        load=480,
        fuels=Fuels(
            **{
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60
            }
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
    result = compute_production_request(payload)
    powers = [p.p for p in result]

    total_power = sum(powers)
    assert abs(total_power - payload.load) <= payload.load, \
        f"Total power {total_power} differs from load {payload.load}"

    # Optional: check each allocation is non-negative and respects pmax
    for pp, allocated in zip(payload.powerplants, powers):
        assert 0 <= allocated <= pp.pmax + 0.1