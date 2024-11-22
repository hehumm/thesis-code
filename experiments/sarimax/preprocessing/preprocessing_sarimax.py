import shared.preprocessing_general as preprocessing_general
from statsmodels.tsa.stattools import adfuller

def _find_spikes_for_one_site(df, column, threshold=0.95):
    threshold_value = df[column].quantile(threshold)
    spikes = df[df[column] > threshold_value]
    return spikes[['load_energy_sum']]

def find_spikes(spike_threshold=0.95):
    dfs = preprocessing_general.get_sites_with_data_wide()
    spikes = {}
    for site_id, df in dfs.items():
        spike = _find_spikes_for_one_site(df, 'load_energy_sum', threshold=0.95)
        spikes[site_id] = spike
    return spikes

def replace_spikes_with_interpolated_values():
    dfs = 'load_energy_sum'
    for site_id, df in dfs.items():
        spikes = _find_spikes_for_one_site(df, 'load_energy_sum', threshold=0.95)
        for index, row in spikes.iterrows():
            df.loc[index, 'load_energy_sum'] = None
        df = df.interpolate()
        dfs[site_id] = df
    return dfs

def test_sites_for_stationarity(dfs):
    forecast_horizon = 36
    for site_id, df in dfs.items():
        y = df['load_energy_sum']
        y_train = y[:-forecast_horizon]
        result = adfuller(y_train)
        print(f'Site {site_id} p-value: {result[1]}')

def get_sites_with_stationary_data():
    dfs = preprocessing_general.get_sites_with_data_wide()
    dfs[5] = dfs[5].diff().dropna()
    return dfs
