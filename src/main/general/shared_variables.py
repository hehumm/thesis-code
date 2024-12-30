repo_path = '/home/henri/Code/thesis-code/'

sites_ids = [2, 4, 5, 6, 12]

configuration = {
    'prediction_length': 36,
    'known_covariates_names': ['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage'],
    'eval_metric': 'MAPE',
    'time_limit': 300,
}

ag_model_names = ['Theta', 'AutoARIMA',
                  'ChronosFineTunedWithRegressor[bolt_base]']
ag_forecasts_path = f'{repo_path}final_results/autogluon'

skforecast_forecasts_path = f'{repo_path}final_results/skforecast'

mlforecast_forecasts_path = f'{repo_path}final_results/mlforecast'