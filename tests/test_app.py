from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_production_plan_endpoint():
    payload = {
        "load": 480,
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60
        },
        "powerplants": [
            {"name": "gasfiredbig1", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
            {"name": "gasfiredbig2", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
            {"name": "gasfiredsomewhatsmaller", "type": "gasfired", "efficiency": 0.37, "pmin": 40, "pmax": 210},
            {"name": "tj1", "type": "turbojet", "efficiency": 0.3, "pmin": 0, "pmax": 16},
            {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150},
            {"name": "windpark2", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 36}
        ]
    }

    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    for item in data:
        assert "name" in item
        assert "p" in item
        assert item["p"] >= 0

    total_power = sum(item["p"] for item in data)
    assert abs(total_power - payload["load"]) < 1.0