# Phase 6 — Model Evaluation and Analysis

## Objective and scope

This phase evaluates the 15-minute-ahead traffic-volume forecasting work for the selected NYC traffic series. The analysis is limited to the selected segments and the March 4–22, 2021 project period; it does not establish performance for all NYC roads or other dates.

The forecasting series are the four `SegmentID` + `Direction` combinations:

| Segment ID | Direction |
| ---: | :--- |
| 157501 | SB |
| 177615 | EB |
| 177615 | WB |
| 191114 | NB |

Segment `177615` is treated as two separate directional series.

## Evaluation setup

The existing final-evaluation notebook uses the prepared chronological splits:

| Split | Rows |
| :--- | ---: |
| Train | 4,565 |
| Validation | 978 |
| Test | 979 |
| Final training data (train + validation) | 5,543 |

The target is `target_15min`. The Random Forest predictors are `Vol`, `lag_15`, `lag_30`, `lag_60`, `lag_120`, `lag_1day`, `hour`, `day_of_week`, `SegmentID`, and `Direction`. Numeric predictors are passed through; `SegmentID` and `Direction` are one-hot encoded. The final Random Forest has 200 trees, `random_state=42`, and is fit on train + validation before evaluation on the held-out test split.

The model notebooks report MAE and RMSE. Lower values indicate smaller prediction errors. MAE describes average absolute error in vehicles; RMSE weights larger errors more heavily.

## Validation comparison

The validation metrics recorded in the model notebooks and calculated for the
same-time-yesterday baseline are:

| Model | MAE (vehicles) | RMSE (vehicles) |
| :--- | ---: | ---: |
| Persistence | 13.846626 | 19.097318 |
| Linear Regression | 12.441580 | 17.204182 |
| Random Forest | 11.809888 | 16.488574 |
| Same-time yesterday | 14.914110 | 20.629857 |

For the same-time-yesterday baseline, each `target_15min` forecast is matched to
`Vol` at the exact timestamp 24 hours before the target, within the same
SegmentID + Direction series. All 978 validation rows had a match exactly 96
observations earlier. Random Forest has the lowest MAE and RMSE among these
validation comparisons. These validation results are not a substitute for
held-out test performance.

## Final held-out test results

The final evaluation notebook reports Random Forest metrics after training on
train + validation. The same-time-yesterday baseline is also evaluated on the
existing held-out test split:

| Model | MAE (vehicles) | RMSE (vehicles) |
| :--- | ---: | ---: |
| Random Forest | 9.994035 | 13.679209 |
| Same-time yesterday | 22.546476 | 33.980542 |

All 979 test rows had an exact same-series observation 24 hours before the
forecast target, corresponding to 96 observations earlier. The test comparison
shows lower error for Random Forest than for the same-time-yesterday baseline.
The repository still does not report final test metrics for Persistence or
Linear Regression, so those models cannot be ranked on the test set.

### Test performance by series

| Segment ID | Direction | MAE (vehicles) | RMSE (vehicles) |
| ---: | :--- | ---: | ---: |
| 157501 | SB | 12.770185 | 17.461320 |
| 177615 | EB | 8.446837 | 11.275240 |
| 177615 | WB | 7.768902 | 10.518993 |
| 191114 | NB | 11.021959 | 14.390230 |

Performance varies across the selected series. The lowest recorded MAE is for 177615 WB, and the highest is for 157501 SB.

## Interpretation and limitations

For the selected series and period, the recorded results indicate that recent
traffic-volume and time information were useful for 15-minute-ahead prediction.
Random Forest had lower validation MAE/RMSE than Persistence, Linear Regression,
and the same-time-yesterday baseline, and lower held-out test error than the
same-time-yesterday baseline. This is a bounded finding about this experiment,
not evidence of performance on other NYC roads or periods.

Important limitations and reproducibility notes:

- The data has incomplete coverage and missing timestamp intervals. A row-based lag may not always correspond to its nominal elapsed-time lag when there is a gap.
- The same-time-yesterday baseline is implemented in the Phase 6 evaluation
  notebook and evaluated on the existing validation and test splits; Persistence
  and Linear Regression still have no reported final test metrics.
- `data/train.csv`, `data/validation.csv`, and `data/test.csv` are currently
  tracked in Git and are available to a fresh clone. `.gitignore` contains a
  general `*.csv` rule, but that does not affect files already tracked by Git.
  The remaining reproducibility limitation is that no tracked preprocessing
  script or notebook has been established that regenerates these exact prepared
  splits from the raw subset.
- The Stage 6 error-analysis cells in the evaluation notebook calculate additional signed-error, percentile, and forecast-hour summaries when executed. Those summaries are not included here because the notebook has not been run in the current environment to generate and verify them.

## Conclusion

The Random Forest achieved the best recorded validation metrics among the
implemented comparisons, with a held-out test MAE of 9.994035 vehicles and RMSE
of 13.679209 vehicles. On the test split it also had lower error than the
same-time-yesterday baseline (MAE 22.546476; RMSE 33.980542). Its errors were not
uniform across the four directional series. Results support continued use of
the approach for this focused project dataset, while missing reproducibility
steps and the absence of test metrics for Persistence and Linear Regression
limit broader comparisons.

## Source files

- Model validation results: [phase_4_random_forest.ipynb](../notebooks/phase_4_random_forest.ipynb)
- Model test results: [phase_5_final_evaluation.ipynb](../notebooks/phase_5_final_evaluation.ipynb)
- Expanded evaluation workflow, plots, and error-analysis cells: [phase_6_evaluation_analysis.ipynb](../notebooks/phase_6_evaluation_analysis.ipynb)
- Dataset scope and EDA: [phase-2-data-exploration.md](./phase-2-data-exploration.md)
