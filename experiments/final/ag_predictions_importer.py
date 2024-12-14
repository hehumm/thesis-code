import pandas as pd
import shared.shared_utility as shared_utility
import experiments.final.final_shared as final_shared

def _import_raw_ag_predictions():
    all_predictions = {}
    for site in shared_utility.sites:
        site_predictions = {}
        for model in final_shared.ag_model_names:
            df = pd.read_csv(f'{final_shared.ag_forecasts_path}/{site}/{model}.csv')
            site_predictions[model] = df
        all_predictions[site] = site_predictions
    return all_predictions

def import_ag_predictions():
    raw_predictions = _import_raw_ag_predictions()
    predictions = {}
    for site, site_predictions in raw_predictions.items():
        predictions[site] = {}
        for model, df in site_predictions.items():
            predictions[site][model] = df[['timestamp', 'mean']].assign(timestamp=df['timestamp'].astype('datetime64[ns, UTC]')).set_index('timestamp')
    return predictions