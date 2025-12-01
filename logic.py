from typing import List

from schemas import ProductionRequest, ProductionResponse


def compute_production_request(request: ProductionRequest) -> List[ProductionResponse]:
    fuels = request.fuels
    load_remainig = request.load
    result_unsorted = []

    plan_costs = []

    for pp in request.powerplants:
        if pp.type == "windturbine":
            cost = 0
            available = pp.pmax * fuels.wind_percentage / 100

        elif pp.type == "gasfired":
            cost = fuels.gas_euro_mwh / pp.efficiency
            available = pp.pmax
        elif pp.type == "turbojet":
            cost = fuels.kerosine_euro_mwh / pp.efficiency
            available = pp.pmax
        else:
            continue

        plan_costs.append((pp, cost, available))

    # sort by cost (cheapest first)
    plan_costs.sort(key=lambda x: x[1])

    # allocate power
    for pp, _, available in plan_costs:
        if load_remainig <= 0:
            result_unsorted.append(ProductionResponse(name=pp.name, p=0))

        p = min(available, load_remainig)

        if p < pp.pmin and load_remainig > 0:
            p = pp.pmin

        p = round(p, 1)
        load_remainig -= p

        result_unsorted.append(ProductionResponse(name=pp.name, p=p))

    # reorder result to match input order

    result_ordered = []
    for pp in request.powerplants:
        allocation = next(r for r in result_unsorted if r.name == pp.name)
        result_ordered.append(allocation)

    return result_ordered
