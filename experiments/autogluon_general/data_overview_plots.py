import matplotlib.pyplot as plt
import shared.preprocessing_general as preprocessing_general
import experiments.sarimax.preprocessing.spike_remover as spike_remover

original_dfs = preprocessing_general.get_sites_with_data_wide()
all_sites_spikes = spike_remover.find_spikes()

def plot_vanilla_data():

    for site_id, df in original_dfs.items():
        plt.figure(figsize=(24, 12))
        plt.plot(df['load_energy_sum'])
        plt.title(f'Site {site_id}')
        plt.ylabel('Electricity Consumption (mWh)')
    plt.show()

def plot_spikes():
    for site_id, spike in all_sites_spikes.items():
        plt.figure(figsize=(24, 12))
        plt.plot(original_dfs[site_id]['load_energy_sum'], label='Original')
        plt.plot(spike['load_energy_sum'], label='Spikes')
        plt.title(f'Site {site_id}')
        plt.ylabel('Electricity Consumption (mWh)')
        plt.legend(loc='upper left')
        plt.show()

plot_vanilla_data()
plot_spikes()