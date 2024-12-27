import os
from datetime import datetime
import pandas as pd
from skforecast.sarimax import Sarimax
from skforecast.recursive import ForecasterSarimax
from statsmodels.tsa.stattools import adfuller
import src.main.models.skforecast.hyperparams_tuner as tuner
import src.main.models.skforecast.sarimax_config as config
import src.main.general.shared_variables as shared_variables
import src.main.general.data_importer as data_importer

def test_sites_for_stationarity(dfs):
    forecast_horizon = 36
    for site_id, df in dfs.items():
        y = df['load_energy_sum']
        y_train = y[:-forecast_horizon]
        result = adfuller(y_train)
        print(f'Site {site_id} p-value: {result[1]}')

def _get_params_file_path():
    output_dir = f'{shared_variables.repo_path}sk_forecast_forecasts'
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

def _get_sk_formatted_data():
    preprocessed_data = data_importer.get_imported_data()
    sites_main = {site: df[['start_time', 'site_id', 'load_energy_sum']] for site, df in preprocessed_data.items()}
    sites_covariates = {site: df[['start_time', 'site_id', 'sun_percentage', 'buy_price_kwh', 'feels_like', 'sell_price_kwh', 'clouds', 'temp', 'pop']] for site, df in preprocessed_data.items()}
    data = {}
    for site in shared_variables.sites_ids:
        site_main = sites_main[site]
        site_covariates = sites_covariates[site]
        y = pd.Series(data=site_main.set_index('start_time')['load_energy_sum']).asfreq('h')
        exog = site_covariates.set_index('start_time').drop(columns=['item_id']).asfreq('h')
        data[site] = (y, exog)
    return data

def fit_predict():
    data = _get_sk_formatted_data()

    for site in shared_variables.sites_ids:
        pred_len = shared_variables.configuration.get('prediction_length')
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
        y_pred.to_csv(f'{shared_variables.repo_path}sk_forecast_forecasts/predictions_sarimax_{site}.csv')
