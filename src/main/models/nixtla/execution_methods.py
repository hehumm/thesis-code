import os
from datetime import datetime
from neuralforecast import NeuralForecast
from neuralforecast.models import LSTM
from neuralforecast.losses.pytorch import MAPE
import src.main.general.data_importer as data_importer
import src.main.general.shared_variables as shared_variables

def _get_nixtla_main_dfs_with_covariates():
    default_main_with_covariates = data_importer.get_imported_data()
    sites_main_with_covariates = {}
    for site, df in default_main_with_covariates.items():
        sites_main_with_covariates[site] = df.rename(columns={'start_time': 'ds', 'load_energy_sum': 'y', 'site_id': 'unique_id'})
    return sites_main_with_covariates

def fit_predict():
    output_dir = shared_variables.nixtla_forecasts_path
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'nixtla_time_logs.txt')

    sites_main_with_covariates = _get_nixtla_main_dfs_with_covariates()

    for site in shared_variables.sites_ids:
        with open(output_file, 'a') as f:
            f.write(f'Fitting and predicting for site {site} started at {datetime.now()}\n')

        pred_len = shared_variables.configuration.get('prediction_length')
        df = sites_main_with_covariates.get(site)
        df_train = df[:-pred_len]
        nf = NeuralForecast(
            models=[
                LSTM(
                    h=shared_variables.configuration['prediction_length'],
                    loss=MAPE(),
                    futr_exog_list=shared_variables.configuration['known_covariates_names'],
                    scaler_type='standard', # maybe standardize the data earlier in the pipeline
                )
            ],
            freq='h'
        )
        nf.fit(df_train)
        exog_test = df[-pred_len:].drop(columns=['y'])
        y_pred = nf.predict(futr_df=exog_test)

        y_pred.to_csv(f'{output_dir}/predictions_lstm_{site}.csv')

        with open(output_file, 'a') as f:
            f.write(f'Fitting and predicting for site {site} ended at {datetime.now()}\n')
            