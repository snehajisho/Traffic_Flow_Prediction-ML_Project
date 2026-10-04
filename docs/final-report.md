# Machine Learning for Traffic Flow Prediction in Urban Areas

## 1. Introduction

### Problem context and motivation

Short-term traffic forecasts can help describe how vehicle volumes change over
time on urban roads. This project studies a focused set of New York City traffic
counting series and uses recent traffic observations and time information to
forecast near-term vehicle volume. The project predicts volume, not congestion:
the available data does not directly measure speed, road capacity, or a
congestion state.

### Research question

> Can recent traffic volumes and time information predict vehicle volume
> 15 minutes ahead on each of the selected NYC road segments?

### Project objective

The objective is to predict vehicle volume during the next 15-minute interval
(`target_15min`) for each selected `SegmentID` + `Direction` series, and to
evaluate the forecasts using mean absolute error (MAE) and root mean squared
error (RMSE).

## 2. Dataset and Scope

The project uses a filtered subset of NYC traffic-volume observations described
in the project files as traffic counts for selected road segments. The tracked
raw subset, [traffic_forecasting_subset.csv](../data/traffic_forecasting_subset.csv),
contains 6,910 observations and the fields `RequestID`, `Boro`, `Yr`, `M`, `D`,
`HH`, `MM`, `Vol`, `SegmentID`, `WktGeom`, `street`, `fromSt`, `toSt`, and
`Direction`. Observations span March 4 through March 22, 2021.

The analysis treats each combination of segment and direction as a separate
forecasting series:

| Segment ID | Direction | Raw observations |
| ---: | :--- | ---: |
| 157501 | SB | 1,728 |
| 177615 | EB | 1,728 |
| 177615 | WB | 1,727 |
| 191114 | NB | 1,727 |

Segment 177615 therefore contributes two distinct series, eastbound and
westbound. They are not combined.

The target `target_15min` represents the next 15-minute observation's vehicle
volume. Conclusions in this report apply only to these selected series and the
available period; they should not be generalized to all NYC roads or other
periods.

## 3. Exploratory Data Analysis

The raw subset has 6,910 rows across four segment-direction series. The EDA
notebook inspects the dataset structure and numeric summaries, constructs
timestamps, and visualizes traffic volume over time, by hour, and by day of
week. The observed mean volume differs substantially by series:

| Segment ID | Direction | Mean volume | Minimum | Maximum |
| ---: | :--- | ---: | ---: | ---: |
| 157501 | SB | 173.62 | 11 | 387 |
| 177615 | EB | 75.31 | 4 | 199 |
| 177615 | WB | 66.21 | 2 | 165 |
| 191114 | NB | 158.63 | 8 | 341 |

The EDA reports no missing volume values after numeric preparation. Its saved
timestamp-interval check finds 6,906 consecutive within-series intervals, all
15 minutes long. The duplicate check reports zero duplicates for the key
`SegmentID` + `Direction` + `timestamp`.

Traffic volume varies over time, by hour, and across the selected
segment-direction series. The EDA includes hourly and day-of-week summaries and
plots, but this report does not assert a particular weekday or hourly effect
beyond those documented observations. The individual series have unequal row
counts and less than the theoretical number of observations for 19 complete
days, so the dataset does not provide full-period coverage for every series.

These findings informed the forecasting design: preserve each directional
series independently, construct time-aware features, retain chronological
ordering, and evaluate on later observations rather than using a randomly
shuffled split.

## 4. Feature Engineering and Data Preparation

The project EDA combines `Yr`, `M`, `D`, `HH`, and `MM` into a timestamp and
converts `Vol` to a numeric value. The tracked
[traffic_forecasting_features.csv](../data/traffic_forecasting_features.csv)
contains the derived timestamp, lag features, target, hour, and day-of-week
fields. The model notebooks use the following features:

- Current volume: `Vol`
- Lagged volumes: `lag_15`, `lag_30`, `lag_60`, `lag_120`, and `lag_1day`
- Time information: `hour` and `day_of_week`
- Series identity: `SegmentID` and `Direction` as categorical inputs

The target is `target_15min`. Linear Regression and Random Forest both include
the numeric volume/time features and one-hot encoded `SegmentID` and
`Direction`. The persistence and same-time-yesterday methods use their
respective baseline definitions rather than fitted model features.

The tracked prepared modeling data contains 6,522 rows. It is represented by
chronological train, validation, and test files with 4,565, 978, and 979 rows,
respectively. The existing split files are used as prepared; no random
shuffling or replacement split is introduced in the evaluation.

The EDA found that consecutive retained timestamps are 15 minutes apart, while
the series have unequal counts and incomplete coverage across the project
period. A row-based lag is an elapsed-time lag only when the corresponding
observations are continuous. Any missing timestamp inside a series would make
a row shift differ from the named elapsed-time lag; this remains a limitation
to keep in mind when interpreting the prepared lag variables.

The prepared split CSVs are tracked in Git. However, the repository does not
establish a tracked preprocessing script or notebook that regenerates these
exact features and split boundaries from the raw subset.

## 5. Forecasting Methods

All methods predict `target_15min`.

### Persistence

Persistence predicts the next interval's volume using the current row's
observed `Vol`. It is a simple reference forecast requiring no model fitting.

### Same-time yesterday

For each target timestamp, this baseline uses the observed volume exactly 24
hours earlier, matched within the same `SegmentID` + `Direction` series. At the
15-minute observation frequency, the matched observation is 96 observations
earlier. The evaluation code verifies this correspondence for validation and
test rows.

### Linear Regression

Linear Regression provides a fitted linear benchmark. It uses `Vol`, the
prepared lag features, `hour`, and `day_of_week`; `SegmentID` and `Direction`
are one-hot encoded. For final test evaluation it is fit on the existing train
+ validation data and evaluated on the held-out test data. No hyperparameter
tuning is claimed.

### Random Forest

Random Forest provides a nonlinear regression comparison using the same
numeric volume/time features and one-hot encoded `SegmentID` and `Direction`.
The final evaluation uses 200 trees, `random_state=42`, and `n_jobs=-1`, fitting
on train + validation before predicting the held-out test set. No hyperparameter
tuning is claimed.

## 6. Validation Results

The validation comparison uses the existing 978-row validation split. The
Persistence, Linear Regression, and Random Forest figures are recorded in the
model notebooks/result CSV; the same-time-yesterday metrics are calculated by
the Phase 6 evaluation workflow.

| Method | MAE (vehicles) | RMSE (vehicles) |
| :--- | ---: | ---: |
| Persistence | 13.846626 | 19.097318 |
| Linear Regression | 12.441580 | 17.204182 |
| Random Forest | 11.809888 | 16.488574 |
| Same-time yesterday | 14.914110 | 20.629857 |

Random Forest has the lowest recorded validation MAE and RMSE among these four
methods.

## 7. Final Held-Out Test Results

The final comparison evaluates every method against `target_15min` on the same
979 held-out test rows. Persistence uses the current row's volume;
Linear Regression is refit on train + validation with its existing feature
definitions and preprocessing; Random Forest follows the existing final
evaluation; and same-time yesterday uses the exact 24-hour-earlier value from
the same series.

| Method | Test rows | MAE (vehicles) | RMSE (vehicles) |
| :--- | ---: | ---: | ---: |
| Persistence | 979 | 12.602656 | 17.088486 |
| Linear Regression | 979 | 10.908557 | 14.867493 |
| Random Forest | 979 | 9.994035 | 13.679209 |
| Same-time yesterday | 979 | 22.546476 | 33.980542 |

Random Forest has the lowest recorded test MAE and RMSE among the four
evaluated methods in this experiment.

## 8. Segment-Level Test Performance

The final Random Forest evaluation reports the following held-out test metrics
by `SegmentID` + `Direction`:

| Segment ID | Direction | Test rows | MAE (vehicles) | RMSE (vehicles) |
| ---: | :--- | ---: | ---: | ---: |
| 157501 | SB | 243 | 12.770185 | 17.461320 |
| 177615 | EB | 245 | 8.446837 | 11.275240 |
| 177615 | WB | 246 | 7.768902 | 10.518993 |
| 191114 | NB | 245 | 11.021959 | 14.390230 |

The lowest recorded segment-level test MAE is for 177615 WB; the highest is for
157501 SB. The two directions of SegmentID 177615 remain separate throughout
the analysis.

## 9. Actual-versus-Predicted Analysis and Error Analysis

The Phase 5 final-evaluation notebook generates an overall actual-versus-
predicted plot and separate plots for each of the four test series. These
visualizations compare the held-out target values with Random Forest
predictions.

The Phase 6 notebook contains additional error-analysis code for signed error
(actual minus predicted), absolute and squared error, median absolute error,
the 90th percentile and maximum absolute error, segment-level summaries,
forecast-hour summaries, and the largest-error cases.

The Phase 6 notebook was not executed in the available environment: its code
cells have no saved execution counts or outputs. Therefore, those additional
error-analysis summaries are described here as implemented analysis code, not
as verified numerical findings. The model MAE/RMSE values reported in Sections
6–8 are distinct: they are present in recorded Phase 3–5 outputs and result
files, or independently calculated from the tracked CSVs for the Phase 6
baseline comparisons.

## 10. Discussion

On the validation split, Random Forest has lower MAE and RMSE than Persistence,
Linear Regression, and same-time yesterday. The held-out test results show the
same ordering for this experiment: Random Forest has the lowest error,
followed by Linear Regression, Persistence, and same-time yesterday.

The results suggest that the recent traffic history and time features used by
the fitted models provide useful information for predicting the next
15-minute volume in these selected series. Current and lagged volume describe
recent traffic levels, while hour and day-of-week encode temporal context.
These are plausible predictive inputs for this task; the results do not
establish which individual feature caused the performance differences.

The comparison is specific to four direction-series over the project period.
It does not establish universal superiority of Random Forest, nor performance
on other NYC roads, dates, or traffic conditions. The same-time-yesterday
baseline performs substantially worse than the other three methods on this
test split, but that observation is likewise limited to the evaluated data.

## 11. Limitations

- The analysis covers only four selected `SegmentID` + `Direction` series and
  the March 4–22, 2021 period.
- The observations provide incomplete coverage relative to 19 complete days;
  the four series have unequal counts. Although all consecutive timestamps
  recorded by the EDA are 15 minutes apart, row-based lag interpretation
  depends on continuity wherever timestamps may be missing.
- The project predicts vehicle volume, not speed, road capacity, or a direct
  congestion measure. Weather, incidents, construction, and special events
  are not included.
- No broader NYC-wide or future-period generalization follows from this
  focused evaluation.
- The Phase 6 error-analysis cells were not executed in the available
  environment, so their additional summaries do not have saved outputs and
  are not reported as numerical findings.
- The prepared split CSVs are tracked, but a tracked preprocessing script or
  notebook that regenerates the exact feature data and split boundaries from
  the raw subset has not been established.

## 12. Conclusion

For the selected NYC traffic series and March 2021 period, recent traffic
volumes and time information were useful for predicting vehicle volume
15 minutes ahead. Random Forest achieved the lowest recorded validation and
held-out test MAE/RMSE among the four evaluated methods. This conclusion is
limited to the dataset, series, split, and period examined; it does not imply
that the method will be superior on other roads or dates.

## 13. References and Project Files

This report is based on the project's own files:

- [Project definition](phase-1-project-definition.md)
- [Phase 2 data exploration documentation](phase-2-data-exploration.md)
- [Phase 2 EDA notebook](phase-2-eda-analysis.ipynb)
- [Phase 3 Linear Regression notebook](../notebooks/phase_3_linear_regression.ipynb)
- [Phase 4 Random Forest notebook](../notebooks/phase_4_random_forest.ipynb)
- [Phase 5 final evaluation notebook](../notebooks/phase_5_final_evaluation.ipynb)
- [Phase 6 evaluation and analysis notebook](../notebooks/phase_6_evaluation_analysis.ipynb)
- [Phase 6 evaluation documentation](phase-6-evaluation-analysis.md)
- [Raw traffic subset](../data/traffic_forecasting_subset.csv)
- [Prepared feature data](../data/traffic_forecasting_features.csv)
- [Prepared modeling data](../data/traffic_forecasting_modeling.csv)
- [Training split](../data/train.csv), [validation split](../data/validation.csv),
  and [test split](../data/test.csv)
- [Recorded Random Forest validation comparison](../data/random_forest_validation_results.csv)
- [Recorded Random Forest validation metrics by series](../data/random_forest_segment_validation_results.csv)
