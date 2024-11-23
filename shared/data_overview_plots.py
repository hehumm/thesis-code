
import matplotlib.pyplot as plt
import shared.preprocessing_general as preprocessing_general
import experiments.sarimax.preprocessing.preprocessing_sarimax as preprocessing_sarimax
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

original_dfs = preprocessing_general.get_sites_with_data_wide()
all_sites_spikes = preprocessing_sarimax.find_spikes()

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

def plot_interpolated_data():
    interpolated_dfs = preprocessing_sarimax.get_sites_with_data_without_spikes(original_dfs)
    for site_id, df in interpolated_dfs.items():
        plt.figure(figsize=(24, 12))
        plt.plot(df['load_energy_sum'])
        plt.title(f'Site {site_id} without spikes')
        plt.ylabel('Electricity Consumption (mWh)')
    plt.show()

def plot_acf_pacf(dfs):
    for site_id, df in dfs.items():
        y = df['load_energy_sum']

        plt.figure(figsize=(12, 6))
        plt.subplot(121)
        plot_acf(y, lags=50, ax=plt.gca())
        plt.title(f'Site {site_id} ACF')

        plt.subplot(122)
        plot_pacf(y, lags=50, ax=plt.gca(), method='ywm')
        plt.title(f'Site {site_id} PACF')

        plt.tight_layout()
        plt.show()

def plot_exog_data():
    for site_id, df in original_dfs.items():

        plt.figure(figsize=(24, 12))
        plt.plot(df['buy_price_kwh'])
        plt.title(f'Site {site_id} buy price')
        plt.ylabel('Buy price in cents*100 for 1kWh')
        plt.show()

        plt.figure(figsize=(24, 12))
        plt.plot(df['sell_price_kwh'])
        plt.title(f'Site {site_id} sell price')
        plt.ylabel('Sell price in cents*100 for 1kWh')
        plt.show()

        plt.figure(figsize=(24, 12))
        plt.plot(df['temp'])
        plt.title(f'Site {site_id} temp')
        plt.ylabel('Temperature (C)')
        plt.show()

        plt.figure(figsize=(24, 12))
        plt.plot(df['feels_like'])
        plt.title(f'Site {site_id} feels like')
        plt.ylabel('Feels like (C)')
        plt.show()

        plt.figure(figsize=(24, 12))
        plt.plot(df['pop'])
        plt.title(f'Site {site_id} probability of precipitation')
        plt.ylabel('Probability of precipitation')
        plt.show()

        plt.figure(figsize=(24, 12))
        plt.plot(df['clouds'])
        plt.title(f'Site {site_id} clouds')
        plt.ylabel('Clouds (%)')
        plt.show()

        plt.figure(figsize=(24, 12))
        plt.plot(df['sun_percentage'])
        plt.title(f'Site {site_id} sun percentage')
        plt.ylabel('Sun percentage (%)')
        plt.show()

#plot_vanilla_data()
#plot_spikes()
#plot_interpolated_data()

#sites_wo_spikes = preprocessing_sarimax.get_sites_with_data_without_spikes(original_dfs)
#sites_wo_spikes = preprocessing_sarimax.get_sites_with_stationary_data(sites_wo_spikes)
#training_dfs, _ = preprocessing_sarimax.test_train_split(sites_wo_spikes)
#plot_acf_pacf(training_dfs)

#plot_exog_data()