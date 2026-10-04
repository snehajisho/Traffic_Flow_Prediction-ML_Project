# Phase 2 — Data Exploration and Understanding

## 1. Objective

Phase 2 focused on inspecting and understanding the traffic-volume dataset before creating forecasting features or training machine-learning models.

The purpose of this phase was to understand the structure and quality of the selected traffic series, identify any data-quality issues, and explore how traffic volume changes over time and across days of the week.

## 2. Dataset Used

The analysis uses the filtered traffic dataset containing observations for the selected NYC road segments during the focused project period:

**March 4, 2021 – March 22, 2021**

The filtered dataset contains **6,910 observations** across four segment-direction traffic series.

The original dataset contains the following fields:

- `RequestID`
- `Boro`
- `Yr`
- `M`
- `D`
- `HH`
- `MM`
- `Vol`
- `SegmentID`
- `WktGeom`
- `street`
- `fromSt`
- `toSt`
- `Direction`

## 3. Timestamp Preparation

The separate date and time columns (`Yr`, `M`, `D`, `HH`, and `MM`) were combined to create a single `timestamp` variable.

This timestamp is required for chronological analysis and will also be used later when creating time-based forecasting features.

The `Vol` column was converted to a numeric data type so that it could be used for statistical analysis and machine-learning models.

## 4. Traffic Series

The selected data contains four meaningful SegmentID + Direction combinations:

| Segment ID | Direction | Observations |
|---|---|---:|
| 157501 | SB | 1,728 |
| 177615 | EB | 1,728 |
| 177615 | WB | 1,727 |
| 191114 | NB | 1,727 |

Segment `177615` appears in both eastbound and westbound directions. Therefore, the project treats **SegmentID + Direction** as the individual forecasting series.

This prevents observations from opposite traffic directions from being treated as one continuous series.

## 5. Data Quality Checks

### Missing Volume Values

The `Vol` values were converted to numeric values and checked for missing values.

No missing `Vol` values were identified in the selected dataset after conversion.

### Duplicate Observations

Duplicate observations were checked using the combination of:

- `SegmentID`
- `Direction`
- `timestamp`

This combination identifies an individual traffic-volume observation within a forecasting series.

### Timestamp Intervals

The timestamps were sorted separately for each SegmentID + Direction series and the differences between consecutive observations were inspected.

The data is intended to represent traffic observations at approximately **15-minute intervals**. The selected series do not all contain the full theoretical number of observations for 19 complete days, indicating that some observations are missing or that coverage is incomplete.

This needs to be considered when creating lag features in Phase 3. A simple row-based shift should only be interpreted as a 15-minute lag when the underlying timestamps are continuous.

## 6. Traffic Volume Summary

The observed traffic-volume statistics for the four series were:

| Segment ID | Direction | Mean | Minimum | Maximum |
|---|---|---:|---:|---:|
| 157501 | SB | 173.62 | 11 | 387 |
| 177615 | EB | 75.31 | 4 | 199 |
| 177615 | WB | 66.21 | 2 | 165 |
| 191114 | NB | 158.63 | 8 | 341 |

These values show that traffic volume differs substantially between the selected road-direction series.

## 7. Traffic Volume Over Time

Traffic volume was plotted against the constructed timestamp for each SegmentID + Direction combination.

The time-series plots provide an overview of how vehicle volume changes throughout the selected period and allow potential changes in traffic patterns, peaks, and lower-volume periods to be observed.

The plots were created separately for:

- Segment 157501 — SB
- Segment 177615 — EB
- Segment 177615 — WB
- Segment 191114 — NB

## 8. Traffic Volume by Day of Week

The day of the week was derived from the timestamp.

Average traffic volume was then calculated for each day of the week separately for each SegmentID + Direction series.

The days were ordered as:

**Monday → Tuesday → Wednesday → Thursday → Friday → Saturday → Sunday**

This analysis was used to investigate whether traffic volume differs depending on the day of the week.

Day-of-week information may later be used as a predictive feature because traffic patterns can vary between weekdays and weekends.

## 9. Key Findings

The main findings from the exploratory analysis are:

1. The focused dataset contains four meaningful traffic series when SegmentID and Direction are considered together.
2. Traffic volume varies considerably between the selected road-direction series.
3. Traffic volume changes over time and is not constant throughout the observation period.
4. Day-of-week analysis provides a way to examine differences between weekday and weekend traffic patterns.
5. The traffic data is based on approximately 15-minute observations, but the selected series do not all contain every theoretically possible observation.
6. Timestamp continuity must therefore be checked before creating lag features for the forecasting task.
7. The `Vol` variable is the main numerical target used for predicting future traffic volume.

## 10. Implications for Phase 3

The findings from Phase 2 should be considered when preparing the forecasting dataset.

In particular:

- Lag features should be created separately for each SegmentID + Direction series.
- The chronological order of observations must be preserved.
- Timestamp gaps should be considered when creating 15-, 30-, 60-, and 120-minute lag features.
- The target should represent traffic volume **15 minutes into the future**.
- Train, validation, and test data should be split chronologically rather than randomly.

Phase 2 does not make any claims about which forecasting model performs best. Model performance will be evaluated later using held-out test data.
