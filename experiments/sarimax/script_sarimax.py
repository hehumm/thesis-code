import shared.preprocessing_general as preprocessing_general
import experiments.sarimax.preprocessing.preprocessing_sarimax as preprocessing_sarimax

dfs = preprocessing_general.get_sites_with_data_wide()
dfs = preprocessing_sarimax.convert_target_to_megawatt_hours(dfs)
dfs = preprocessing_sarimax.standardize_exog_data(dfs)
train_dfs, test_dfs = preprocessing_sarimax.test_train_split(dfs)
train_dfs = preprocessing_sarimax.get_sites_with_data_without_spikes(train_dfs)

# import shared.data_overview_plots as data_overview_plots
# data_overview_plots.plot_acf_pacf(train_dfs)

preprocessing_sarimax.perform_grid_search(train_dfs)