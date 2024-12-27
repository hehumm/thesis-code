import os
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error, root_mean_squared_error
import src.main.general.results_dataset_generator as results_dataset_generator
import src.main.general.shared_variables as shared_variables

def generate_metrics():
    metrics_dir = f'{shared_variables.repo_path}/metrics'
    if not os.path.exists(metrics_dir):
        os.makedirs(metrics_dir)

    data = results_dataset_generator.get_summary()
    for site in shared_variables.sites_ids:
        values = data[site]
        measured_data = values['actual']['target'][-(shared_variables.configuration.get('prediction_length')):]
        metrics_data = {
            "Model": ["Theta", "AutoARIMA", "Chronos", "SARIMAX", "LSTM"],
            "MAPE": [
                mean_absolute_percentage_error(measured_data, values['Theta']['mean']),
                mean_absolute_percentage_error(measured_data, values['AutoARIMA']['mean']),
                mean_absolute_percentage_error(measured_data, values['Chronos']['mean']),
                mean_absolute_percentage_error(measured_data, values['SARIMAX']['mean']),
                mean_absolute_percentage_error(measured_data, values['LSTM']['mean']),
            ],
            "MAE": [
                mean_absolute_error(measured_data, values['Theta']['mean']),
                mean_absolute_error(measured_data, values['AutoARIMA']['mean']),
                mean_absolute_error(measured_data, values['Chronos']['mean']),
                mean_absolute_error(measured_data, values['SARIMAX']['mean']),
                mean_absolute_error(measured_data, values['LSTM']['mean']),
            ],
            "RMSE": [
                root_mean_squared_error(measured_data, values['Theta']['mean']),
                root_mean_squared_error(measured_data, values['AutoARIMA']['mean']),
                root_mean_squared_error(measured_data, values['Chronos']['mean']),
                root_mean_squared_error(measured_data, values['SARIMAX']['mean']),
                root_mean_squared_error(measured_data, values['LSTM']['mean']),
            ],
        }
        pd.DataFrame(metrics_data).to_excel(f'{metrics_dir}/metrics_site_{site}.xlsx')
