import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import shared.preprocessing_general as preprocessing_general
import experiments.sarimax.preprocessing_sarimax as preprocessing_sarimax

# # Generate ACF and PACF plots
# plt.figure(figsize=(12, 6))
# plt.subplot(121)
# plot_acf(y_train, lags=50, ax=plt.gca())  # Autocorrelation function
# plt.title('ACF')

# plt.subplot(122)
# plot_pacf(y_train, lags=50, ax=plt.gca(), method='ywm')  # Partial autocorrelation
# plt.title('PACF')

# plt.tight_layout()
# plt.show()

#dfs = preprocessing_general.get_sites_with_data_wide()
dfs = preprocessing_sarimax.get_sites_with_stationary_data()
target_column = 'load_energy_sum'
forecast_horizon = 36

for site_id, df in dfs.items():
    y = df[target_column]
    y_train = y[:-forecast_horizon]
    
    # Generate ACF and PACF plots
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plot_acf(y_train, lags=50, ax=plt.gca())  # Autocorrelation function
    plt.title(f'Site {site_id} ACF')

    plt.subplot(122)
    plot_pacf(y_train, lags=50, ax=plt.gca(), method='ywm')  # Partial autocorrelation
    plt.title(f'Site {site_id} PACF')

    plt.tight_layout()
    plt.show()