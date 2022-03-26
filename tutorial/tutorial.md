### Think what you need

Think about what you need when you pick up an MLOps platform/toolkit?
* You need to real time or offline analysis
* Which environment will you deploy the model? k8s, local machine, virtual machine?
* You develop on local laptop or remote cluster?
* Integrated data processing tools? Do you need Spark, Dask? Airflow, Perfect
* Do you need autoML training?
* Do you need distributed training?
* Do you need retraining pipeline?
* Integrated deploying serving tools

### Data Engineering

1. Data collecting
2. ETL, data labeling

### Model development

0. Create a git repo

1. Create a new notebook from kubeflow UI, install required tools for data versioning, model tracking, model versioning, model inspection, pipeline orchestration

    pip install -r requirements.txt (mlflow, dvc, kfp, tfx)
    git init to sync to the repo
    Define parameters (data root, storage, mlflow init, dvc init)

2. Load the data from data storage, do EDA, 
    
    add your data to dvc
    tools you can use for evaluation and inspection
    a. microsoft reliable AI 
    
3. Model training, debugging and evaluation
   Just metrics like accuracy is not enough,  
   tools you can use for model debugging
   a. Tensorflow model analysis
   
   b. Responsible model ai-toolbox
   
   c. Manifold
   
4. Build tfx pipeline components and compile the pipeline and write retraining trigger code/funcion(the component can include retraining trigger function)

Retrain the model when: (Kubeflow Pipeline, here we use the other half data), every retraining data should be versioned
 * code or model updated in the repo (trigger rebuild and retrain the pipeline using github action, run CI/CD for the pipeline, then CD for the model)
 * data uploaded to the repo (trigger run the retraining pipeline using github action, no new pipeline deployed)
 * data upload to the storage (trigger run the deployed retraining pipeline using components in kubeflow or cloud build)
 * concept drift detected (trigger running the deployed pipeline with the new data in storage or repo using monitoring and cloudbuild or kubeflow component)

5. Upload to kubeflow to test the pipeline

6. Write the deployment yaml for seldon core model serving including monitoring, (data for retraining collection), and model retraining trigger logic for concept drift, data drift, adversirial attack. 

7. Write CI/CD script with github actions, cloudbuild.yaml to automate image, pipeline building and deployment (include retraining trigger condition)

    For retraining pipeline: (model is trained in the deployed pipeline)
    
    model code change -> CI trigger --> CI script --> CD trigger --> CD script --> deployed pipeline --> model deployed (or push to registry --> CD for model deployment)
    
    No retraining pipeline: (model is train in the CI script)
    
    model/data change -> CI trigger --> CI script for retrain the model --> CD trigger --> CD script --> model deployede


### Reference

#### MLOps Level 0

Manual, no pipeline, no CI/CD automation

Example: Assemly Line, robots only recognize fixed number of objects. It won't change 

#### MLOps Level 1

 manually deployed pipeline,. CD for model deployment

Example: 

#### MLOps Level 2

CI/CD automation for pipeline, CD for model

Example: Stock Price prediction

#### Model Deployment Options for Edge

1. Github Large File Store
2. Model is stored in Registry. Script fetching the models from Registry when building 
3. Model is stored in Regsitry. App is built and running then download the model. Can fetch or by push method(OTA) 
   (need to restart the app/without restarting the app)
