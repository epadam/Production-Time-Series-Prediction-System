
### Data Engineering

1. Data collecting
2. ETL, data labeling



### Model development

0. Create a git repo

1. Create a new notebook from kubeflow UI, install required tools for data versioning, model tracking, model versioning, model inspection, pipeline orchestration

    pip install -r requirements.txt (mlflow, dvc, kfp, tfx)
    git init to sync to the repo
    Define parameters (data root, storage, mlflow init, dvc init)

2. Load the data from data storage, do EDA, model training, evaluation
    
    add your data to dvc
    tools you can use for evaluation and inspection
    a. microsoft reliable AI 


3. Build tfx pipeline components and compile the pipeline

4. upload to kubeflow to run

5. Write the deployment yaml for seldon model serving including monitoring (seldon core analytics should already there, but drift, outlier, adversirial detection)

6. Push all the code to the git repo

7. Write CI/CD script with github actions, cloudbuild.yaml to automate image, pipeline building and deployment

    For retraining pipeline:
    CI trigger --> CI script 

    CD trigger --> CD script

    If model deployment is not in the pipeline:
    CD trigger --> CD script
    
    No retraining pipeline:
    CI trigger --> CI script --> (CD script)
    
    CD trigger --> CD script
