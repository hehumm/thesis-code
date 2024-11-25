import shared.preprocessing_general as preprocessing_general
import experiments.sarimax.preprocessing.preprocessing_sarimax as preprocessing_sarimax
import experiments.sarimax.utility as utility
import experiments.sarimax.forecasting as forecasting

dfs = preprocessing_general.get_sites_with_data_wide()
dfs = preprocessing_general.convert_all_dfs_targets_to_megawatt_hours(dfs, 'load_energy_sum')
dfs = preprocessing_sarimax.standardize_exog_data(dfs)
train_dfs, test_dfs = preprocessing_sarimax.test_train_split(dfs)
train_dfs = preprocessing_sarimax.get_sites_with_data_without_spikes(train_dfs)

# import shared.data_overview_plots as data_overview_plots
# data_overview_plots.plot_acf_pacf(train_dfs)

#preprocessing_sarimax.perform_grid_search(train_dfs)
#preprocessing_sarimax.perform_random_search(train_dfs)
#preprocessing_sarimax.perform_halving_random_search(train_dfs)

for site_id in train_dfs.keys():
    for params_version in utility.model_params[site_id].keys():
        forecast_values, forecast_ci = forecasting.get_forecast(site_id, params_version, train_dfs, test_dfs)

# import matplotlib.pyplot as plt
# plt.figure(figsize=(24, 12))
# plt.plot(train_dfs.get(2)['load_energy_sum'], label='train')
# plt.plot(test_dfs.get(2)['load_energy_sum'], label='test')
# plt.plot(forecast_values, label='forecast')
# plt.fill_between(forecast_ci.index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='k', alpha=0.2)
# plt.legend()
# plt.show()
