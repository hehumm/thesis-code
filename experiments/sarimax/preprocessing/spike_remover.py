import shared.preprocessing_general as preprocessing_general

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
    dfs = preprocessing_general.get_sites_with_data_wide()
    for site_id, df in dfs.items():
        spikes = _find_spikes_for_one_site(df, 'load_energy_sum', threshold=0.95)
        for index, row in spikes.iterrows():
            df.loc[index, 'load_energy_sum'] = None
        df = df.interpolate()
        dfs[site_id] = df
    return dfs