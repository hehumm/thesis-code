import pandas as pd
import numpy as np
import shared.preprocessing_general as preprocessing_general
import matplotlib.pyplot as plt

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

global_spikes = find_spikes()
dfs = preprocessing_general.get_sites_with_data_wide()

for site_id, spike in global_spikes.items():
    plt.figure(figsize=(24, 12))
    plt.plot(dfs[site_id]['load_energy_sum'], label='Original')
    plt.plot(spike['load_energy_sum'], label='Spikes')
    plt.title(f'Site {site_id}')
    plt.ylabel('Electricity Consumption (mWh)')
    plt.legend(loc='upper left')
    plt.show() 
