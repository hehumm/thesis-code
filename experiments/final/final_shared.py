configuration = {
    'prediction_length': 24,
    'known_covariates_names': ['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage'],
    'eval_metric': 'RMSE',
    'time_limit': 300,
}

ag_model_names = ['Theta', 'ETS', 'AutoARIMA', 'Chronos[bolt_tiny]']

ag_forecasts_path = '/home/henri/Code/thesis-code/autogluon_forecasts'