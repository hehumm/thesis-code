import shared.shared_utility as shared_utility
import experiments.archive.sarimax.utility as sarimax_utility
import pandas as pd

def _get_sarimax_results_path(site_id, variation):
    return f'/home/henri/Code/thesis-code/experiments/sarimax/forecasts/forecast_site_{site_id}_params_{variation}.csv'

def import_sarimax_predicitions():
    predictions = {}

    for site in shared_utility.sites:
        predictions[site] = {}
        for variation in sarimax_utility.variations:
            df = pd.read_csv(_get_sarimax_results_path(site, variation))
            df.rename(columns={'Unnamed: 0': 'timestamp', 'predicted_mean': 'mean'}, inplace=True)
            predictions[site][variation] = df

    return predictions
    