### Serving with Seldon Core

1. Install Seldon Core

2. Write python wraper or use predefined model server and build the docker image, this can be part of Kubeflow pipeline

3. Build the docker and push it to the registry

4. Write the yaml file of the model (A/B testing, Canary deployment) and logging, outlier, drift detection, explainer for kubernetes,
    Kubeflow has deployment ops for model deployment
    
    a. A/B testing
    
    b. Alibi Explainers (how to store explainer results)
    
    c. Outlier Detector (expose logging, knative eventing, ELK server) 
    
    d. Drift monitoring (expose )

5. Install Seldon Core Analytics and ELK to monitor the model performance:
    
    Metrics:
    - Requests per second
    - Latency per request
    - CPU/memory/data utilisation
    - Custom application metrics
    
    Explainability monitoring:
    - Human-interpretable insights for model behaviour
    - Introducing use-case-specific explainability capabilities
    - Identifying key metrics such as trust scores or statistical perf. thresholds
    - Enabling for use of some more complex ML techniques
    
    Outlier Detection:
    - Detecting anomalies in data instances
    - Flagging / alerting when outliers take place
    - Identifying potential metadata that could help diagnose outliers
    - Enable drill down of outliers that are identified
    - Enabling for continuous / automated retraining of detectors
    
    Drift Detecting:
    - Identifying drift in data distribution, as well as drifts in the relationship between input and output data from a model
    - Flagging drift that is found together with the relevant datapoints where it was identified
    - Allowing for the ability to drill down into the data that was used to calculate the drift

6. Model can be deployed manually or by CT pipeline or CD script.

    
    
 

## Embedded

1. Push the developed model to registry

2. Trigger the building process of the app

## Reference

1. https://towardsdatascience.com/production-machine-learning-monitoring-outliers-drift-explainers-statistical-performance-d9b1d02ac158
