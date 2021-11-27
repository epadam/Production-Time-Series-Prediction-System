
### Data Engineering

1. Data collecting
2. ETL, data labeling



### Model development

0. Create a new notebook, install required tools for data versioning, model tracking, model versioning, model inspection, pipeline orchestration

1. Load the data from data storage, do EDA, model training, evaluation

2. Build tfx pipeline components and compile the pipeline

3. upload to kubeflow to run

4. Write the deployment yaml including monitoring (seldon core analytics should already there, but drift, outlier, adversirial detection)

5. Write CI/CD script with github actions, cloudbuild.yaml

    For retraining pipeline:
    CI trigger --> CI script 

    CD trigger --> CD script

    If model deployment is not in the pipeline:
    CD trigger --> CD script
    
    No retraining pipeline:
    CI trigger --> CI script --> (CD script)
    
    CD trigger --> CD script
