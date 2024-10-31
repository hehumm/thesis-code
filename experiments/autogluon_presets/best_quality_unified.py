import experiments.autogluon_presets.model_training as model_training
import experiments.chronos.preprocessing_autogluon as preprocessing_autogluon

sites_ids = [2, 4, 5, 6, 12]
unified_data_without_covariates = preprocessing_autogluon.get_autogluon_compatible_unified_df_without_covariates()
prediction_length = 36

model_training.train_model(
    unified_data_without_covariates, 
    prediction_length, 
    f'/home/henri/Code/thesis-code/experiments/autogluon_presets/models/unified', 
    f'/home/henri/Code/thesis-code/experiments/autogluon_presets/predictions/unified.csv', 
    'WAPE'
)

print('Best quality unified model trained and predictions made.')