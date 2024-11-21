# Results:
# Site 2 p-value: 3.71992023593113e-05
# Site 4 p-value: 3.6861127208643487e-07
# Site 5 p-value: 0.04892466276070679
# Site 6 p-value: 4.590613764947615e-19
# Site 12 p-value: 1.7999520769225346e-06
#
# All the sites have stationary data

import shared.preprocessing_general as preprocessing_general
from statsmodels.tsa.stattools import adfuller

# If p-value > 0.05, the series is non-stationary and requires differencing
# If p-value <= 0.05, the series is stationary and does not require differencing

dfs = preprocessing_general.get_sites_with_data_wide()
target_column = 'load_energy_sum'
forecast_horizon = 36

for site_id, df in dfs.items():
    y = df[target_column]
    y_train = y[:-forecast_horizon]
    if site_id == 5:
        y_train = y_train.diff().dropna()
    result = adfuller(y_train)
    print(f'Site {site_id} p-value: {result[1]}')