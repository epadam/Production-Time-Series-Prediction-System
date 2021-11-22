# Environment Setup for Production Level Machine Learning

## Docker Compose

### Data Engineering 

1. Kafka with Zookeeper

### Machine Learning

You can use MLflow to track, store and serve your model on your instance, this includes

1. Mlflow Server

2. MinIO Server

3. Artifact Store using minIO on s3, gcs (as model registry)

4. Backstore using local file or database (for meta data)

For model serving, you can also use Tensroflow Serving or TorchServe

Monitoring using ELK, Prometheus

## Kubernetes

### Data Engineering 

1. Kafka with Zookeeper

### Machine Learning

1. Kubeflow (Includes Seldon, minIO, Istio, Spark)
2. MLflow
3. ELK
4. Prometheus with Grafana
