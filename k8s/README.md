# Environment Setup for Production Level Machine Learning

## Docker Compose

### Data Engineering 

1. Kafka with Zookeeper

### Machine Learning

1. You can use MLflow to track, store and serve your model on your instance, this includes a Mlflow Server, MinIO Server, Artifact Store using minIO on s3, gcs (as model registry), Backstore using local file or database (for meta data)

Test your mlflow deployment

2. For model serving, you can also use Tensroflow Serving or TorchServe

3. Monitoring using ELK, Prometheus

4. Optional: Jenkins for CI/CD

## Kubernetes

### Data Engineering 

1. Kafka with Zookeeper

### Machine Learning

1. Kubeflow (Includes Seldon, minIO, Istio, Spark)
2. MLflow
3. ELK
4. Prometheus with Grafana

#### Steps:

1. Install Kubeflow follow instruction [here](https://www.kubeflow.org/docs/started/installing-kubeflow/)

2. Install MLflow with Helm (Mlflow Server, Database)

3. Install ELK with Helm

4. Deploy Prometheus and Grafana onto the cluster using the community Helm chart

  https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

If using Seldon for deployment, then you can use seldon-core-analytics which also use Prometheus and Grafana 

  https://github.com/SeldonIO/seldon-core/tree/master/helm-charts/seldon-core-analytics


## Reference

1. https://github.com/sachua/mlflow-docker-compose

2. https://github.com/jeremyjordan/ml-monitoring

3. https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

On a single node
https://towardsdatascience.com/a-simple-mlops-pipeline-on-your-local-machine-db9326addf31

