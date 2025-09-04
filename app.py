from fastapi import FastAPI, HTTPException
from settings import Settings
from dotenv import load_dotenv
from inference import load_model, predict
from api.models.iris import PredictRequest, PredictResponse


# Load environment variables
load_dotenv(".env.dev", override=True)
settings = Settings()

# Load ML model
try:
    model, target_names = load_model("model.joblib")
    print("Model loaded successfully")
except FileNotFoundError:
    print("Model file not found. Please train the model first.")
    model, target_names = None, None

app = FastAPI(title=settings.APP_NAME)


@app.get("/")
def welcome_root():
    return {"message": "Welcome to the ML API", "environment": settings.ENVIRONMENT}


@app.get("/health")
def health_check():
    model_status = "loaded" if model else "not loaded"
    return {"status": "ok", "app_name": settings.APP_NAME, "model_status": model_status}


@app.post("/predict", response_model=PredictResponse)
def predict_iris(request: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Convert request to feature array
        features = [
            request.sepal_length,
            request.sepal_width,
            request.petal_length,
            request.petal_width,
        ]

        # Get prediction
        prediction = predict(model, target_names, features)

        # Get probabilities
        probabilities = model.predict_proba([features])[0]
        prob_dict = {
            target_names[i]: float(prob) for i, prob in enumerate(probabilities)
        }

        return PredictResponse(prediction=prediction, probabilities=prob_dict)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
