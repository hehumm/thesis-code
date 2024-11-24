import os
import experiments.sarimax.utility as utility
from statsmodels.tsa.statespace.sarimax import SARIMAX

def get_forecast(site_id, params_version, train_dfs, test_dfs):
    output_dir = '/home/henri/Code/thesis-code/experiments/sarimax/forecasts'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'forecast_site_{site_id}_params_{params_version}.csv')
    
    model = SARIMAX(train_dfs.get(site_id)['load_energy_sum'], 
                    order=utility.model_params[site_id][params_version]['order'], 
                    seasonal_order=utility.model_params[site_id][params_version]['seasonal_order'],
                    exog=train_dfs.get(site_id)[utility.exog_columns])

    results = model.fit()
    forecast = results.get_forecast(steps=36, exog=test_dfs.get(site_id)[utility.exog_columns])
    
    forecast_values = forecast.predicted_mean
    forecast_values.to_csv(output_file)

    forecast_ci = forecast.conf_int()
    return forecast_values, forecast_ci