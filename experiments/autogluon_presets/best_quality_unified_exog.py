import experiments.autogluon_presets.model_training as model_training
import experiments.chronos.preprocessing_autogluon as preprocessing_autogluon

sites_ids = [2, 4, 5, 6, 12]
unified_data_with_covariates = preprocessing_autogluon.get_autogluon_compatible_unified_df()
prediction_length = 36

model_training.train_model(
    unified_data_with_covariates, 
    prediction_length, 
    f'/home/henri/Code/thesis-code/experiments/autogluon_presets/models/unified_exog', 
    f'/home/henri/Code/thesis-code/experiments/autogluon_presets/predictions/unified_exog.csv', 
    'WAPE'
)

print('Best quality unified model with exogenous features trained and predictions made.')