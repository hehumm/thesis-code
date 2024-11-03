from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
from datetime import datetime

def train_and_predict_with_model(df, prediction_length, model_path, predictions_path_1, predictions_path_2, known_covariates_names, known_covariates, eval_metric):
    tsdf = TimeSeriesDataFrame.from_data_frame(df)
    train_data, test_data = tsdf.train_test_split(prediction_length)

    predictor = TimeSeriesPredictor(
        prediction_length=prediction_length,
        path=model_path,
        target='target',
        eval_metric=eval_metric,
        known_covariates_names=known_covariates_names,
    )

    print('\nFitting and predicting...\n')
    print(f'fitting started at {datetime.now()}')
    predictor.fit(train_data, presets="fast_training", time_limit=600)

    ets_predictions = predictor.predict(data=train_data, known_covariates=known_covariates, model='ETS')
    ets_predictions.to_csv(predictions_path_1)

    theta_predictions = predictor.predict(data=train_data, known_covariates=known_covariates, model='Theta')
    theta_predictions.to_csv(predictions_path_2)

    #predictor.fit(train_data, presets="best_quality", time_limit=3600)

    #chronos_predictions = predictor.predict(data: train_data, known_covariates=known_covariates, model: 'Chronos[large]')
    #chronos_predictions.to_csv(predictions_path_1)

    #arima_predictions = predictor.predict(data: train_data, known_covariates=known_covariates, model: 'AutoARIMA')
    #arima_predictions.to_csv(predictions_path_2)

    print(f'predicting ended at {datetime.now()}')