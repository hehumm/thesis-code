import os
from datetime import datetime
import pandas as pd
from skforecast.sarimax import Sarimax
from skforecast.recursive import ForecasterSarimax
import experiments.final.skforecast.hyperparams_tuner as tuner
import experiments.final.skforecast.sarimax_config as config
import experiments.final.preprocessed_data as preprocessed_data
import experiments.final.final_shared as final_shared
import shared.shared_utility as shared_utility

def _get_params_file_path():
    output_dir = '/home/henri/Code/thesis-code/sk_forecast_forecasts'
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, 'sarimax_params_finding_time_logs.txt')

def _generate_sarimax_orders(site, y, exog):
    output_file = _get_params_file_path()
    with open(output_file, 'a') as f:
        f.write(f'Best params search for site {site} started at {datetime.now()}\n')

    best_params = tuner.perform_grid_search(config.param_grids.get(site), y, exog)
    best_params.to_excel(f'best_params_{site}.xlsx')

    with open(output_file, 'a') as f:
        f.write(f'Best params search for site {site} ended at {datetime.now()}\n')

def _transform_data_to_sk_format(sites_main, sites_covariates):
    data = {}
    for site in shared_utility.sites:
        site_main = sites_main[site]
        site_covariates = sites_covariates[site]
        y = pd.Series(data=site_main.set_index('timestamp')['target']).asfreq('h')
        exog = site_covariates.set_index('timestamp').drop(columns=['item_id']).asfreq('h')
        data[site] = (y, exog)
    return data

def fit_predict():
    sites_main = preprocessed_data.get_sites_independent_dfs_only_main()
    sites_covariates = preprocessed_data.get_sites_independent_dfs_only_covariates()
    data = _transform_data_to_sk_format(sites_main, sites_covariates)

    for site in shared_utility.sites:
        pred_len = final_shared.configuration.get('prediction_length')
        y, exog = data.get(site)
        y_train = y[:-pred_len]
        exog_train = exog[:-pred_len]

        # _generate_sarimax_orders(site, y_train, exog_train)
        params = config.best_params.get(site)
        forecaster = ForecasterSarimax(
            regressor=Sarimax(order=params.get('order'), seasonal_order=params.get('seasonal_order'), maxiter=200)
        )
        forecaster.fit(y=y_train, exog=exog_train)
        exog_test = exog[-pred_len:]
        y_pred = forecaster.predict(steps=pred_len, exog=exog_test)
        y_pred.to_csv(f'/home/henri/Code/thesis-code/sk_forecast_forecasts/predictions_sarimax_{site}.csv')
