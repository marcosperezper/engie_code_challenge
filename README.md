# Engie Code Challenge – Production Plan API

## Project Overview

This project is a **FastAPI REST API** that computes a **production plan** for powerplants based on a requested load and fuel costs.  

---

## Installation

1. Clone the repository:

```
git clone https://github.com/marcosperezper/engie_code_challenge
cd engie_code_challenge
```

2. Create a Python virutal environment:
```
# macOS/Linux
python -m venv .venv
source .venv/bin/activate

# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```
pip install -r requirements.txt
```
---
## Running the App
```commandline
docker compose build
docker compose up
```
The server runs at http://127.0.0.1:8000/

Swagger UI / Docs: http://127.0.0.1:8000/docs

---
## Example Request
POST to /productionplan with JSON payload:

```json
{
  "load": 480,
  "fuels": {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [
    {"name":"gasfiredbig1","type":"gasfired","efficiency":0.53,"pmin":100,"pmax":460},
    {"name":"windpark1","type":"windturbine","efficiency":1,"pmin":0,"pmax":150}
  ]
}
```

Response:
```json
[
  {
    "name": "gasfiredbig1",
    "p": 390
  },
  {
    "name": "windpark1",
    "p": 90
  }
]
```
---
## Testing
All tests are in the tests/ folder.

To run the tests run this command:
```commandline
pytest -v tests/
```