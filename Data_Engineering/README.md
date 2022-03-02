## Data Engineering

0. Install Infrastructure on Kubernetes (Kafka, Zookeeper, LabelStudio, Create a GCP project, data storage)

1. Data Collection (from IoT, web or other sources, streaming data or bulk)
    
    a. API fetching example
    
    Build the Docker Image and Push to the registry
    
    b. Kafka Streaming example
    
    Build the Docker Image and Push to the registry

2. ETL (ex: denmamize customers personal information from database, transform the format you need and store in feature store)

    Requirements:
    
    1. Staging and Validation
    
    2. Atomic
    
    You can use Apache Beam, Spark, Flink
    
    Build the Docker Image

3. (optional) Data Labeling 
   
   * Use pre-trained model to pre annotate the data
   
4. Orchestrate the pipeline (Airflow)

5. Develop CI/CD automation for your Data Processing pipeline (data collection, ETL, Airflow)

6. Deploy on Kubernetes

