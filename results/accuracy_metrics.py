import shared.preprocessing_general as preprocessing_general
import experiments.sarimax.utility as utility
import shared.shared_utility as shared_utility
import pandas as pd
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

#measuring MAE, RMSE, WAPE and maybe sMAPE

dfs = preprocessing_general.get_sites_with_data_wide()
dfs = preprocessing_general.convert_all_dfs_targets_to_megawatt_hours(dfs, 'load_energy_sum')

def calculate_metrics_for_site(site_id):

    results_r_path = f'/home/henri/Code/thesis-code/experiments/sarimax/forecasts/forecast_site_{site_id}_params_random_search.csv'
    sarimax_results_r = pd.read_csv(results_r_path)
    sarimax_results_r.rename(columns={'Unnamed: 0': 'timestamp', 'predicted_mean': 'mean'}, inplace=True)
    
    # results_hr_path = f'/home/henri/Code/thesis-code/experiments/sarimax/forecasts/forecast_site_{site_id}_params_halving_random_search.csv'
    # sarimax_results_hr = pd.read_csv(results_hr_path)
    # sarimax_results_hr.rename(columns={'Unnamed: 0': 'timestamp', 'predicted_mean': 'mean'}, inplace=True)
    
    results_autoarima_path = f'/home/henri/documents/thesis/experiments_results/rmse/models/others/separate_exog/{site_id}/predictions_2.csv'
    autoarima_results = pd.read_csv(results_autoarima_path)
    # autoarima_results = preprocessing_general.convert_one_dfs_target_to_megawatt_hours(autoarima_results, 'mean')
    
    results_chronos_path = f'/home/henri/documents/thesis/experiments_results/rmse/models/chronos/separate_exog/{site_id}/predictions_1.csv'
    chronos_results = pd.read_csv(results_chronos_path)
    # chronos_results = preprocessing_general.convert_one_dfs_target_to_megawatt_hours(chronos_results, 'mean')

    mae_sarimax_r = mean_absolute_error(sarimax_results_r['mean'], dfs[site_id]['load_energy_sum'][-36:])
    #mae_sarimax_hr = mean_absolute_error(sarimax_results_hr['mean'], dfs[site_id]['load_energy_sum'][-36:])
    mae_autoarima = mean_absolute_error(autoarima_results['mean'], dfs[site_id]['load_energy_sum'][-36:])
    mae_chronos = mean_absolute_error(chronos_results['mean'], dfs[site_id]['load_energy_sum'][-36:])

    rmse_sarimax_r = root_mean_squared_error(sarimax_results_r['mean'], dfs[site_id]['load_energy_sum'][-36:])
    #rmse_sarimax_hr = root_mean_squared_error(sarimax_results_hr['mean'], dfs[site_id]['load_energy_sum'][-36:])
    rmse_autoarima = root_mean_squared_error(autoarima_results['mean'], dfs[site_id]['load_energy_sum'][-36:])
    rmse_chronos = root_mean_squared_error(chronos_results['mean'], dfs[site_id]['load_energy_sum'][-36:])

    wape_sarimax_r = shared_utility.wape(sarimax_results_r['mean'], dfs[site_id]['load_energy_sum'][-36:])
    #wape_sarimax_hr = shared_utility.wape(sarimax_results_hr['mean'], dfs[site_id]['load_energy_sum'][-36:])
    wape_autoarima = shared_utility.wape(autoarima_results['mean'], dfs[site_id]['load_energy_sum'][-36:])
    wape_chronos = shared_utility.wape(chronos_results['mean'], dfs[site_id]['load_energy_sum'][-36:])

    metrics_df = pd.DataFrame(columns=['site', 'model', 'mae', 'rmse', 'wape'])
    metrics_df.loc[0] = {'site': site_id, 'model': 'SARIMAX Random Search', 'mae': mae_sarimax_r, 'rmse': rmse_sarimax_r, 'wape': wape_sarimax_r}
    metrics_df.loc[1] = {'site': site_id, 'model': 'AutoARIMA', 'mae': mae_autoarima, 'rmse': rmse_autoarima, 'wape': wape_autoarima}
    metrics_df.loc[2] = {'site': site_id, 'model': 'Chronos', 'mae': mae_chronos, 'rmse': rmse_chronos, 'wape': wape_chronos}
    # metrics_df.loc[3] = {'site': site_id, 'model': 'SARIMAX Halving Random Search', 'mae': mae_sarimax_hr, 'rmse': rmse_sarimax_hr, 'wape': wape_sarimax_hr}

    return metrics_df

metrics_df = pd.DataFrame()
for site in shared_utility.sites:
    metrics_df = pd.concat([metrics_df, calculate_metrics_for_site(site)])
metrics_df

"""
   site                          model       mae      rmse      wape
0     2          SARIMAX Random Search  0.503018  0.715403  0.374606
1     2  SARIMAX Halving Random Search  0.496818  0.693871  0.363910
2     2                      AutoARIMA  1.177017  1.355828  2.516028
3     2                        Chronos  0.563650  0.829508  0.476227
0     4          SARIMAX Random Search  0.436623  0.951932  0.390242
1     4  SARIMAX Halving Random Search  0.522860  1.045781  0.505118
2     4                      AutoARIMA  0.627798  1.105062  0.507716
3     4                        Chronos  0.435270  1.091838  0.435129
0     5          SARIMAX Random Search  0.158866  0.230647  0.377782
1     5  SARIMAX Halving Random Search  0.148528  0.215787  0.320323
2     5                      AutoARIMA  0.147216  0.224164  0.329264
3     5                        Chronos  0.202701  0.271278  0.574316
0     6          SARIMAX Random Search  1.599181  2.300296  1.092540
1     6  SARIMAX Halving Random Search  1.760099  2.198632  0.785993
2     6                      AutoARIMA  1.685523  2.102012  0.729905
3     6                        Chronos  1.577470  2.441092  1.294801
0    12          SARIMAX Random Search  0.959467  1.328700  0.715279
1    12  SARIMAX Halving Random Search  0.924007  1.270113  0.655058
2    12                      AutoARIMA  0.935235  1.351552  0.725232
3    12                        Chronos  0.990575  1.478875  0.995089

currently these values seem off, need to check if the forecast values are correct

   site                  model           mae          rmse      wape
0     2  SARIMAX Random Search  1.317392e+09  1.334757e+09  1.000000
1     2              AutoARIMA  1.177017e+00  1.355828e+00  2.516028
2     2                Chronos  5.580797e-01  8.242962e-01  0.469230
0     4  SARIMAX Random Search  1.087740e+09  1.177901e+09  1.000000
1     4              AutoARIMA  6.277985e-01  1.105062e+00  0.507716
2     4                Chronos  4.304414e-01  1.089149e+00  0.430645
0     5  SARIMAX Random Search  4.776933e+08  4.806244e+08  1.000000
1     5              AutoARIMA  1.472156e-01  2.241645e-01  0.329264
2     5                Chronos  2.015243e-01  2.704622e-01  0.573095
0     6  SARIMAX Random Search  2.391052e+09  2.428822e+09  1.000000
1     6              AutoARIMA  1.685523e+00  2.102012e+00  0.729905
2     6                Chronos  1.702972e+00  2.423801e+00  1.186502
0    12  SARIMAX Random Search  1.417442e+09  1.488915e+09  1.000000
1    12              AutoARIMA  9.352354e-01  1.351552e+00  0.725232
2    12                Chronos  9.842342e-01  1.467244e+00  0.970192

"""