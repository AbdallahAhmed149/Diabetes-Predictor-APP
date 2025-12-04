from typing import Dict, Any, Tuple
import numpy as np
from app.ml.load_models import get_ml_models
from app.ml.preprocessor import DiabetesPreprocessor


class DiabetesPredictor:
    """
    Main predictor class for diabetes risk prediction
    """

    def __init__(self):
        self.ml_models = get_ml_models()
        self.preprocessor = DiabetesPreprocessor(
            encoder=self.ml_models.encoder, poly=self.ml_models.poly
        )

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make prediction on input data

        Args:
            input_data: Dictionary containing all 29 input fields

        Returns:
            Dictionary containing prediction results
        """
        # Preprocess the data
        processed_data = self.preprocessor.preprocess(input_data)

        # Ensure columns match training data
        # Reorder columns to match feature_columns from training
        feature_cols = self.ml_models.feature_columns

        # Add missing columns with 0
        for col in feature_cols:
            if col not in processed_data.columns:
                processed_data[col] = 0

        # Select and reorder columns
        processed_data = processed_data[feature_cols]

        # Scale the features
        scaled_data = self.ml_models.scaler.transform(processed_data)

        # Make prediction
        prediction_class = int(self.ml_models.model.predict(scaled_data)[0])
        prediction_proba = float(self.ml_models.model.predict_proba(scaled_data)[0][1])

        # Determine risk level
        risk_level = self._calculate_risk_level(prediction_proba)

        return {
            "prediction_class": prediction_class,
            "risk_probability": round(
                prediction_proba * 100, 2
            ),  # Convert to percentage
            "risk_level": risk_level,
            "risk_interpretation": self._get_risk_interpretation(
                risk_level, prediction_proba
            ),
        }

    def _calculate_risk_level(self, probability: float) -> str:
        """Calculate risk level from probability"""
        if probability < 0.3:
            return "Low"
        elif probability < 0.7:
            return "Medium"
        else:
            return "High"

    def _get_risk_interpretation(self, risk_level: str, probability: float) -> str:
        """Get human-readable interpretation of risk"""
        prob_percent = round(probability * 100, 1)

        interpretations = {
            "Low": f"Low risk of diabetes ({prob_percent}%). Continue healthy lifestyle habits.",
            "Medium": f"Moderate risk of diabetes ({prob_percent}%). Consider lifestyle modifications and regular monitoring.",
            "High": f"High risk of diabetes ({prob_percent}%). Consult with healthcare provider for detailed evaluation.",
        }

        return interpretations.get(risk_level, "Unknown risk level")


# Create global predictor instance
diabetes_predictor = DiabetesPredictor()


def get_predictor():
    """Get predictor instance"""
    return diabetes_predictor
