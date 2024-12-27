import pandas as pd
import shared.shared_utility as shared_utility
import src.main.shared_variables as shared_variables
import src.main.preprocessed_data as preprocessed_data

def _import_raw_ag_predictions():
    predictions = {}
    for site in shared_utility.sites:
        site_predictions = {}
        for model in shared_variables.ag_model_names:
            df = pd.read_csv(f'{shared_variables.ag_forecasts_path}/{site}/{model}.csv')
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
        df = pd.read_csv(f'{shared_variables.skforecast_forecasts_path}/predictions_sarimax_{site}.csv', header=0, names=['timestamp', 'mean'])
        predictions[site] = df.assign(timestamp=df['timestamp'].astype('datetime64[ns, UTC]')).set_index('timestamp')
    return predictions

def _import_nixtla_predictions():
    predictions = {}
    for site in shared_utility.sites:
        df = pd.read_csv(f'{shared_variables.nixtla_forecasts_path}/predictions_lstm_{site}.csv', header=0, names=['unique_id', 'timestamp', 'mean'])
        predictions[site] = df[['timestamp', 'mean']].assign(timestamp=df['timestamp'].astype('datetime64[ns, UTC]')).set_index('timestamp')
    return predictions

def get_summary():
    actual_dfs = preprocessed_data.get_sites_independent_dfs_only_main()
    ag_predictions = _import_ag_predictions()
    skforecast_predictions = _import_skforecast_predictions()
    nixtla_predictions = _import_nixtla_predictions()
    summary = {}
    for site in shared_utility.sites:
        summary[site] = {
            'actual': actual_dfs[site].set_index('start_time'),
            'Theta': ag_predictions[site]['Theta'],
            'AutoARIMA': ag_predictions[site]['AutoARIMA'],
            'Chronos': ag_predictions[site]['ChronosFineTunedWithRegressor[bolt_base]'],
            'SARIMAX': skforecast_predictions[site],
            'LSTM': nixtla_predictions[site],
        }
    return summary
