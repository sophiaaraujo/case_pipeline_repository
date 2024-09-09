# Brewery Data Pipeline

This project implements a data pipeline to consume data from the Open Brewery DB API, transform it, and load it into a data lake using the Medallion architecture.
## Objective

The objective is to create a data pipeline that consumes data from an API, transforms it, and persists it in a data lake with three layers: bronze, silver, and gold.
## Project Structure

- `dags/`: Contains the brewery_dag.py file for the data pipeline in Airflow.
- `scripts/`: Contains Python scripts for data extraction, transformation, and loading.
- `docker-compose.yaml`: File to configure and start Docker containers.
- `Dockerfile`: Defines the custom Docker image for Airflow.

## Design and Decisions

### Medallion Architecture (within the data_lake directory)

1. **Bronze Layer**: Stores raw data extracted from the API in JSON format.
2. **Silver Layer**: Transforms the data into a columnar format (Parquet) and partitions by location.
3. **Gold Layer**: Creates an aggregated view with the number of breweries by type and location, stored in CSV format.

### Tools and Technologies

- **Apache Airflow**: Orchestration of the data pipeline.
- **PostgreSQL**: Storage for Airflow's metadata.
- **Docker**: Containerization of the Airflow and PostgreSQL environment.
- **Python**: Language used for ETL scripts.
- **Pandas e PyArrow**: Libraries for data transformation.

### Design Choices and Trade-offs

- **Airflow**: Airflow is used for its robustness in workflow orchestration and flexibility in handling different data sources. It also supports scheduled tasks, including automatic retries and parallelism. The use of the LocalExecutor in Airflow allows tasks to run efficiently in a local environment, while PostgreSQL stores Airflow’s state.
- **Parquet Format**: Used in the Silver layer due to its efficiency for storage and queries.
- **Containerization with Docker**: Simplifies environment setup and isolation, ensuring consistency between development and production environments.

## Monitoring and Alerts

To ensure continuous operation and data quality in the pipeline, the following monitoring and alert mechanisms are implemented:

1. **Airflow Monitoring**:
   - **Logs**: Airflow provides detailed logs for each task in the DAG. These logs help diagnose issues and failures.
   - **Web Interface**: Airflow offers a web interface for real-time monitoring of DAGs and their executions.
   - For more advanced monitoring, you can integrate Airflow with Prometheus and use Grafana to create real-time monitoring dashboards. This can be useful for continuously visualizing the performance and behavior of the pipeline.
   - It is also possible to configure different profiles in the docker-compose.yml for development and production. This allows you to adjust parameters (such as logging levels or Airflow retry settings) based on the environment.

2. **Failure Alerts**:
   - **Emails**: Configure Airflow to send email notifications in case of task failures. This can be set up by adjusting email settings in the `airflow.cfg`.
   - **Slack Alerts**: For a more advanced solution, Slack alerts can be set up using Airflow hooks and custom sensors.

3. **Data Quality**:
   - **Data Validation**: The pipeline can include automatic quality checks, such as verifying that the data contains all expected columns or that no critical fields have null values.

4. **Logs and Metrics**:
   - **Execution Logs**: Ensure logs are correctly captured and stored for later analysis.
   - **Performance Metrics**: Monitor Airflow and PostgreSQL performance metrics to identify bottlenecks.

5. **Pipeline CI/CD**:
   - **Deployment Automation**: If the project grows or is maintained by a team, adding CI/CD (Continuous Integration/Continuous Deployment) pipelines can streamline testing and automatic deployments. Tools like GitHub Actions can be used to ensure that when pushing to the repository, tests are run, and if they pass, deployment to a production or staging environment is done automatically.

## Instructions to Run

Ensure you have the following tools installed:

Docker (version 20.10 or higher)
Docker Compose (version 1.29 or higher)
To verify, run:
```bash
docker --version
docker-compose --version 
```

1. **Clone the Repository**

   Clone the repository and navigate to the project directory:

   ```bash
   git clone https://github.com/sophiaaraujo/case_pipeline_repository.git
   cd case_pipeline
   ```

2. **Start Services with Docker**

   The project uses Docker Compose to orchestrate the services. To initialize Airflow, PostgreSQL, and other components, run the following command:
   ```bash
   docker-compose up -d
   ```
   This command will download the necessary images and start the containers in the background.

3. ***Access the Airflow Interface***

   Once the containers are running, you can access the Airflow web interface in your browser:
   http://localhost:8080   (Username: airflow; Password: airflow)

4. ***Activate and Run the DAG***

   In the Airflow interface:

   Go to the "DAGs" tab to view the list of available DAGs.
   Locate the brewery_dag and activate it by clicking the toggle switch next to its name.
   To manually trigger the DAG, click the "play" (run) icon.

5. ***Check Data in the Data Lakee***

   The data will be saved in the data_lake directory mounted in the Airflow container:

   Bronze Layer: Raw data in JSON format.
   Silver Layer: Transformed data in Parquet format, partitioned by location.
   Gold Layer: Aggregated view of breweries by type and location, stored in CSV format.

   These files can be found in the data_lake folder within the container or in the mapped local directory.

6. ***Stop the Containers***

   When finished using the pipeline, stop all containers with the following command:
   ```bash
   docker-compose down
   ```
   
[Leia em Português](README_pt.md)