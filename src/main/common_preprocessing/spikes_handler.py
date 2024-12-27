import experiments.final.general.data_importer as data_importer

def _find_spikes_for_one_site(df, column, threshold=0.95):
    threshold_value = df[column].quantile(threshold)
    spikes = df[df[column] > threshold_value]
    return spikes[['load_energy_sum']]

def find_spikes(spike_threshold=0.95):
    dfs = data_importer.get_imported_data()
    spikes = {}
    for site_id, df in dfs.items():
        spike = _find_spikes_for_one_site(df, 'load_energy_sum', threshold=0.95)
        spikes[site_id] = spike
    return spikes

def get_sites_with_data_without_spikes(dfs):
    for site_id, df in dfs.items():
        spikes = _find_spikes_for_one_site(df, 'load_energy_sum', threshold=0.95)
        for index, row in spikes.iterrows():
            df.loc[index, 'load_energy_sum'] = None
        df = df.interpolate()
        dfs[site_id] = df
    return dfs