"""
Script to retrain the model and export all artifacts with correct feature count
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, RobustScaler, PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import warnings

warnings.filterwarnings("ignore")

# Load dataset
print("Loading dataset...")
diabetes_dataset = pd.read_csv("data/diabetes_dataset.csv")
diabetes_dataset.drop_duplicates(inplace=True)

# Handle outliers
numerical_data = diabetes_dataset.select_dtypes("number")
for col in numerical_data.columns:
    lower_bound = diabetes_dataset[col].quantile(0.01)
    upper_bound = diabetes_dataset[col].quantile(0.99)
    diabetes_dataset[col] = np.clip(diabetes_dataset[col], lower_bound, upper_bound)

print("Performing feature engineering...")

# Feature Engineering
diabetes_dataset["hba1c_glucose_interaction"] = (
    diabetes_dataset["hba1c"] * diabetes_dataset["glucose_postprandial"]
)
diabetes_dataset["age_bmi"] = diabetes_dataset["age"] * diabetes_dataset["bmi"]
diabetes_dataset["insulin_resistance_proxy"] = (
    diabetes_dataset["glucose_fasting"] * diabetes_dataset["insulin_level"] / 405
)
diabetes_dataset["bmi_glucose"] = (
    diabetes_dataset["bmi"] * diabetes_dataset["glucose_fasting"]
)

# Log transformations
skewed = [
    "insulin_level",
    "triglycerides",
    "ldl_cholesterol",
    "glucose_postprandial",
    "hba1c",
]
for col in skewed:
    diabetes_dataset[col + "_log"] = np.log1p(diabetes_dataset[col])

# Onehot encoding
onehot_encoding_columns = ["gender", "ethnicity", "employment_status"]
onehot_encoding = OneHotEncoder(sparse_output=False)
encoded_data = onehot_encoding.fit_transform(diabetes_dataset[onehot_encoding_columns])
encoded_col = onehot_encoding.get_feature_names_out(onehot_encoding_columns)
diabetes_dataset[encoded_col] = encoded_data

# Ordinal encoding
diabetes_dataset["education_level_encoded"] = diabetes_dataset["education_level"].map(
    {"No formal": 0, "Highschool": 1, "Graduate": 2, "Postgraduate": 3}
)
diabetes_dataset["income_level_encoded"] = diabetes_dataset["income_level"].map(
    {"Low": 0, "Lower-Middle": 1, "Middle": 2, "Upper-Middle": 3, "High": 4}
)
diabetes_dataset["smoking_status_encoded"] = diabetes_dataset["smoking_status"].map(
    {"Never": 0, "Former": 1, "Current": 2}
)

# Polynomial features
important_cols = [
    "hba1c",
    "glucose_fasting",
    "bmi",
    "age",
    "insulin_level_log",
    "glucose_postprandial",
    "age_bmi",
    "hba1c_glucose_interaction",
    "bmi_glucose",
    "insulin_resistance_proxy",
]

poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True)
poly_features = poly.fit_transform(diabetes_dataset[important_cols])
poly_col_names = poly.get_feature_names_out(important_cols)
diabetes_dataset[poly_col_names] = poly_features

# Prepare X and y
drop_cols = diabetes_dataset.select_dtypes("object").columns.tolist()
drop_cols.extend(["diagnosed_diabetes", "diabetes_risk_score"])

X = diabetes_dataset.drop(drop_cols, axis=1)
y = diabetes_dataset["diagnosed_diabetes"]

print(f"Total features in X: {len(X.columns)}")
print(f"Feature list: {X.columns.tolist()[:10]}...")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scaling
robust_scaler = RobustScaler()
X_train_scaled = robust_scaler.fit_transform(X_train)
X_test_scaled = robust_scaler.transform(X_test)

# Train model with best parameters from original training
print("Training model...")
best_model_LoR = LogisticRegression(
    tol=0.01,
    C=10.0,
    class_weight="balanced",
    intercept_scaling=2,
    max_iter=1000,
    solver="newton-cholesky",
    penalty="l2",
)
best_model_LoR.fit(X_train_scaled, y_train)

# Evaluate
train_score = best_model_LoR.score(X_train_scaled, y_train)
test_score = best_model_LoR.score(X_test_scaled, y_test)
print(f"Training Score: {train_score}")
print(f"Testing Score: {test_score}")

# Save everything
print("Saving model artifacts...")
joblib.dump(
    best_model_LoR,
    "diabetes-prediction-app/backend/ml_models/logistic_regression_diabetes_model.pkl",
)
joblib.dump(
    robust_scaler, "diabetes-prediction-app/backend/ml_models/robust_scaler.pkl"
)
joblib.dump(
    X.columns.tolist(), "diabetes-prediction-app/backend/ml_models/feature_columns.pkl"
)
joblib.dump(
    onehot_encoding, "diabetes-prediction-app/backend/ml_models/onehot_encoder.pkl"
)
# IMPORTANT: Save the fitted poly object!
joblib.dump(poly, "diabetes-prediction-app/backend/ml_models/poly.pkl")

print(f"\n✅ Model saved successfully!")
print(f"Feature count: {len(X.columns)}")
print(f"Model expects: {best_model_LoR.n_features_in_} features")
print("All artifacts saved to diabetes-prediction-app/backend/ml_models/")
