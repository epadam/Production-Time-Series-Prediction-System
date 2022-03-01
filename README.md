# Production Level Machine Learning

Don't just train the models on your computer, build a system for it

## Make this specific and move the general to the tutorial

## How to setup infrastructure for Production Machine Learning

Please follow here to set up the environment on an instance or a kubernetes cluster (including mlflow, kubeflow)

https://github.com/epadam/production-level-data-analysis/new/master/k8s

## What it the target and data type?

   a. Structured Data 
     
     - Regression

     - Classification
    
   b. Unstructured Data
      
     - Text

     - Image, Videos

   c. Multimodal Data
 
## How to collect your data

1. Web
2. Internal Data


## Process your data (Data Engineering)

Please see the instruction [here](https://github.com/epadam/production-level-machine-learning/tree/master/Data_Engineering):

## How to develop your model

Here we use bike sharing dataset as example, we split the dataset to half and trigger the retraining when upload the other half to gcs. 

### Prepare your dataset

2. Load data from database, feature store or file storage. Do EDA, data augmentation 

* If you don't have much labeled data, you can do active learning(you annotate few data)

### Select your model

Decsion Tree or Deep Learning

### Train your model

1. Set up the parameters and configurations for storage and database for tracking and artifact, metadata storage

Tracking (dvc, mlflow, tensorboard, dvc to track your data and model

Select your MLOps tools (ClearML, Kubeflow, Mlflow)

### Evaluate and Debugging your model
    
    b. Debugging your model
    microsoft responsible AI toolkit
   
### (Optional) Once done model development, build a machine learning pipeline for retraining (mlrun, tfx, kubeflow pipeline)
    
    https://sbakiu.medium.com/productionalizing-ml-with-kubernetes-kubeflow-and-seldon-core-39aed36ade83
    
    The meta data of the tfx pipeline is recorded with ML Metadata. After running the pipeline use the notebook to investigate the metadata
    
    Using PV and PVC as local storage between components

## Deploy, Monitor, Logging your Model


    a. On the cloud:
    
    Seldon Core(outlier detection, explainer, drift detector, adversirial, Auditability), where do you store the explain results?
    
    Seldon suports A/B test, Canary Deployment, Shadow deployment
    
    Monitor your model
    
    Metrics like performance, explainer is going to Prometheus and can be visualized with Grafana
    
    Logging is sending to ELK for further analysis
    
    b. At the edge:
    
    Please check the guide [here](tutorial/mlops_edge_cloud.md)

## Do CI/CD/CT automation for the model (github actions, Jenkins)

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

Retrain the model when: (Kubeflow Pipeline, here we use the other half data), every retraining data should be versioned
 * code or model updated in the repo (trigger rebuild and retrain the pipeline using github action, run CI/CD for the pipeline, then CD for the model)
 * data uploaded to the repo (trigger run the retraining pipeline using github action, no new pipeline deployed)
 * data upload to the storage (trigger run the deployed retraining pipeline using components in kubeflow or cloud build)
 * concept drift detected (trigger running the deployed pipeline with the new data in storage or repo using monitoring and cloudbuild or kubeflow component)


## Reference

### mlflow with dvc

https://www.iteblog.com/ppt/dataai-summit-euepadarope-2020/data-versioning-and-reproducible-ml-with-dvc-and-mlflow-iteblog.com.pdf

### CI/CD

1. https://github.com/ksalama/kubeflow-examples/tree/master/kfp-cloudbuild

### TFX

1. https://blog.doit-intl.com/how-to-deploy-tensorflow-extended-pipeline-to-kubeflow-1fecf4602a39

2. https://towardsdatascience.com/production-machine-learning-monitoring-outliers-drift-explainers-statistical-performance-d9b1d02ac158

### Open Source/Commercial Platform

* H2O
* OnePanel
* AnalyticsZoo











