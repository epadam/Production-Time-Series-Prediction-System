## Data Engineering

0. Install Infrastructure on Kubernetes (Kafka, Zookeeper, LabelStudio, Create a GCP project)

1. Data Collection (from IoT, web or other sources, streaming data or bulk)
    API fetching example
    Kafka Streaming example

2. ETL, Data Labeling (denmamize customers personal information from database, transform the format you need and store in feature store)

    You can use Apache Beam, Spark, Flink
    
    1. Staging and Validation
    
    2. Atomic

3. Orchestrate the pipeline (Airflow)

4. Develop CI/CD for your Data Processing pipeline

5. Deploy on Kubernetes

