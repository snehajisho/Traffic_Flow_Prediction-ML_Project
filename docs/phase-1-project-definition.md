# Phase 1 — Project Definition

## 1. Project Title

**Machine Learning for Traffic Flow Prediction in Urban Areas**

## 2. Project Objective

The objective of this project is to use machine learning to predict **vehicle volume 15 minutes into the future** for selected road segments in New York City.

The prediction will be based primarily on recent traffic-volume observations and time-related information.

## 3. Research Question

> **Can recent traffic volumes and time information predict vehicle volume 15 minutes ahead on each of the selected NYC road segments?**

The project focuses on predicting a numerical traffic volume rather than directly classifying whether a road is congested.

## 4. Prediction Target

The target variable is:

**Vehicle volume (`Vol`) during the next 15-minute interval.**

For a given observation at time `t`, the model will attempt to predict:

**`Vol(t + 15 minutes)`**

For example, if the available traffic observation is at 8:00 AM, the model should predict the number of vehicles recorded during the 8:15 AM interval.

## 5. Dataset Scope

The project uses traffic-volume observations from selected NYC road segments.

The focused dataset covers the period:

**March 4, 2021 – March 22, 2021**

Traffic observations are recorded at approximately **15-minute intervals**.

The project is intentionally limited to the selected road segments and this time period rather than attempting to predict traffic across all NYC roads.

## 6. Selected Traffic Series

The dataset contains the following segment-direction series:

| Segment ID | Direction |
| ---------- | --------- |
| 157501     | SB        |
| 177615     | EB        |
| 177615     | WB        |
| 191114     | NB        |

Because Segment `177615` contains observations in both eastbound and westbound directions, the forecasting series are treated as **SegmentID + Direction** combinations.

This prevents observations from different traffic directions from being incorrectly treated as one continuous traffic series.

## 7. Main Variables

The dataset contains information including:

* `SegmentID` — identifies the road segment
* `Direction` — identifies the traffic direction
* `Vol` — recorded vehicle volume
* `Yr` — year
* `M` — month
* `D` — day
* `HH` — hour
* `MM` — minute
* `Boro` — borough
* `street` — street associated with the segment
* `fromSt` — starting/reference street
* `toSt` — ending/reference street
* `WktGeom` — geographic geometry information

The date and time fields will be combined into a single timestamp for forecasting and time-based analysis.

## 8. Planned Input Features

The project will investigate whether recent traffic history and time information can predict future traffic volume.

Potential features include:

* Previous 15-minute volume
* Previous 30-minute volume
* Previous 60-minute volume
* Previous 120-minute volume
* Hour of the day
* Day of the week
* Other time-derived features where appropriate

Lag features will be created separately for each SegmentID + Direction series.

## 9. Planned Models and Baselines

The project will compare machine-learning models against simple forecasting baselines.

### Baseline 1 — Persistence

The next traffic volume is predicted to be equal to the current traffic volume.

> `Prediction = Current Volume`

### Baseline 2 — Same Time Yesterday

The prediction uses the traffic volume observed approximately 24 hours earlier.

### Model 1 — Linear Regression

A linear regression model will be used as a simple machine-learning benchmark.

### Model 2 — Random Forest Regressor

A modest random forest regression model will be used to investigate whether a nonlinear model can improve prediction performance.

## 10. Train, Validation, and Test Strategy

Because this is a time-series forecasting problem, observations will be split **chronologically**.

The data will not be randomly shuffled before splitting.

Earlier observations will be used for training, while later observations will be reserved for validation and/or testing.

This prevents information from the future from being used to predict the past.

## 11. Evaluation Metrics

Model performance will be evaluated using:

### Mean Absolute Error (MAE)

MAE measures the average absolute difference between the predicted and actual vehicle volumes.

### Root Mean Squared Error (RMSE)

RMSE measures prediction error while giving greater weight to larger errors.

Performance will be evaluated:

* Overall
* Separately for each SegmentID + Direction series
* Across the different forecasting approaches

Actual-versus-predicted visualizations will also be used to assess model behavior.

## 12. Project Workflow

The overall project will follow these stages:

1. **Define the forecasting task**
2. **Inspect and understand the data**
3. **Prepare the forecasting dataset**
4. **Create a chronological train/validation/test split**
5. **Establish baseline forecasts**
6. **Train and compare machine-learning models**
7. **Evaluate predictions on held-out test data**
8. **Interpret the results**
9. **Document limitations**
10. **Prepare the final project report and submission**

## 13. Project Limitations Identified at This Stage

The available data primarily contains traffic volume and road-segment information.

The dataset does not provide all factors that can influence traffic conditions, such as:

* Vehicle speed
* Road capacity
* Weather conditions
* Traffic incidents
* Construction
* Special events
* Detailed real-time road conditions

Therefore, this project focuses specifically on **short-term vehicle-volume prediction** rather than attempting to model every factor affecting urban traffic congestion.

## 14. Expected Outcome

The final project will determine whether recent traffic-volume history and time-related features can provide useful predictions of vehicle volume 15 minutes ahead for the selected NYC road segments.

The final conclusions will be based on model performance on held-out test data. No model-performance claims are made at this stage.
