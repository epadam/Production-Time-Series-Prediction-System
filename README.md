# Production-Level-Data-Analysis

Model Developing Process

1. Data Collection

2. ETL 

3. EDA 

4. Model Development/Evaluation (dvc, mlflow, microsoft responsible AI toolkit)

5. Develop CI/CD/CT for the model (mlrun, tfx, kubeflow pipeline, github actions)

6. Deploy the model and monitor it (Seldon Core(outlier detection, explainer), Prometheus)

7. Retrain the model (Kubeflow Pipeline)


You use streamlit as the interface to check the api

1. prediction result
2. explain the result
3. data drift alert

you can also check the statistics of the model by deploying prometheus and grafana
