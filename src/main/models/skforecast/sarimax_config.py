param_grids = {
    2: {
        'order': [(0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 1), (2, 0, 0), (2, 1, 1)],
        'seasonal_order': [(0, 0, 0, 0)]
    },
    4: {
        'order': [(0, 0, 0), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 0, 0), (2, 1, 0), (3, 0, 0)],
        'seasonal_order': [(0, 0, 0, 0), (1, 0, 1, 12), (1, 1, 1, 12), (2, 0, 1, 12)]
    },
    5: {
        'order': [(0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 1), (2, 0, 0)],
        'seasonal_order': [(0, 0, 0, 0)]
    },
    6: {
        'order': [(0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 1), (2, 0, 0)],
        'seasonal_order': [(0, 0, 0, 0)]
    },
    12: {
        'order': [(0, 0, 0), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 0, 0), (2, 1, 0), (3, 0, 0)],
        'seasonal_order': [(0, 0, 0, 0), (1, 0, 1, 12), (1, 1, 1, 12), (2, 0, 1, 12)]
    }
}

best_params = {
    2: {
        'order': (0, 1, 1),
        'seasonal_order': (0, 0, 0, 0)
    },
    4: {
        'order': (2, 1, 0),
        'seasonal_order': (0, 0, 0, 0)
    },
    5: {
        'order': (1, 1, 1),
        'seasonal_order': (0, 0, 0, 0)
    },
    6: {
        'order': (1, 0, 0),
        'seasonal_order': (0, 0, 0, 0)
    },
    12: {
        'order': (2, 1, 0),
        'seasonal_order': (2, 0, 1, 12)
    }
}