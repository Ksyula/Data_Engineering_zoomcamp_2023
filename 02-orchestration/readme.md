## Workflow Orchestration

### Data Lake (GCS)

* What is a Data Lake
* ELT vs. ETL
* Alternatives to components (S3/HDFS, Redshift, Snowflake etc.)

### 1. Introduction to Workflow orchestration

* What is orchestration?
* Workflow orchestrators vs. other types of orchestrators
* Core features of a workflow orchestration tool
* Different types of workflow orchestration tools that currently exist 

### 2. Introduction to Prefect concepts

* What is Prefect?
* Installing Prefect
* Prefect flow
* Creating an ETL
* Prefect task
* Blocks and collections
* Orion UI

### 3. ETL with GCP & Prefect

* Flow 1: Putting data to Google Cloud Storage 

### 4. From Google Cloud Storage to Big Query

* Flow 2: From GCS to BigQuery

### 5. Parametrizing Flow & Deployments 

* Parametrizing the script from your flow
* Parameter validation with Pydantic
* Creating a deployment locally
* Setting up Prefect Agent
* Running the flow
* Notifications

### 6. Schedules & Docker Storage with Infrastructure

* Scheduling a deployment
* Flow code storage
* Running tasks in Docker

### 7. Prefect Cloud and Additional Resources 

* Using Prefect Cloud instead of local Prefect
* Workspaces
* Running flows on GCP
* 
* [Prefect docs](https://docs.prefect.io/)
* [Pefect Discourse](https://discourse.prefect.io/)
* [Prefect Cloud](https://app.prefect.cloud/)
* [Prefect Slack](https://prefect-community.slack.com)