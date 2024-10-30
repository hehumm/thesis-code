from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor

def train_model(df, prediction_length, model_path, predictions_path, eval_metric):
    data = TimeSeriesDataFrame.from_data_frame(df)
    train_data, test_data = data.train_test_split(prediction_length)

    predictor = TimeSeriesPredictor(
        prediction_length=prediction_length,
        path=model_path,
        target='target',
        eval_metric=eval_metric,
    )

    predictor.fit(train_data, presets="fast_training", time_limit=600) # don't forget to change the preset to best_quality
    predictions = predictor.predict(train_data)
    predictions.to_csv(predictions_path)