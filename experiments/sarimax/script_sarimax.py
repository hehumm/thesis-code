"""
Initial MAPE scores for site 2 with SARIMAX:
[0.42172088724392065, 0.4211198717162883, 0.5788698955821633, 0.3390898691522347, 0.2839357863476988]


"""
import shared.rolling_cross_validation as rolling_cross_validation
import shared.preprocessing_general as preprocessing_general

df = preprocessing_general.get_sites_with_data_wide().get(2)
target_column = 'load_energy_sum'
exog_columns = ['buy_price_kwh', 'sell_price_kwh', 'temp', 'feels_like', 'pop', 'clouds', 'sun_percentage']
forecast_horizon = 36
n_splits = 5

metric_scores = rolling_cross_validation.validate_SARIMAX(df, target_column, exog_columns, forecast_horizon, n_splits)