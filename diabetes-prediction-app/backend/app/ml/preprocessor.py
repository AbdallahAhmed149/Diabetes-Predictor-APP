import pandas as pd
import numpy as np
from typing import Dict, Any


class DiabetesPreprocessor:
    """
    Preprocessor for diabetes prediction input data
    Applies the same transformations as the original model training
    """

    def __init__(self, encoder, poly):
        self.encoder = encoder
        self.poly = poly

    def preprocess(self, input_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Preprocess raw input data for prediction

        Args:
            input_data: Dictionary containing all 29 input fields

        Returns:
            DataFrame ready for model prediction
        """
        # Create DataFrame from input
        df = pd.DataFrame([input_data])

        # Feature Engineering
        df["hba1c_glucose_interaction"] = df["hba1c"] * df["glucose_postprandial"]
        df["age_bmi"] = df["age"] * df["bmi"]
        df["insulin_resistance_proxy"] = (
            df["glucose_fasting"] * df["insulin_level"]
        ) / 405
        df["bmi_glucose"] = df["bmi"] * df["glucose_fasting"]

        # Log transformations for skewed features
        skewed_features = [
            "insulin_level",
            "triglycerides",
            "ldl_cholesterol",
            "glucose_postprandial",
            "hba1c",
        ]
        for col in skewed_features:
            df[col + "_log"] = np.log1p(df[col])

        # One-hot encoding for categorical features
        categorical_cols = ["gender", "ethnicity", "employment_status"]
        encoded_data = self.encoder.transform(df[categorical_cols])
        encoded_col_names = self.encoder.get_feature_names_out(categorical_cols)
        df[encoded_col_names] = encoded_data

        # Ordinal encoding for ordered categorical features
        df["education_level_encoded"] = df["education_level"].map(
            {"No formal": 0, "Highschool": 1, "Graduate": 2, "Postgraduate": 3}
        )

        df["income_level_encoded"] = df["income_level"].map(
            {"Low": 0, "Lower-Middle": 1, "Middle": 2, "Upper-Middle": 3, "High": 4}
        )

        df["smoking_status_encoded"] = df["smoking_status"].map(
            {"Never": 0, "Former": 1, "Current": 2}
        )

        # Polynomial features for important columns
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

        # Fit poly on important cols subset (this should match training)
        poly_features = self.poly.fit_transform(df[important_cols])
        poly_col_names = self.poly.get_feature_names_out(important_cols)
        df[poly_col_names] = poly_features

        # Drop categorical columns
        categorical_to_drop = [
            "gender",
            "ethnicity",
            "employment_status",
            "education_level",
            "income_level",
            "smoking_status",
        ]
        df = df.drop(columns=categorical_to_drop, errors="ignore")

        return df
