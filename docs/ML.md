# Machine learning

Attendance risk currently exposes a deterministic, explainable local inference baseline. Responses include risk level, probability, contributing factors, and model version. The attendance ETL validates required columns and duplicate records before aggregation.

A production training phase should version a real dataset, compare a simple baseline with XGBoost, record parameters/metrics/artifacts in MLflow, and register only a model that beats the baseline. No accuracy claim is made by the current repository.
