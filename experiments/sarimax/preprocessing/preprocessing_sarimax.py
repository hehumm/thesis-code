import shared.preprocessing_general as preprocessing_general
from statsmodels.tsa.stattools import adfuller

# def get_sites_with_stationary_data():
#     dfs = preprocessing_general.get_sites_with_data_wide()
#     target_column = 'load_energy_sum'
#     forecast_horizon = 36

#     for site_id, df in dfs.items():
#         y = df[target_column]
#         y_train = y[:-forecast_horizon]
#         if site_id == 5:
#             y_train = y_train.diff().dropna()
#         result = adfuller(y_train)
#         print(f'Site {site_id} p-value: {result[1]}')

def get_sites_with_stationary_data():
    dfs = preprocessing_general.get_sites_with_data_wide()
    dfs[5] = dfs[5].diff().dropna()
    return dfs