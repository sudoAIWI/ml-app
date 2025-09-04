from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib


def load_data():
    """Load and return iris dataset"""
    iris = load_iris()
    return iris.data, iris.target, iris.target_names


def train_model():
    """Train a Random Forest classifier on iris data"""
    X, y, target_names = load_data()

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"Model trained with accuracy: {accuracy:.2f}")

    return model, target_names


def save_model(model, target_names, filename="model.joblib"):
    """Save trained model and target names"""
    model_data = {"model": model, "target_names": target_names}
    joblib.dump(model_data, filename)
    print(f"Model saved to {filename}")


if __name__ == "__main__":
    # Train and save model
    model, target_names = train_model()
    save_model(model, target_names)
