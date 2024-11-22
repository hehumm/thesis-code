import itertools
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings("ignore")
import shared.preprocessing_general as preprocessing_general

dfs = preprocessing_general.get_sites_with_data_wide()
target_column = 'load_energy_sum'
forecast_horizon = 36

for site_id, df in dfs.items():
    y = df[target_column]
    y_train = y[:-forecast_horizon]
    X = df[['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage']]
    X_train = X[:-forecast_horizon]
    
    # Define parameter ranges
    p = q = range(1, 3)
    d = range(0, 1)
    P = Q = range(0, 2)
    D = range(0, 1)
    m = [24]  # Seasonal period (daily)

    # Generate all combinations of parameters
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], m[0]) for x in itertools.product(P, D, Q)]

    # Grid search to find the best parameters
    best_aic = float("inf")
    best_order = None
    best_seasonal_order = None

    for order in pdq:
        for seasonal_order in seasonal_pdq:
            print('orders: ', order, seasonal_order)
            try:
                model = SARIMAX(y_train, exog=X_train, order=order, seasonal_order=seasonal_order)
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