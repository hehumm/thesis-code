import shared.preprocessing_general as preprocessing_general
from statsmodels.tsa.stattools import adfuller
from sklearn.preprocessing import StandardScaler
import itertools
from statsmodels.tsa.statespace.sarimax import SARIMAX

def _find_spikes_for_one_site(df, column, threshold=0.95):
    threshold_value = df[column].quantile(threshold)
    spikes = df[df[column] > threshold_value]
    return spikes[['load_energy_sum']]

def find_spikes(spike_threshold=0.95):
    dfs = preprocessing_general.get_sites_with_data_wide()
    spikes = {}
    for site_id, df in dfs.items():
        spike = _find_spikes_for_one_site(df, 'load_energy_sum', threshold=0.95)
        spikes[site_id] = spike
    return spikes

def get_sites_with_data_without_spikes(dfs):
    for site_id, df in dfs.items():
        spikes = _find_spikes_for_one_site(df, 'load_energy_sum', threshold=0.95)
        for index, row in spikes.iterrows():
            df.loc[index, 'load_energy_sum'] = None
        df = df.interpolate()
        dfs[site_id] = df
    return dfs

def convert_target_to_megawatt_hours(dfs):
    for site_id, df in dfs.items():
        df['load_energy_sum'] = df['load_energy_sum'] / 1000000000
    return dfs

def standardize_exog_data(dfs):
    for site_id, df in dfs.items():
        scaler = StandardScaler()
        df[['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage']] = scaler.fit_transform(df[['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage']])
    return dfs

def test_train_split(dfs, forecast_horizon=36):
    train_dfs = {}
    test_dfs = {}
    for site_id, df in dfs.items():
        train_dfs[site_id] = df[:-forecast_horizon]
        test_dfs[site_id] = df[-forecast_horizon:]
    return train_dfs, test_dfs

def test_sites_for_stationarity(dfs):
    forecast_horizon = 36
    for site_id, df in dfs.items():
        y = df['load_energy_sum']
        y_train = y[:-forecast_horizon]
        result = adfuller(y_train)
        print(f'Site {site_id} p-value: {result[1]}')

def get_sites_with_stationary_data(dfs):
    dfs[5] = dfs[5].diff().dropna()
    return dfs

def perform_grid_search(dfs):
    target_column = 'load_energy_sum'
    for site_id, df in dfs.items():
        y = df[target_column]
        X = df[['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage']]
        
        # Define parameter ranges
        p = q = range(0, 4)
        d = range(0, 2)
        P = Q = range(0, 3)
        D = range(0, 2)
        m = [12, 24]

        # Generate all combinations of parameters
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], m[0]) for x in itertools.product(P, D, Q)]

        print(f"combinations count: {len(pdq) * len(seasonal_pdq)}")

        # Grid search to find the best parameters
        best_aic = float("inf")
        best_order = None
        best_seasonal_order = None

        for order in pdq:
            for seasonal_order in seasonal_pdq:
                print('orders: ', order, seasonal_order)
                try:
                    model = SARIMAX(y, exog=X, order=order, seasonal_order=seasonal_order)
                    results = model.fit(disp=False)
                    if results.aic < best_aic:
                        best_aic = results.aic
                        best_order = order
                        best_seasonal_order = seasonal_order
                except:
                    continue

        print(f"Site {site_id} best order:", best_order)
        print(f"Site {site_id} best seasonal order:", best_seasonal_order)
        with open("best_orders.txt", "a") as file:
            file.write(f"Site {site_id} best order: {best_order}\n")
            file.write(f"Site {site_id} best seasonal order: {best_seasonal_order}\n")