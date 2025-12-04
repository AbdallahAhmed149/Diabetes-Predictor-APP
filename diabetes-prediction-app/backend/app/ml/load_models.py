import joblib
import os
from app.core.config import settings


class MLModels:
    """Singleton class to load and store ML models"""

    _instance = None
    _models_loaded = False

    model = None
    scaler = None
    encoder = None
    poly = None
    feature_columns = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLModels, cls).__new__(cls)
        return cls._instance

    def load_models(self):
        """Load all ML models and preprocessors"""
        if self._models_loaded:
            return

        models_path = settings.ML_MODELS_PATH

        try:
            # Load the trained model
            self.model = joblib.load(
                os.path.join(models_path, "logistic_regression_diabetes_model.pkl")
            )

            # Load the scaler
            self.scaler = joblib.load(os.path.join(models_path, "robust_scaler.pkl"))

            # Load the one-hot encoder
            self.encoder = joblib.load(os.path.join(models_path, "onehot_encoder.pkl"))

            # Load feature columns
            self.feature_columns = joblib.load(
                os.path.join(models_path, "feature_columns.pkl")
            )

            # Load the fitted polynomial features transformer
            self.poly = joblib.load(os.path.join(models_path, "poly.pkl"))

            self._models_loaded = True
            print("✅ ML models loaded successfully")
        except Exception as e:
            print(f"❌ Error loading ML models: {e}")
            raise


# Create global instance
ml_models = MLModels()


def get_ml_models():
    """Get ML models instance"""
    if not ml_models._models_loaded:
        ml_models.load_models()
    return ml_models
