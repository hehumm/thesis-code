import experiments.autogluon_presets.model_training as model_training
import experiments.chronos.preprocessing_autogluon as preprocessing_autogluon

sites_ids = [2, 4, 5, 6, 12]
sites_data = preprocessing_autogluon.get_autogluon_compatible_sites_independent_dfs_without_covariates()
prediction_length = 36

for site_id in sites_ids:
    model_training.train_model(
        sites_data.get(site_id), 
        prediction_length, 
        f'/home/henri/Code/thesis-code/experiments/autogluon_presets/models/separate/{site_id}', 
        f'/home/henri/Code/thesis-code/experiments/autogluon_presets/predictions/separate/{site_id}.csv', 
        'WAPE'
    )
