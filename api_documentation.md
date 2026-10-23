# EV Battery Health (SoH) Prediction API

This repository hosts the asynchronous RESTful API for serving real-time and batch predictions of Electric Vehicle (EV) battery State of Health ($\text{SoH}\%$).

---

## **Base URL**

```http
http://localhost:8000
```
*(Replace with server host IP address in production environments)*

---

## **API Endpoints**

### **1. Health Check & Model Metadata**
Check API operational status and retrieve expected feature metadata.

* **URL:** `/`
* **Method:** `GET`
* **Headers:** `Content-Type: application/json`

#### **Response (`200 OK`)**
```json
{
  "status": "online",
  "model_loaded": "XGBoost",
  "features_expected": [
    "Battery_Capacity_kWh",
    "Vehicle_Age_Months",
    "Total_Charging_Cycles",
    "Avg_Temperature_C",
    "Fast_Charge_Ratio",
    "Avg_Discharge_Rate_C",
    "Internal_Resistance_Ohm",
    "Car_Model",
    "Battery_Type",
    "Driving_Style"
  ]
}
```

---

### **2. Single Battery Prediction**
Predicts the battery State of Health ($\text{SoH}\%$) for a single vehicle record.

* **URL:** `/predict`
* **Method:** `POST`
* **Headers:** `Content-Type: application/json`

#### **Request Body**
```json
{
  "Car_Model": "Tesla Model 3",
  "Battery_Type": "NMC",
  "Battery_Capacity_kWh": 75.0,
  "Vehicle_Age_Months": 41,
  "Total_Charging_Cycles": 390,
  "Avg_Temperature_C": 21.5,
  "Fast_Charge_Ratio": 0.51,
  "Avg_Discharge_Rate_C": 2.22,
  "Driving_Style": "Aggressive",
  "Internal_Resistance_Ohm": 0.0362
}
```

#### **Response (`200 OK`)**
```json
{
  "predicted_SoH_Percent": 94.60
}
```

#### **Error Response (`400 Bad Request`)**
```json
{
  "detail": "Prediction error: [Validation or Missing Field Error details]"
}
```

---

### **3. Batch Battery Prediction**
Predicts State of Health ($\text{SoH}\%$) for multiple vehicle telemetry records in a single payload.

* **URL:** `/predict_batch`
* **Method:** `POST`
* **Headers:** `Content-Type: application/json`

#### **Request Body**
```json
{
  "data": [
    {
      "Car_Model": "Tesla Model 3",
      "Battery_Type": "NMC",
      "Battery_Capacity_kWh": 75.0,
      "Vehicle_Age_Months": 41,
      "Total_Charging_Cycles": 390,
      "Avg_Temperature_C": 21.5,
      "Fast_Charge_Ratio": 0.51,
      "Avg_Discharge_Rate_C": 2.22,
      "Driving_Style": "Aggressive",
      "Internal_Resistance_Ohm": 0.0362
    },
    {
      "Car_Model": "Nissan Leaf",
      "Battery_Type": "LFP",
      "Battery_Capacity_kWh": 40.0,
      "Vehicle_Age_Months": 60,
      "Total_Charging_Cycles": 700,
      "Avg_Temperature_C": 28.0,
      "Fast_Charge_Ratio": 0.20,
      "Avg_Discharge_Rate_C": 1.50,
      "Driving_Style": "Moderate",
      "Internal_Resistance_Ohm": 0.0480
    }
  ]
}
```

#### **Response (`200 OK`)**
```json
{
  "predictions": [
    94.60,
    81.25
  ]
}
```

---

## **Interactive API Documentation**

An interactive OpenAPI interface (Swagger UI) is automatically available when running the application server:

* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc Interface:** `http://localhost:8000/redoc`