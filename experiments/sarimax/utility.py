variations = ['random_search', 'halving_random_search']

exog_columns = ['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage']

# provided by an external party
initial_model_params = {
    'order': (2, 0, 0),
    'seasonal_order': (2, 1, 1, 24)
}

# These values come from running random and halving random searches on the training data.
model_params = {
    2: {
        'random_search': {
            'trend': 'c',
            'seasonal_order': (2, 1, 1, 12),
            'order': (0, 0, 2),
        },
    },
    4: {
        'random_search': {
            'trend': 'c',
            'seasonal_order': (1, 1, 1, 12),
            'order': (0, 0, 1),
        },
    },
    5: {
        'random_search': {
            'trend': 'c',
            'seasonal_order': (0, 0, 0, 12),
            'order': (2, 1, 1),
        },
    },
    6: {
        'random_search': {
            'trend': 'c',
            'seasonal_order': (0, 1, 2, 12),
            'order': (0, 0, 1),
        },
    },
    12: {
        'random_search': {
            'trend': 'c',
            'seasonal_order': (0, 1, 2, 24),
            'order': (1, 1, 2),
        },
    },
}
