# Production Level Machine Learning

## How to setup infrastructure for Production Machine Learning

Please follow here to set up the environment on an instance or a kubernetes cluster (including mlflow, kubeflow)

https://github.com/epadam/production-level-data-analysis/new/master/k8s


## What is the target and what data do you need?

1. What it the target and data type?

   a. Structured Data 
     
     - Regression

     - Classification
    
   b. Unstructured Data
      
     - Text

     - Image, Videos

   c. Multimodal Data
 
## How to collect your data


## Process your data (Data Engineering)

Please see the instruction [here](https://github.com/epadam/production-level-machine-learning/tree/master/Data_Engineering):

## How to develop your model

Here we use bike sharing dataset as example, we split the dataset to half and trigger the retraining when upload the other half to gcs. 

1. Set up the parameters and load dataset from database, feature store or file storage.

2. EDA, Model Development/Tacking/Evaluation (dvc, mlflow, microsoft responsible AI toolkit)
    Use mlflow, tensorboard, dvc to track your data and model
    
    a. Evaluate your model
    
    b. Debugging your model
   

3. (Optional) Once done model development, build a machine learning pipeline for retraining (mlrun, tfx, kubeflow pipeline)
    
    https://sbakiu.medium.com/productionalizing-ml-with-kubernetes-kubeflow-and-seldon-core-39aed36ade83
    
    The meta data of the tfx pipeline is recorded with ML Metadata. After running the pipeline use the notebook to investigate the metadata
    
    Using PV and PVC as local storage between components

## How to deploy, monitor and logging the model?

    a. On the cloud:
    
    Seldon Core(outlier detection, explainer, drift detector, adversirial, Auditability), where do you store the explain results?
    
    Seldon suports A/B test, Canary Deployment, Shadow deployment
    
    Metrics like performance, explainer is going to Prometheus and can be visualized with Grafana
    
    Logging is sending to ELK for further analysis
    
    b. At the edge:
    
    Please check the guide [here](tutorial/mlops_edge_cloud.md)

## How to do CI/CD/CT automation for the model (github actions, Jenkins)

    CI with github actions:

    https://billtcheng2013.medium.com/hello-world-to-github-actions-for-mlops-with-google-cloud-f5917b80d8a9

    set up env. secret in github secrets

    https://github.com/NikeNano/kubeflow-github-action

    https://github.com/kubeflow/examples/tree/master/pipelines/github_action

    https://github.com/marketplace/actions/kubeflow-compile-deploy-and-run
    
    CD:
    1. A Docker container image containing our pipeline and dependencies. The image is pushed to the Google Container Registry.
    2. And the CLI to create the pipeline.

### Trigger Retraining Process

Following two condition will trigger the retraining process:

a. Retrain the model when new data is available or concept drift happened (Kubeflow Pipeline, here we use the other half data)

b. When updating the code of retraining pipeline or detecting concept drift, trigger github actions to test the retraining pipeline, followed by CD to the test environment and finally deploy it in production 

c. M




## Reference

### mlflow with dvc

https://www.iteblog.com/ppt/dataai-summit-euepadarope-2020/data-versioning-and-reproducible-ml-with-dvc-and-mlflow-iteblog.com.pdf

### CI/CD

1. https://github.com/ksalama/kubeflow-examples/tree/master/kfp-cloudbuild

### TFX

1. https://blog.doit-intl.com/how-to-deploy-tensorflow-extended-pipeline-to-kubeflow-1fecf4602a39

2. https://towardsdatascience.com/production-machine-learning-monitoring-outliers-drift-explainers-statistical-performance-d9b1d02ac158













