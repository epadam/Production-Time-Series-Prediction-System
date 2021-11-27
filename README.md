# Production-Level-Data-Analysis

## Environment setup for MLOps

Please follow here to set up the environment on an instance or a kubernetes cluster (including mlflow, kubeflow)

https://github.com/epadam/production-level-data-analysis/new/master/k8s

## Model Developing and Deploying Process

Here we use adults income dataset as example

1. Data Collection (You will denmamize customers personal information from database) Dockerize your code

2. ETL, Data Labeling (transform the format you need and store in feature store)

3. EDA, Model Development/Tacking/Evaluation (dvc, mlflow, microsoft responsible AI toolkit)

4. (Optional) Once done model development, build a machine learning pipeline for retraining (mlrun, tfx, kubeflow pipeline, )
    
    https://sbakiu.medium.com/productionalizing-ml-with-kubernetes-kubeflow-and-seldon-core-39aed36ade83


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
    You can also try streamlit to check the avaible seldon api 



## Reference

1. https://blog.doit-intl.com/how-to-deploy-tensorflow-extended-pipeline-to-kubeflow-1fecf4602a39

2. https://towardsdatascience.com/production-machine-learning-monitoring-outliers-drift-explainers-statistical-performance-d9b1d02ac158













