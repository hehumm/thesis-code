from itertools import product

site_parameters = {
    2: {
        "p_range": range(0, 2),
        "d_range": [0],
        "q_range": range(0, 3),
        "P_range": [0],
        "D_range": [0],
        "Q_range": [0],
    },
    4: {
        "p_range": range(0, 3),
        "d_range": [0],
        "q_range": range(0, 3),
        "P_range": range(1, 3),
        "D_range": range(0, 2),
        "Q_range": range(0, 2),
    },
    5: {
        "p_range": range(0, 2),
        "d_range": range(0, 2),
        "q_range": range(0, 3),
        "P_range": [0],
        "D_range": [0],
        "Q_range": [0],
    },
    6: {
        "p_range": range(0, 2),
        "d_range": [0],
        "q_range": range(0, 2),
        "P_range": [0],
        "D_range": [0],
        "Q_range": [0],
    },
    12: {
        "p_range": range(0, 3),
        "d_range": [0],
        "q_range": range(0, 3),
        "P_range": range(1, 3),
        "D_range": range(0, 2),
        "Q_range": range(0, 2),
    },
}

def get_param_grids():
    parameter_grids = {}
    for site, params in site_parameters.items():
        order_combinations = list(product(params["p_range"], params["d_range"], params["q_range"]))
        seasonal_order_combinations = list(product(params["P_range"], params["D_range"], params["Q_range"], [24]))
        parameter_grids[site] = {
            "order": order_combinations,
            "seasonal_order": seasonal_order_combinations,
        }
    return parameter_grids
