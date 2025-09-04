import joblib


def load_model(filename="model.joblib"):
    """Load trained model from file"""
    model_data = joblib.load(filename)
    return model_data["model"], model_data["target_names"]


def predict(model, target_names, features):
    """Make prediction using the trained model"""
    prediction = model.predict([features])[0]
    return target_names[prediction]
