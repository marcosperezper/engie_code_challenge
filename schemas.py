from typing import List

from pydantic import BaseModel, Field, ConfigDict


class PowerPlant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float


class Fuels(BaseModel):
    gas_euro_mwh: float = Field(..., alias="gas(euro/MWh)")
    kerosine_euro_mwh: float = Field(..., alias="kerosine(euro/MWh)")
    co2_euro_ton: float = Field(..., alias="co2(euro/ton)")
    wind_percentage: float = Field(..., alias="wind(%)")

    model_config = ConfigDict(validate_by_name=True)


class ProductionRequest(BaseModel):
    load: float
    fuels: Fuels
    powerplants: List[PowerPlant]


class ProductionResponse(BaseModel):
    name: str
    p: float
