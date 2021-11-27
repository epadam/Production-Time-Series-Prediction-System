### Serving with Seldon Core

1. Install Seldon Core

2. Write python wraper or use predefined model server and build the docker image, this can be part of Kubeflow pipeline

3. Build the docker and push it to the registry

4. Write the yaml file of the model (A/B testing, Canary deployment) and logging, outlier, drift detection, explainer for kubernetes,
    Kubeflow has deployment ops for model deployment

5. Model can be deployed manually or by CT pipeline or CD script.

6. Install Seldon Core Analytics and ELK to monitor the model performance



## Embedded

1. Push the developed model to registry

2. Trigger the building process of the app
