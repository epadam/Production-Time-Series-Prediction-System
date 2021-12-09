# Environment Setup for Production Level Machine Learning

## Docker Compose

### Data Engineering 

1. Kafka with Zookeeper

### Machine Learning

For Development:

    1. Using MLflow to track, store and serve your model on your instance, this includes a Mlflow Server, MinIO Server, Artifact Store using minIO on s3, gcs (as model registry), Backstore using local file or database (for meta data)

    Test your mlflow deployment
    
    2. Deploy Feature Store
    
    3. (Optional): Jenkins for CI/CD, or github actions/gitlab CI/CD

For Production:

    1. Monitoring logging using ELK

    2. Monitoring Metrics with Prometheus



## Kubernetes

### Data Engineering 

1. Kafka with Zookeeper

2. LabelStudio

### Machine Learning

1. Kubeflow (it includes Seldon, minIO, Istio, Spark, Jupyter Notebook)
    Please check here to see how to deploy Kubeflow
2. MLflow 
3. Feature Store
3. ELK
4. Prometheus with Grafana

#### Steps:

1. Install Kubeflow follow instruction [here](https://www.kubeflow.org/docs/started/installing-kubeflow/)

2. Install MLflow with Helm (Mlflow Server, Backend Store(Database), Artifact Store(GCS)))

    https://aahansingh.com/mlflow-on-kubernetes

    https://github.com/wajeehulhassanvii/mlflow_on_kubeflow

    https://github.com/cetic/helm-mlflow

    https://towardsdatascience.com/mlflow-part-2-deploying-a-tracking-server-to-minikube-a2d6671e6455


3. Deploy Prometheus and Grafana onto the cluster using the community Helm chart

    https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

    If using Seldon for deployment, then you can use seldon-core-analytics which also use Prometheus and Grafana 

    https://github.com/SeldonIO/seldon-core/tree/master/helm-charts/seldon-core-analytics

4. Install ELK with Helm (as infrastructure or go with the model deployment?)

## Reference

1. https://github.com/sachua/mlflow-docker-compose

2. https://github.com/jeremyjordan/ml-monitoring

3. https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

On a single node
https://towardsdatascience.com/a-simple-mlops-pipeline-on-your-local-machine-db9326addf31

