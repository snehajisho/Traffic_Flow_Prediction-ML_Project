# Phase 1: Task Definition

## Project
Machine Learning for Traffic Flow Prediction in Urban Areas

## Forecasting Task

Predict vehicle volume 15 minutes ahead for each of the three specified NYC road segments.

The target variable is numeric traffic volume (`Vol`), so this is formulated as a regression/forecasting problem rather than a classification problem.

## Project Scope

The analysis is limited to:
- The three road segments provided in the dataset
- The available period from March 4 to March 22, 2021
- 15-minute traffic volume observations

The project will not make claims about traffic conditions across all NYC roads.

## Planned Features

Potential predictors include:
- Traffic volume lagged by 15 minutes
- Traffic volume lagged by 30 minutes
- Traffic volume lagged by 60 minutes
- Traffic volume lagged by 120 minutes
- Hour of day
- Day of week
- Optional cyclical hour features using sine and cosine transformations

Lag features will be created separately for each road segment after sorting observations chronologically.

## Planned Models

### Baselines
1. Persistence baseline: predict the next volume using the current volume.
2. Same-time-yesterday baseline: use the volume from 24 hours earlier.

### Machine Learning Models
1. Linear Regression
2. Random Forest Regressor

## Evaluation

Models will be evaluated using:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

Performance will be reported:
- Overall
- Separately for each road segment

Actual versus predicted values will also be visualized.

## Validation Strategy

The data will be split chronologically into training, validation, and final test periods.

Random shuffling will not be used because this is a time-series forecasting problem.

## Phase 1 Completion Criteria

Phase 1 is complete when:
- The 15-minute-ahead numeric forecasting target is defined.
- The project scope is established.
- The regression formulation is established.
- Planned features and models are documented.
- MAE and RMSE are selected as evaluation metrics.
- Chronological train/validation/test splitting is established.
