import statsmodels.api as sm
from sklearn.metrics import mean_absolute_percentage_error
import experiments.sarimax.utility as utility

def _split_into_time_windows(df, splits_count):
    splits = []
    split_elements_count = len(df) // splits_count
    leftover_elements_count = len(df) % splits_count
    for i in range(splits_count):
        start = i * split_elements_count
        if i == splits_count - 1:
            end = start + split_elements_count + leftover_elements_count
        else:
            end = start + split_elements_count
        
        
        split_df = df.iloc[start:end]
        splits.append(split_df)
    return splits

def validate_SARIMAX(df, target_column, exog_columns, forecast_horizon, splits_count):
    time_windows = _split_into_time_windows(df, splits_count)
    metric_scores = []
    for i in range(splits_count):

        train_df = time_windows[i].iloc[:-forecast_horizon]
        test_df = time_windows[i].iloc[-forecast_horizon:]

        y_train = train_df[target_column]
        X_train = train_df[exog_columns]
        y_test = test_df[target_column]
        X_test = test_df[exog_columns]

        model = sm.tsa.statespace.SARIMAX(y_train, exog=X_train, order=utility.initial_model_params.get('order'), seasonal_order=utility.initial_model_params.get('seasonal_order'))
        results = model.fit(disp=False)

        forecast = results.get_forecast(steps=forecast_horizon, exog=X_test)
        forecast_values = forecast.predicted_mean

        mape = mean_absolute_percentage_error(y_test, forecast_values)
        metric_scores.append(mape)
    
    return metric_scores
