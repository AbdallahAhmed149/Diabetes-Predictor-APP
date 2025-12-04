import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder

import warnings
warnings.filterwarnings("ignore")

# Dataset Link: https://www.kaggle.com/datasets/mohankrishnathalla/diabetes-health-indicators-dataset
diabetes_dataset = pd.read_csv("data\diabetes_dataset.csv")

# diabetes_dataset Exploration
print(diabetes_dataset.shape)
print(diabetes_dataset.head())
print(diabetes_dataset.info())
print(diabetes_dataset.describe())

# Null Values
print(diabetes_dataset.isna().sum())

# Removing dublicated values
diabetes_dataset.drop_duplicates(inplace=True)

# Function to visualize the outliers
def visualize_outliers(data):
    numerical_data = data.select_dtypes("number")
    fig, ax = plt.subplots(len(numerical_data.columns), 1, figsize=(7, 18), dpi=95)
    for i, col in enumerate(numerical_data.columns):
        ax[i].boxplot(data[col], vert=False)
        ax[i].set_ylabel(col)
    plt.tight_layout()
    plt.show()

# Function to visualize the distribution
def visualize_distribution(data):
    numerical_data = data.select_dtypes("number")
    fig, ax = plt.subplots(len(numerical_data.columns), 1, figsize=(7, 18), dpi=95)
    for i, col in enumerate(numerical_data.columns):
        ax[i].hist(data[col])
        ax[i].set_ylabel(col)
    plt.tight_layout()
    plt.show()

# Before Handling Outliers
visualize_outliers(diabetes_dataset)
visualize_distribution(diabetes_dataset)

# Handling outliers
numerical_data = diabetes_dataset.select_dtypes("number")
for col in numerical_data.columns:
    lower_bound = diabetes_dataset[col].quantile(0.01)
    upper_bound = diabetes_dataset[col].quantile(0.99)
    diabetes_dataset[col] = np.clip(diabetes_dataset[col], lower_bound, upper_bound)

# After Handling Outliers
visualize_outliers(diabetes_dataset)
visualize_distribution(diabetes_dataset)

# =======================================================================================================

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

# Converting right skewed features to normally distributed
skewed = [
    "insulin_level",
    "triglycerides",
    "ldl_cholesterol",
    "glucose_postprandial",
    "hba1c",
]
for col in skewed:
    diabetes_dataset[col + "_log"] = np.log1p(diabetes_dataset[col])

# Visualization after converting
visualize_distribution(diabetes_dataset[skewed])

# Feature Encoding
onehot_encoding_cloumns = ["gender", "ethnicity", "employment_status"]
onehot_encoding = OneHotEncoder(sparse_output=False)
encoded_data = onehot_encoding.fit_transform(diabetes_dataset[onehot_encoding_cloumns])
encoded_col = onehot_encoding.get_feature_names_out(onehot_encoding_cloumns)
diabetes_dataset[encoded_col] = encoded_data

diabetes_dataset["education_level_encoded"] = diabetes_dataset["education_level"].map(
    {"No formal": 0, "Highschool": 1, "Graduate": 2, "Postgraduate": 3}
)
diabetes_dataset["income_level_encoded"] = diabetes_dataset["income_level"].map(
    {"Low": 0, "Lower-Middle": 1, "Middle": 2, "Upper-Middle": 3, "High": 4}
)
diabetes_dataset["smoking_status_encoded"] = diabetes_dataset["smoking_status"].map(
    {"Never": 0, "Former": 1, "Current": 2}
)

# To detect columns probably cause dataleakage
for col in (
    diabetes_dataset.select_dtypes("number").drop("diagnosed_diabetes", axis=1).columns
):
    corr = diabetes_dataset[col].corr(diabetes_dataset["diagnosed_diabetes"])
    if corr > 0.9:
        print(f"{col}: {corr}")

# -------------------------------------------------------------------------------------

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler, PolynomialFeatures
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    RandomizedSearchCV,
)
from sklearn.metrics import (
    accuracy_score,
    mean_squared_error,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve,
)

# After train/test split and BEFORE scaling
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

drop_cols = diabetes_dataset.select_dtypes("object").columns.tolist()
drop_cols.extend(["diagnosed_diabetes", "diabetes_risk_score"])

X = diabetes_dataset.drop(drop_cols, axis=1)
y = diabetes_dataset["diagnosed_diabetes"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

robust_scaler = RobustScaler()
X_train = robust_scaler.fit_transform(X_train)
X_test = robust_scaler.transform(X_test)

params = {
    "tol": [1e-1, 1e-2, 1e-3, 1e-4, 1e-5],
    "C": [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
    "max_iter": [1000, 2000, 5000, 10000],
    "intercept_scaling": list(range(1, 11)),
    "solver": ["lbfgs", "liblinear", "newton-cg", "newton-cholesky", "sag", "saga"],
    "class_weight": ["balanced"],
    "penalty": ["l2"],
}

# Logistic Regression Algorithm
model_LoR = LogisticRegression()

# Hyperimeter Tuning
randomized_search = RandomizedSearchCV(
    model_LoR, params, cv=5, n_jobs=-1, n_iter=100, random_state=42
)
randomized_search.fit(X_train, y_train)

# The Best Model --> LogisticRegression(tol=0.01, C=10.0, class_weight='balanced', intercept_scaling=2, max_iter=1000, solver='newton-cholesky', penalty="l2")
best_model_LoR = randomized_search.best_estimator_
print(f"The Best Logistic Regression Model: {best_model_LoR}")
best_model_LoR.fit(X_train, y_train)

# Cross Validation
cross_validation = cross_val_score(best_model_LoR, X_train, y_train, cv=5)

y_pred = best_model_LoR.predict(X_test)
y_pred_propa = best_model_LoR.predict_proba(X_test)[:, 1]

print(f"Training Score: {best_model_LoR.score(X_train, y_train)}")
print(f"Testing Score: {accuracy_score(y_test, y_pred)}")
print(f"CV Score: {np.mean(cross_validation)}")
print(f"Mean Squared Error (MSE): {mean_squared_error(y_test, y_pred)}")

print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
print(f"Classification Report:\n{classification_report(y_test, y_pred)}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# ROC AUC Score
rocauc_score = roc_auc_score(y_test, y_pred_propa)
print(f"ROC AUC Score: {rocauc_score}")

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_propa)
plt.plot([0, 1], [0, 1], "k--")
plt.plot(fpr, tpr)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Logistic Regression ROC Curve")
plt.show()

# Feature Importance
feature_importance = pd.DataFrame(
    {"feature": X.columns, "coefficient": best_model_LoR.coef_[0]}
).sort_values("coefficient", ascending=False, key=abs)
feature_importance = feature_importance.head(15)
plt.barh(range(len(feature_importance)), feature_importance["coefficient"])
plt.yticks(range(len(feature_importance)), labels=feature_importance["feature"])
plt.xlabel("Coefficient")
plt.title("Feature Importance")
plt.grid(alpha=0.3)
plt.show()

# Saving the model
import joblib

joblib.dump(best_model_LoR, "model/logistic_regression_diabetes_model.pkl")
joblib.dump(robust_scaler, "model/robust_scaler.pkl")
joblib.dump(X.columns.tolist(), "model/feature_columns.pkl")
joblib.dump(onehot_encoding, "model/onehot_encoder.pkl")
