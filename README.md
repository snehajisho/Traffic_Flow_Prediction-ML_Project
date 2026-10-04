# TRAFFIC FLOW PREDICTION

**Course:** Machine Learning  (UE24CS352A)
**Students:**

- Sneha Angelin Jisho - PES2UG24CS507
- Taran S -  PES2UG24CS555

---

## Project Description

This project focuses on **short-term traffic volume forecasting in urban areas using machine learning**.

The goal is to predict vehicle volume **15 minutes into the future** using recent traffic-volume observations and time-based information. The project uses traffic data from selected NYC road segments and evaluates several forecasting approaches, including simple baseline methods, Linear Regression, and Random Forest Regression.

The forecasting dataset contains traffic-volume measurements recorded at **15-minute intervals**. Features include recent traffic-volume lags, time of day, day of week, and segment/direction information.

The models are evaluated using a **chronological train/validation/test split** to preserve the time-series nature of the problem. Model performance is assessed using **Mean Absolute Error (MAE)** and **Root Mean Squared Error (RMSE)**, both overall and separately for each segment-direction series.

The project is limited to the provided road segments and time period. Since the dataset contains traffic volume rather than speed or road capacity, the project focuses on **traffic-volume forecasting rather than directly predicting traffic congestion**.

---

## Repository Structure

```text
Traffic_Flow_Prediction-ML_Project/
│
├── data/
│   ├── traffic_forecasting_subset.csv
│   ├── traffic_forecasting_features.csv
│   ├── traffic_forecasting_modeling.csv
│   ├── train.csv
│   ├── validation.csv
│   ├── test.csv
│   ├── random_forest_validation_results.csv
│   └── random_forest_segment_validation_results.csv
│
├── notebooks/
│   ├── phase_3_linear_regression.ipynb
│   ├── phase_4_random_forest.ipynb
│   └── phase_5_final_evaluation.ipynb
│
├── reports/
│
├── requirements.txt
└── .gitignore
```

---

## Setup

### 1. Clone the repository

```bash
git clone [REPOSITORY URL]
cd Traffic_Flow_Prediction-ML_Project
```

### 2. Create a virtual environment

It is recommended to use a separate Python virtual environment for the project.

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

### 4. Install the required packages

```bash
pip install -r requirements.txt
```

### 5. Start Jupyter

From the project root:

```bash
cd notebooks
jupyter notebook
```

Alternatively, JupyterLab can be used:

```bash
jupyter lab
```

If using JupyterLab from the project root, open the notebooks from the `notebooks/` folder.

---

## Running the Project

The main modeling workflow is organized into notebooks.

### 1. Linear Regression

Open:

```text
notebooks/phase_3_linear_regression.ipynb
```

This notebook:

- Loads the training and validation datasets.
- Defines the forecasting features.
- Encodes segment and direction information.
- Trains a Linear Regression model.
- Evaluates the model using MAE and RMSE.
- Compares the model against the persistence baseline.

### 2. Random Forest

Open:

```text
notebooks/phase_4_random_forest.ipynb
```

This notebook:

- Uses the same forecasting features.
- Trains a Random Forest Regressor.
- Evaluates performance on the validation set.
- Compares Random Forest against Linear Regression and the persistence baseline.
- Produces validation results overall and by segment-direction.

### 3. Final Evaluation

Open:

```text
notebooks/phase_5_final_evaluation.ipynb
```

This notebook:

- Combines the training and validation data.
- Retrains the selected Random Forest model.
- Evaluates the final model on the held-out test set.
- Calculates overall MAE and RMSE.
- Calculates performance separately for each segment-direction series.
- Produces actual-vs-predicted plots.

---

## Reproducibility

To reproduce the analysis:

1. Clone the repository.
2. Create and activate the virtual environment.
3. Install the dependencies from `requirements.txt`.
4. Start Jupyter.
5. Run the notebooks in the `notebooks/` directory.
6. Ensure that the required CSV files are available in the `data/` directory.

The forecasting workflow uses chronological data splits rather than random shuffling so that future observations are not used when training models for earlier periods.

---

## Evaluation Metrics

The project uses two primary evaluation metrics:

**Mean Absolute Error (MAE)**
Measures the average absolute difference between predicted and actual traffic volume.

**Root Mean Squared Error (RMSE)**
Measures the square root of the average squared prediction error and gives greater weight to larger errors.

Both metrics are reported overall and separately for each segment-direction series.

---

## Scope and Limitations

This project focuses on the specific traffic segments and time period contained in the provided dataset.

Important limitations include:

- The dataset covers a relatively short time period.
- The analysis is limited to the selected road segments and directions.
- The target variable is traffic volume rather than speed, capacity, or a direct measure of congestion.
- External factors such as weather, traffic incidents, and other contextual variables are not included.
- The forecasting horizon is limited to 15 minutes.
- Results should not be interpreted as representative of all roads or traffic conditions in New York City.

---

## Authors

**Sneha Angelin Jisho**
PES2UG24CS507

**Taran S**
PES2UG24CS555

---

## Course Information

**Course:** Machine Learning (UE24CS352A)
**Academic Term:** SEM 5

