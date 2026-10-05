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

### Features

The forecasting features include:

- Current traffic volume
- Lagged traffic volume at 15 minutes
- Lagged traffic volume at 30 minutes
- Lagged traffic volume at 60 minutes
- Lagged traffic volume at 120 minutes
- Lagged traffic volume from 1 day earlier
- Hour of day
- Day of week
- SegmentID
- Direction

The main feature columns are:

```text
Vol
lag_15
lag_30
lag_60
lag_120
lag_1day
hour
day_of_week
SegmentID
Direction
```

The prediction target is:

```text
target_15min
```

which represents the traffic volume 15 minutes ahead.

### Forecasting Approaches

The project evaluates four forecasting approaches:

1. Persistence baseline
2. Same-time-yesterday baseline
3. Linear Regression
4. Random Forest

The models are evaluated using a **chronological train/validation/test split** with no random shuffling.

Performance is assessed using:

- **Mean Absolute Error (MAE)**
- **Root Mean Squared Error (RMSE)**

Random Forest performance is also evaluated separately for each segment-direction series.

The project is limited to the provided road segments and time period. Since the dataset contains traffic volume rather than speed or road capacity, the project focuses on **traffic-volume forecasting rather than directly predicting traffic congestion**.

---

## Final Held-Out Test Results

All four methods are evaluated against the same **979 held-out test rows**.

Random Forest achieved the lowest MAE and RMSE in the final held-out test evaluation.

| Method | MAE (vehicles) | RMSE (vehicles) |
| :--- | ---: | ---: |
| Persistence | 12.602656 | 17.088486 |
| Linear Regression | 10.908557 | 14.867493 |
| Random Forest | **9.994035** | **13.679209** |
| Same-time yesterday | 22.546476 | 33.980542 |

### Result Summary

Random Forest produced the best overall performance among the four evaluated approaches:

- **MAE:** 9.994035 vehicles
- **RMSE:** 13.679209 vehicles

This indicates that the Random Forest model produced the lowest average absolute prediction error and the lowest root mean squared error on the held-out test set.

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

### 5. Run the preprocessing pipeline

From the project root:

```bash
python src/preprocessing.py
```

If `python` is not available as a system command, use:

```bash
.venv/bin/python src/preprocessing.py
```

On Windows, the equivalent virtual-environment Python executable can be used.

### 6. Start Jupyter

Because the notebooks use paths relative to the `notebooks/` directory, start Jupyter from that directory:

```bash
cd notebooks
jupyter notebook
```

Alternatively:

```bash
jupyter lab
```

Then open the required notebook.

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

or:

```bash
.venv/bin/python src/preprocessing.py
```

### Preprocessing Steps

The preprocessing pipeline performs the following steps:

1. Loads the filtered traffic dataset.
2. Creates a combined `timestamp` from the year, month, day, hour, and minute columns.
3. Converts traffic volume to numeric values.
4. Sorts observations by `SegmentID`, `Direction`, and timestamp for lag construction.
5. Creates calendar features:
   - `hour`
   - `day_of_week`
6. Creates lagged traffic-volume features for each SegmentID + Direction series:
   - `lag_15`
   - `lag_30`
   - `lag_60`
   - `lag_120`
   - `lag_1day`
7. Creates the 15-minute-ahead prediction target:
   - `target_15min`
8. Removes rows where required lag or target values are unavailable.
9. Saves the resulting feature dataset.
10. Sorts the complete feature dataset chronologically.
11. Creates chronological training, validation, and test datasets.

### Generated Files

The preprocessing script generates:

```text
data/traffic_forecasting_features.csv
data/train.csv
data/validation.csv
data/test.csv
```

The resulting feature dataset contains **6,522 usable rows** after lag and target construction.

The chronological split contains:

- **Training:** 4,565 rows
- **Validation:** 978 rows
- **Test:** 979 rows

### Chronological Split

The data is split chronologically to prevent future observations from being used to train models for earlier periods.

```text
Training:
2021-03-05 07:00:00 to 2021-03-17 04:30:00

Validation:
2021-03-17 04:45:00 to 2021-03-19 17:45:00

Test:
2021-03-19 17:45:00 to 2021-03-22 07:00:00
```

The split proportions are approximately:

```text
70% Training
15% Validation
15% Test
```

No random shuffling is performed.

---

## Running the Project

The modeling workflow is organized into sequential notebooks.

### Phase 3 — Linear Regression

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

### Phase 4 — Random Forest

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

### Phase 5 — Final Evaluation

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

The test set remains held out from the model-selection process until final evaluation.

---

### Phase 6 — Evaluation and Analysis

Open:

```text
notebooks/phase_6_evaluation_analysis.ipynb
```

Phase 6 extends the final evaluation by providing:

- Same-time-yesterday baseline
- Held-out test comparisons across all four methods
- Additional error analysis
- Further analysis of model errors
- Comparison of forecasting approaches using the final test set

The Phase 6 analysis is part of the completed project workflow and should be run after the final evaluation stage if reproducing the complete project from scratch.

---

## Reproducibility

The repository contains a tracked preprocessing script so that the prepared feature dataset and chronological data splits can be regenerated.

### 1. Clone the repository

```bash
git clone [REPOSITORY URL]
cd Traffic_Flow_Prediction-ML_Project
```

### 2. Create and activate the virtual environment

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

```bash
python -m venv .venv
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

### 5. Start Jupyter from the notebooks directory

```bash
cd notebooks
jupyter notebook
```

### 6. Run the notebooks in order

The recommended workflow is:

```text
Phase 3 — Linear Regression
        ↓
Phase 4 — Random Forest
        ↓
Phase 5 — Final Evaluation
        ↓
Phase 6 — Evaluation and Analysis
```

Corresponding files:

```text
notebooks/phase_3_linear_regression.ipynb
notebooks/phase_4_random_forest.ipynb
notebooks/phase_5_final_evaluation.ipynb
notebooks/phase_6_evaluation_analysis.ipynb
```

The preprocessing script and notebooks use the tracked project data and feature definitions, allowing the complete modeling workflow to be reproduced without manually recreating the feature-engineering process.

---

## Evaluation Metrics

The project uses two primary evaluation metrics.

### Mean Absolute Error (MAE)

MAE measures the average absolute difference between predicted and actual traffic volume.

```text
MAE = average(|actual - predicted|)
```

Lower MAE indicates that predictions are, on average, closer to the observed traffic volume.

### Root Mean Squared Error (RMSE)

RMSE measures the square root of the average squared prediction error.

```text
RMSE = sqrt(average((actual - predicted)^2))
```

RMSE gives greater weight to larger prediction errors than MAE.

Both metrics are used for comparing the forecasting approaches.

---

## Model Comparison

The final held-out test evaluation gives the following results:

| Rank | Method | MAE | RMSE |
| :---: | :--- | ---: | ---: |
| 1 | **Random Forest** | **9.994035** | **13.679209** |
| 2 | Linear Regression | 10.908557 | 14.867493 |
| 3 | Persistence | 12.602656 | 17.088486 |
| 4 | Same-time yesterday | 22.546476 | 33.980542 |

Random Forest provides the best overall test-set performance among the evaluated methods.

Compared with the persistence baseline, Random Forest reduces:

- MAE from **12.602656** to **9.994035**
- RMSE from **17.088486** to **13.679209**

The same-time-yesterday baseline performs substantially worse on this held-out test set.

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

## Project Workflow

The overall project workflow can be summarized as:

```text
Raw Traffic Dataset
        ↓
Filtered Dataset
        ↓
Feature Engineering
        ↓
Lag Features + Time Features
        ↓
15-Minute-Ahead Target
        ↓
Chronological Train / Validation / Test Split
        ↓
Linear Regression
        ↓
Random Forest
        ↓
Final Held-Out Test Evaluation
        ↓
Baseline Comparison + Error Analysis
        ↓
Final Results
```

---

## Key Findings

Based on the final held-out test evaluation:

1. **Random Forest achieved the best overall performance.**
2. **Linear Regression also outperformed the persistence baseline.**
3. **The persistence baseline provided a stronger benchmark than the same-time-yesterday baseline on this test period.**
4. **Same-time-yesterday produced the highest MAE and RMSE among the evaluated approaches.**
5. Recent traffic observations and time-based information provide useful information for 15-minute-ahead traffic-volume forecasting on the selected road segments.

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
