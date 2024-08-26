import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import numpy as np

# Load the dataset
data_path = 'data3.csv'  # Update the path as needed
data = pd.read_csv(data_path)

# Extracting features (X) and target (y) for x and y coordinates
X = data.drop(columns=['target'])
y = data['target'].apply(eval)  # Convert the string tuples to actual tuples
y_x = y.apply(lambda coord: coord[0])
y_y = y.apply(lambda coord: coord[1])

# Split the data into training and test sets
X_train, X_test, y_x_train, y_x_test, y_y_train, y_y_test = train_test_split(X, y_x, y_y, test_size=0.2, random_state=42)

# Define the base models
svr_model = make_pipeline(StandardScaler(), SVR())
gbr_model = GradientBoostingRegressor(random_state=42)

# Fine-tuning SVR with a narrower range around the best found values
svr_param_grid = {
    'svr__C': [500, 1000, 2000],
    'svr__epsilon': [0.001, 0.01, 0.1],
    'svr__gamma': [0.01, 'auto', 0.1]
}

# Fine-tuning Gradient Boosting with a narrower range around the best found values
gbr_param_grid = {
    'learning_rate': [0.05, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'n_estimators': [300, 500, 700]
}

# Refit and tune SVR and Gradient Boosting
best_svr_x = GridSearchCV(svr_model, svr_param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
best_svr_y = GridSearchCV(svr_model, svr_param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)

best_gbr_x = GridSearchCV(gbr_model, gbr_param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
best_gbr_y = GridSearchCV(gbr_model, gbr_param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)

# Fit the models
best_svr_x.fit(X_train, y_x_train)
best_svr_y.fit(X_train, y_y_train)

best_gbr_x.fit(X_train, y_x_train)
best_gbr_y.fit(X_train, y_y_train)

# Predictions
y_x_pred_svr = best_svr_x.predict(X_test)
y_y_pred_svr = best_svr_y.predict(X_test)

y_x_pred_gbr = best_gbr_x.predict(X_test)
y_y_pred_gbr = best_gbr_y.predict(X_test)

# Ensembling: Average of SVR and Gradient Boosting predictions
y_x_pred_ensemble = (y_x_pred_svr + y_x_pred_gbr) / 2
y_y_pred_ensemble = (y_y_pred_svr + y_y_pred_gbr) / 2

# Evaluate the ensemble
mse_x_ensemble = mean_squared_error(y_x_test, y_x_pred_ensemble)
mae_x_ensemble = mean_absolute_error(y_x_test, y_x_pred_ensemble)
r2_x_ensemble = r2_score(y_x_test, y_x_pred_ensemble)

mse_y_ensemble = mean_squared_error(y_y_test, y_y_pred_ensemble)
mae_y_ensemble = mean_absolute_error(y_y_test, y_y_pred_ensemble)
r2_y_ensemble = r2_score(y_y_test, y_y_pred_ensemble)

# Save the best models and ensemble predictions
joblib.dump(best_svr_x.best_estimator_, 'best_svr_x_tuned.pkl')
joblib.dump(best_svr_y.best_estimator_, 'best_svr_y_tuned.pkl')
joblib.dump(best_gbr_x.best_estimator_, 'best_gbr_x_tuned.pkl')
joblib.dump(best_gbr_y.best_estimator_, 'best_gbr_y_tuned.pkl')

# Print ensemble results
ensemble_results = {
    'y_x': {'MSE': mse_x_ensemble, 'MAE': mae_x_ensemble, 'R2': r2_x_ensemble},
    'y_y': {'MSE': mse_y_ensemble, 'MAE': mae_y_ensemble, 'R2': r2_y_ensemble}
}

print("Ensemble Results:")
print("y_x - MSE:", ensemble_results['y_x']['MSE'], ", MAE:", ensemble_results['y_x']['MAE'], ", R2:", ensemble_results['y_x']['R2'])
print("y_y - MSE:", ensemble_results['y_y']['MSE'], ", MAE:", ensemble_results['y_y']['MAE'], ", R2:", ensemble_results['y_y']['R2'])
