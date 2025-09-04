from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    sepal_length: float = Field(..., description="Sepal length in cm")
    sepal_width: float = Field(..., description="Sepal width in cm")
    petal_length: float = Field(..., description="Petal length in cm")
    petal_width: float = Field(..., description="Petal width in cm")


class PredictResponse(BaseModel):
    prediction: str
    probabilities: dict


# Train the model first
if __name__ == "__main__":
    from training import train_model, save_model

    model, target_names = train_model()
    save_model(model, target_names)
