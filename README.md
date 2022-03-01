# Production Level Machine Learning

Don't just train the models on your computer, build a system for it

## Make this specific and move the general to the tutorial

## How to setup infrastructure for Production Machine Learning

Please follow here to set up the environment on an instance or a kubernetes cluster (including mlflow, kubeflow)

Select your MLOps tools (ClearML, Kubeflow, Mlflow)

https://github.com/epadam/production-level-data-analysis/new/master/k8s

Use commercial platform or build your own one with open source
(Neptune, H2O auto) ,  (Kubeflow, H2O, analyticsZoo)

## What is the target and data type?

   a. Structured Data 
     
     - Regression

     - Classification
    
   b. Unstructured Data
      
     - Text

     - Image, Videos

   c. Multimodal Data
 
## Data Collecting Setup

1. Web
2. Internal Data

## Data processing pipeline infrastructure for your data (Data Engineering, ETL)

Please see the instruction [here](https://github.com/epadam/production-level-machine-learning/tree/master/Data_Engineering):

## How to develop your model

Here we use bike sharing dataset as example, we split the dataset to half and trigger the retraining when upload the other half to gcs. 

### Prepare your dataset

Load data from database, feature store or file storage. Do EDA, data augmentation, data visualization

### Select your model

Decision Tree or Deep Learning (check how Uber use Deep learning for EDA)

or you can use AutoML(AutoGloun, AutoKeras)

https://conferences.oreilly.com/tensorflow/tf-ca-2019/public/schedule/detail/80640.html

### Train and Track your models

1. Set up the parameters and configurations for storage and database for tracking and artifact, metadata storage

Track the model with the infrastructure setup (dvc, mlflow, tensorboard, dvc to track your data and model)

2. Do you need distributed Training?

3. Do you need active learning?

* If you don't have much labeled data, you can do active learning (you annotate few data, model ask you for uncertained labeled)

4. Do you need federated Learning?

### Evaluate, Debugging and compare your model
    
    b. Debugging and explain your model
    microsoft responsible AI toolkit, LIT, Manifold, Tensorboard
    
    Optimize your model and model compression

### Export your model

Export your model for different platforms, 

model as code:

model as data:

Tensorflow Lite, OpenVino, Caffe2, ONNX, SavedModel, TorchScript, TensorRT

## Deploy, Monitor, Logging your Model
    Challenges:
    1. Scaling, launch, rolling updates
    2. Optimization
    3. Health Check, recovery
    4. Lantency
    
    a. On the cloud:
    
    * Embedded:
    
    * Microservice:
    
    Seldon Core(outlier detection, explainer, drift detector, adversirial, Auditability), where do you store the explain results?
    
    Seldon suports A/B test, Canary Deployment, Shadow deployment
    
    Monitor your model
    
    Metrics like performance, explainer is going to Prometheus and can be visualized with Grafana
    
    Logging is sending to ELK for further analysis
    
    b. At the edge:
    
    Android, Pi, Self Driving Car
    
    Please check the guide [here](tutorial/mlops_edge_cloud.md)

## (Optional) Build a machine learning retraining pipeline (mlrun, tfx, kubeflow pipeline)
    
    https://sbakiu.medium.com/productionalizing-ml-with-kubernetes-kubeflow-and-seldon-core-39aed36ade83
    
    The meta data of the tfx pipeline is recorded with ML Metadata. After running the pipeline use the notebook to investigate the metadata
    
    Using PV and PVC as local storage between components (visualize your meta data)

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











