# Production-Level-Data-Analysis

## Environment setup for MLOps

Please follow here to set up the environment on an instance or a kubernetes cluster (including mlflow, kubeflow)

https://github.com/epadam/production-level-data-analysis/new/master/k8s

## Machine Learning Project in Production

### Data Engineering

1. Data Collection (from IoT, web or other sources, streaming data or bulk)
    
    Kafka or API fetch

2. ETL, Data Labeling (denmamize customers personal information from database, transform the format you need and store in feature store)
    
    Apache Beam, Spark, Flink
    1. Staging and Validation
    2. Atomic
    
3. Orchestrate the pipeline (Airflow)

4. Develop CI/CD for your Data Processing pipeline

5. Deploy the pipeline into production env with monitoring

### Model Developing and Deploying Process

Here we use bike sharing dataset as example

3. EDA, Model Development/Tacking/Evaluation (dvc, mlflow, microsoft responsible AI toolkit)
    Use mlflow, tensorboard, dvc to track your data and model

4. (Optional) Once done model development, build a machine learning pipeline for retraining (mlrun, tfx, kubeflow pipeline)
    
    https://sbakiu.medium.com/productionalizing-ml-with-kubernetes-kubeflow-and-seldon-core-39aed36ade83
    
    The meta data of the tfx pipeline is recorded with ML Metadata and store in SQL
    
5. Developing CI/CD/CT for the model (github actions, Jenkins)

    CI with github actions:

    https://billtcheng2013.medium.com/hello-world-to-github-actions-for-mlops-with-google-cloud-f5917b80d8a9

    a. set up env. secret in github secrets

    https://github.com/NikeNano/kubeflow-github-action

    https://github.com/kubeflow/examples/tree/master/pipelines/github_action

    https://github.com/marketplace/actions/kubeflow-compile-deploy-and-run
    
    CD:
    1. A Docker container image containing our pipeline and dependencies. The image is pushed to the Google Container Registry.
    2. And the CLI to create the pipeline.

6. Deploy, monitor and logging the model
    
    Seldon Core(outlier detection, explainer, drift detector, adversirial, Auditability), where do you store the explain results?
    
    Seldon suports A/B test, Canary Deployment, Shadow deployment
    
    Metrics like performance, explainer is going to Prometheus and can be visualized with Grafana
    
    Logging is sending to ELK for further analysis
   

## Retraining Process

Following two condition will trigger the retraining process:

a. Retrain the model when new data is available or concept drift happened (Kubeflow Pipeline, here we use the other half data)

b. When updating the code of retraining pipeline or detecting concept drift, trigger github actions to test the retraining pipeline, followed by CD to the test environment and finally deploy it in production 


## Visualization
    You can also try streamlit to check what seldon core offers



## Reference

### mlflow with dvc

https://www.iteblog.com/ppt/dataai-summit-euepadarope-2020/data-versioning-and-reproducible-ml-with-dvc-and-mlflow-iteblog.com.pdf

### CI/CD

1. https://github.com/ksalama/kubeflow-examples/tree/master/kfp-cloudbuild

### TFX

1. https://blog.doit-intl.com/how-to-deploy-tensorflow-extended-pipeline-to-kubeflow-1fecf4602a39

2. https://towardsdatascience.com/production-machine-learning-monitoring-outliers-drift-explainers-statistical-performance-d9b1d02ac158













