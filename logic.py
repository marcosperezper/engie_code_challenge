from typing import List

from schemas import ProductionRequest, ProductionResponse


def compute_production_request(request: ProductionRequest) -> List[ProductionResponse]:
    fuels = request.fuels
    load_remaining = request.load
    result_unsorted = []
    plan_costs = []

    # Calculate cost and availability for each plant
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

    # Sort by cost (cheapest first)
    plan_costs.sort(key=lambda x: x[1])

    # Allocate power
    for pp, cost, available in plan_costs:
        if load_remaining <= 0:
            result_unsorted.append(ProductionResponse(name=pp.name, p=0))
            continue

        p = min(available, load_remaining)

        # Force pmin if asignation is lower than 0
        if p < pp.pmin and p > 0:
            p = pp.pmin

        p = round(p, 1)
        load_remaining -= p

        result_unsorted.append(ProductionResponse(name=pp.name, p=p))

    # Adjust if overproduction
    if load_remaining < 0:
        excess = abs(load_remaining)

        reducible_plants = []
        for pp, cost, _ in plan_costs:
            allocation = next(r for r in result_unsorted if r.name == pp.name)
            if allocation.p > pp.pmin:
                reducible_plants.append((pp, cost, allocation))

        #Sort by cost (most expensive first)
        reducible_plants.sort(key=lambda x: x[1], reverse=True)

        # Reduce power from most expensive plant to delete overflow
        for pp, _, allocation in reducible_plants:
            if excess <= 0:
                break

            can_reduce = allocation.p - pp.pmin
            reduction = min(can_reduce, excess)

            allocation.p = round(allocation.p - reduction, 1)
            excess -= reduction

    # Reorder result to match with request
    result_ordered = []
    for pp in request.powerplants:
        allocation = next(r for r in result_unsorted if r.name == pp.name)
        result_ordered.append(allocation)

    return result_ordered
