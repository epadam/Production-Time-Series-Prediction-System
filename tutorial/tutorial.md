
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

5. upload to kubeflow to test the pipeline

6. Write the deployment yaml for seldon model serving including monitoring, (data for retraining collection), and model retraining trigger logic for concept drift, data drift, adversirial attack. 

7. Write CI/CD script with github actions, cloudbuild.yaml to automate image, pipeline building and deployment

    For retraining pipeline: (model is trained in the deployed pipeline)
    
    model code change -> CI trigger --> CI script --> CD trigger --> CD script --> deployed pipeline --> model deployed (or push to registry --> CD for model deployment)
    
    No retraining pipeline: (model is train in the CI script)
    
    model/data change -> CI trigger --> CI script for retrain the model --> CD trigger --> CD script --> model deployede
