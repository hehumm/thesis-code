import pandas as pd
import shared.shared_utility as shared_utility
import experiments.final.final_shared as final_shared
import experiments.final.preprocessed_data as preprocessed_data

def _import_raw_ag_predictions():
    predictions = {}
    for site in shared_utility.sites:
        site_predictions = {}
        for model in final_shared.ag_model_names:
            df = pd.read_csv(f'{final_shared.ag_forecasts_path}/{site}/{model}.csv')
            site_predictions[model] = df
        predictions[site] = site_predictions
    return predictions

def _import_ag_predictions():
    raw_predictions = _import_raw_ag_predictions()
    predictions = {}
    for site, site_predictions in raw_predictions.items():
        predictions[site] = {}
        for model, df in site_predictions.items():
            predictions[site][model] = df[['timestamp', 'mean']].assign(timestamp=df['timestamp'].astype('datetime64[ns, UTC]')).set_index('timestamp')
    return predictions

def _import_skforecast_predictions():
    predictions = {}
    for site in shared_utility.sites:
        df = pd.read_csv(f'{final_shared.skforecast_forecasts_path}/predictions_sarimax_{site}.csv', header=0, names=['timestamp', 'mean'])
        predictions[site] = df.assign(timestamp=df['timestamp'].astype('datetime64[ns, UTC]')).set_index('timestamp')
    return predictions

def _import_nixtla_predictions():
    predictions = {}
    for site in shared_utility.sites:
        df = pd.read_csv(f'{final_shared.nixtla_forecasts_path}/predictions_lstm_{site}.csv', header=0, names=['unique_id', 'timestamp', 'mean'])
        predictions[site] = df[['timestamp', 'mean']].assign(timestamp=df['timestamp'].astype('datetime64[ns, UTC]')).set_index('timestamp')
    return predictions

def _convert_one_dfs_target_to_megawatt_hours(df, column='mean'):
    df_copy = df.copy()
    df_copy[column] = df_copy[column] / 1000000000
    return df_copy

def get_summary():
    actual_dfs = preprocessed_data.get_sites_independent_dfs_only_main()
    ag_predictions = _import_ag_predictions()
    skforecast_predictions = _import_skforecast_predictions()
    nixtla_predictions = _import_nixtla_predictions()
    summary = {}
    for site in shared_utility.sites:
        summary[site] = {
            'actual': _convert_one_dfs_target_to_megawatt_hours(actual_dfs[site].set_index('timestamp'), column='target'),
            'Theta': _convert_one_dfs_target_to_megawatt_hours(ag_predictions[site]['Theta']),
            'ETS': _convert_one_dfs_target_to_megawatt_hours(ag_predictions[site]['ETS']),
            'AutoARIMA': _convert_one_dfs_target_to_megawatt_hours(ag_predictions[site]['AutoARIMA']),
            'Chronos': _convert_one_dfs_target_to_megawatt_hours(ag_predictions[site]['ChronosFineTunedWithRegressor[bolt_base]']),
            'SARIMAX': _convert_one_dfs_target_to_megawatt_hours(skforecast_predictions[site]),
            'LSTM': _convert_one_dfs_target_to_megawatt_hours(nixtla_predictions[site]),
        }
    return summary
