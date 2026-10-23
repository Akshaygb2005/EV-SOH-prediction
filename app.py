import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

# Initialize FastAPI App
app = FastAPI(
    title="EV Battery SoH Prediction API",
    description="API Endpoint for predicting Battery State of Health (SoH_Percent)",
    version="1.0.0",
)

# Load Model Pipeline and Metadata at Startup
MODEL_FILE = "best_ev_battery_soh_pipeline.joblib"

try:
    payload = joblib.load(MODEL_FILE)
    model_pipeline = payload["pipeline"]
    num_cols = payload["num_cols"]
    cat_cols = payload["cat_cols"]
    model_name = payload["model_name"]
    print(f"Successfully loaded {model_name} from {MODEL_FILE}")
except Exception as e:
    raise RuntimeError(f"Failed to load model from {MODEL_FILE}: {str(e)}")


# Define Request Data Schema matching raw CSV columns
class BatteryDataInput(BaseModel):
    Car_Model: str = Field(..., example="Tesla Model 3")
    Battery_Type: str = Field(..., example="NMC")
    Battery_Capacity_kWh: float = Field(..., example=75.0)
    Vehicle_Age_Months: int = Field(..., example=41)
    Total_Charging_Cycles: int = Field(..., example=390)
    Avg_Temperature_C: float = Field(..., example=21.5)
    Fast_Charge_Ratio: float = Field(..., example=0.51)
    Avg_Discharge_Rate_C: float = Field(..., example=2.22)
    Driving_Style: str = Field(..., example="Aggressive")
    Internal_Resistance_Ohm: float = Field(..., example=0.0362)


class BatchBatteryDataInput(BaseModel):
    data: List[BatteryDataInput]


class PredictionOutput(BaseModel):
    predicted_SoH_Percent: float


class BatchPredictionOutput(BaseModel):
    predictions: List[float]


@app.get("/")
def health_check():
    return {
        "status": "online",
        "model_loaded": model_name,
        "features_expected": num_cols + cat_cols,
    }


@app.post("/predict", response_model=PredictionOutput)
def predict_soh(input_data: BatteryDataInput):
    try:
        # Convert Pydantic request model to Pandas DataFrame
        input_dict = input_data.model_dump()
        input_df = pd.DataFrame([input_dict])

        # Generate prediction using the loaded pipeline
        prediction = model_pipeline.predict(input_df)[0]

        return PredictionOutput(predicted_SoH_Percent=round(float(prediction), 2))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


@app.post("/predict_batch", response_model=BatchPredictionOutput)
def predict_soh_batch(batch_input: BatchBatteryDataInput):
    try:
        # Convert list of inputs to DataFrame
        input_dicts = [item.model_dump() for item in batch_input.data]
        input_df = pd.DataFrame(input_dicts)

        # Generate batch predictions
        predictions = model_pipeline.predict(input_df)
        formatted_preds = [round(float(p), 2) for p in predictions]

        return BatchPredictionOutput(predictions=formatted_preds)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)