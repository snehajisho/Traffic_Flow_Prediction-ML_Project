# TRAFFIC FLOW PREDICTION

**Course:** Machine Learning (UE24CS352A)

**Students:**

- Sneha Angelin Jisho - PES2UG24CS507
- Taran S - PES2UG24CS555

---

## Project Description

This project focuses on **short-term traffic volume forecasting in urban areas using machine learning**.

The goal is to predict vehicle volume **15 minutes into the future** (`target_15min`) using recent traffic-volume observations and time-based information.

The research question is:

> Can recent traffic volumes and time information predict vehicle volume 15 minutes ahead on each selected NYC road segment?

The filtered dataset contains **6,910 observations** from March 4–22, 2021, across four SegmentID + Direction series:

- 157501 SB
- 177615 EB
- 177615 WB
- 191114 NB

Segment 177615 is treated as two separate directional series.

The forecasting features include:

- Current traffic volume
- Lagged traffic volumes at 15, 30, 60, and 120 minutes
- Lagged traffic volume from 1 day earlier
- Hour of day
- Day of week
- SegmentID
- Direction

The project evaluates four forecasting approaches:

1. Persistence baseline
2. Same-time-yesterday baseline
3. Linear Regression
4. Random Forest

The models are evaluated using a **chronological train/validation/test split** with no random shuffling. Performance is assessed using **Mean Absolute Error (MAE)** and **Root Mean Squared Error (RMSE)**.

Random Forest performance is also reported separately for each segment-direction series.

The project is limited to the provided road segments and time period. Since the dataset contains traffic volume rather than speed or road capacity, the project focuses on **traffic-volume forecasting rather than directly predicting traffic congestion**.

---

## Final Held-Out Test Results

All four methods are evaluated against the same **979 held-out test rows**. Random Forest achieved the lowest MAE and RMSE in this experiment.

| Method | MAE (vehicles) | RMSE (vehicles) |
| :--- | ---: | ---: |
| Persistence | 12.602656 | 17.088486 |
| Linear Regression | 10.908557 | 14.867493 |
| Random Forest | 9.994035 | 13.679209 |
| Same-time yesterday | 22.546476 | 33.980542 |

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
├── docs/
│   ├── phase-1-project-definition.md
│   ├── phase-2-data-exploration.md
│   ├── phase-2-eda-analysis.ipynb
│   ├── phase-6-evaluation-analysis.md
│   └── final-report.md
│
├── notebooks/
│   ├── phase_3_linear_regression.ipynb
│   ├── phase_4_random_forest.ipynb
│   ├── phase_5_final_evaluation.ipynb
│   └── phase_6_evaluation_analysis.ipynb
│
├── reports/
│   └── phase_1_task_definition.md
│
├── src/
│   └── preprocessing.py
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
jupyter notebook
```

Alternatively:

```bash
jupyter lab
```

If using Jupyter from the project root, open the notebooks from the `notebooks/` folder.

---

## Data and Preprocessing

The preprocessing workflow is implemented in:

```text
src/preprocessing.py
```

The script takes the tracked filtered traffic dataset:

```text
data/traffic_forecasting_subset.csv
```

and generates the feature dataset and chronological train/validation/test splits used by the modeling notebooks.

Run the preprocessing pipeline from the project root with:

```bash
python src/preprocessing.py
```

If `python` is not available as a system command, use the Python executable from the virtual environment:

```bash
.venv/bin/python src/preprocessing.py
```

The preprocessing pipeline performs the following steps:

1. Loads the filtered traffic dataset.
2. Sorts observations chronologically.
3. Processes observations by `SegmentID` and `Direction`.
4. Creates the `timestamp` variable.
5. Creates lagged traffic-volume features:
   - `lag_15`
   - `lag_30`
   - `lag_60`
   - `lag_120`
   - `lag_1day`
6. Creates the 15-minute-ahead target:
   - `target_15min`
7. Creates calendar features:
   - `hour`
   - `day_of_week`
8. Removes rows that cannot be used because required lag or target values are unavailable.
9. Saves the resulting feature dataset to:

```text
data/traffic_forecasting_features.csv
```

10. Creates chronological training, validation, and test datasets:

```text
data/train.csv
data/validation.csv
data/test.csv
```

The resulting feature dataset contains **6,522 usable rows** after lag and target construction.

The chronological split contains:

- **Training:** 4,565 rows
- **Validation:** 978 rows
- **Test:** 979 rows

The split is performed in chronological order:

```text
Training:
2021-03-05 07:00:00 to 2021-03-17 04:30:00

Validation:
2021-03-17 04:45:00 to 2021-03-19 17:45:00

Test:
2021-03-19 17:45:00 to 2021-03-22 07:00:00
```

This prevents future observations from being used to train models for earlier periods.

---

## Running the Project

The main modeling workflow is organized into notebooks.

### 1. Preprocessing

Run:

```text
src/preprocessing.py
```

This should be run before the modeling notebooks if the prepared datasets need to be regenerated.

The script creates the feature dataset and chronological train/validation/test splits.

---

### 2. Linear Regression

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

---

### 3. Random Forest

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

---

### 4. Final Evaluation

Open:

```text
notebooks/phase_5_final_evaluation.ipynb
```

This notebook:

- Combines the training and validation data.
- Retrains the selected Random Forest model.
- Evaluates the final Random Forest model on the held-out test set.
- Calculates overall MAE and RMSE.
- Calculates performance separately for each segment-direction series.
- Produces actual-vs-predicted plots.

---

### 5. Extended Evaluation

Open:

```text
notebooks/phase_6_evaluation_analysis.ipynb
```

This notebook includes:

- The same-time-yesterday baseline
- Held-out test comparisons for all four methods
- Additional error-analysis code
- Further analysis of model errors

The Phase 6 error-analysis cells were not executed in the available environment and do not have saved outputs. Therefore, no unverified error-analysis numbers are reported in the project.

---

## Reproducibility

The repository contains a tracked preprocessing script so that the prepared feature dataset and chronological data splits can be regenerated.

To reproduce the project:

### 1. Clone the repository

```bash
git clone [REPOSITORY URL]
cd Traffic_Flow_Prediction-ML_Project
```

### 2. Create and activate the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run preprocessing

From the project root:

```bash
python src/preprocessing.py
```

or:

```bash
.venv/bin/python src/preprocessing.py
```

This regenerates:

```text
data/traffic_forecasting_features.csv
data/train.csv
data/validation.csv
data/test.csv
```

### 5. Run the modeling notebooks

Open the notebooks in:

```text
notebooks/
```

and execute them in order.

The recommended order is:

```text
phase_3_linear_regression.ipynb
        ↓
phase_4_random_forest.ipynb
        ↓
phase_5_final_evaluation.ipynb
        ↓
phase_6_evaluation_analysis.ipynb
```

The preprocessing script and notebooks use the same tracked data files and feature definitions, allowing the modeling workflow to be reproduced without manually recreating the feature-engineering steps.

---

## Evaluation Metrics

The project uses two primary evaluation metrics.

### Mean Absolute Error (MAE)

MAE measures the average absolute difference between predicted and actual traffic volume.

Lower MAE indicates that predictions are, on average, closer to the observed traffic volume.

### Root Mean Squared Error (RMSE)

RMSE measures the square root of the average squared prediction error.

RMSE gives greater weight to larger prediction errors than MAE.

Both MAE and RMSE are reported for the final evaluation.

Random Forest results are also reported separately for each segment-direction series.

---

## Scope and Limitations

This project focuses on the specific traffic segments and time period contained in the provided dataset.

Important limitations include:

- The dataset covers a relatively short time period.
- The analysis is limited to the selected road segments and directions.
- Incomplete timestamp coverage means row-based lags may not always correspond to their nominal elapsed-time intervals when timestamps are missing.
- The target variable is traffic volume rather than speed, capacity, or a direct measure of congestion.
- External factors such as weather, traffic incidents, road closures, and other contextual variables are not included.
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
