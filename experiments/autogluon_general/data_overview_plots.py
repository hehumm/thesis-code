import matplotlib.pyplot as plt
import shared.preprocessing_general as preprocessing_general

dfs = preprocessing_general.get_sites_with_data_wide()

for site_id, df in dfs.items():
    plt.figure(figsize=(24, 12))
    plt.plot(df['load_energy_sum'])
    plt.title(f'Site {site_id}')
    plt.ylabel('Electricity Consumption (mWh)')
    plt.show()