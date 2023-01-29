# Lecture 1
* [terraform_overview](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/1_terraform_gcp/1_terraform_overview.md)
* [terraform_installation](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/1_terraform_gcp/README.md)


export GOOGLE_APPLICATION_CREDENTIALS="~/gcp-service-account-authkeys.json"

# Download Google [SDK](https://cloud.google.com/sdk/docs/quickstart) and install it
gcloud init

gcloud auth application-default login

# Download and install [Terraform](https://developer.hashicorp.com/terraform/downloads)
How to define configuration of resources in the Terraform file:

#### Files

* `main.tf`
* `variables.tf`
* Optional: `resources.tf`, `output.tf`
* `.tfstate`

#### Declarations
* `terraform`: configure basic Terraform settings to provision your infrastructure
   * `required_version`: minimum Terraform version to apply to your configuration
   * `backend`: stores Terraform's "state" snapshots, to map real-world resources to your configuration.
      * `local`: stores state file locally as `terraform.tfstate`
   * `required_providers`: specifies the providers required by the current module
* `provider`:
   * adds a set of resource types and/or data sources that Terraform can manage
   * The Terraform Registry is the main directory of publicly available providers from most major infrastructure platforms.
* `resource`
  * blocks to define components of your infrastructure
  * Project modules/resources: google_storage_bucket, google_bigquery_dataset, google_bigquery_table
* `variable` & `locals`
  * runtime arguments and constants


#### Execution steps
1. `terraform init`: 
    * Initializes & configures the backend, installs plugins/providers, & checks out an existing configuration from a version control 
2. `terraform plan`:
    * Matches/previews local changes against a remote state, and proposes an Execution Plan.
3. `terraform apply`: 
    * Asks for approval to the proposed plan, and applies changes to cloud
4. `terraform destroy`
    * Removes your stack from the Cloud

# Set upGCP VM

```
gcloud compute instances create de-zoomcamp  \
    --project=snappy-cosine-375820 \
    --zone=europe-west3-c \
    --machine-type=e2-standard-2 \
    --network-interface=network-tier=PREMIUM,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=115713813633-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
    --create-disk=auto-delete=yes,boot=yes,device-name=de-zoomcamp,image=projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20230125,mode=rw,size=20,type=projects/snappy-cosine-375820/zones/europe-west3-c/diskTypes/pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --reservation-affinity=any
```

ssh -i ~/.ssh/gcp ksenia@35.234.***.**

htop

gcloud

## Install Anaconda
`wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh`

`bash Anaconda3-2022.10-Linux-x86_64.sh`

`touch ~/.ssh/config`
`code config`

```
Host de-zoomcamp
     HostName 35.234.***.**
     User ksenia
     IdentityFile ~/.ssh/gcp
```

Ctrl + D `logout`

`ssh -i ~/.ssh/gcp ksenia@35.234.112.11`  # login

`which python`
`source .bashrc`

## Install docker
`sudo apt-get update`
`sudo apt-get install docker.io`

## Ssh the remote server
1. Install Remote-SSH plagin in VS Сode

2. Clone the repo - git clone https://github.com/DataTalksClub/data-engineering-zoomcamp.git 

`cd data-engineering-zoomcamp/`

## Grand permissions to docker in ssh config

1. Run Docker commands without sudo - https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md

`sudo groupadd docker`
`sudo gpasswd -a $USER docker`
`sudo service docker restart`

Log out and log back in so that your group membership is re-evaluated

`docker run hello-world`
`docker run -it ubuntu bash`

2. Install docker compose

`mkdir bin`
`cd bin/`
`wget https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -O docker-compose`
`chmod +x docker-compose`
`./docker-compose version`

Make docker visible from any directory

`cd`
`nano .bashrc`

prepend /bin directory to the PATH

```
export PATH="${HOME}/bin:${PATH}"
```

Nano: SAVE: ctrl + O + Enter
Nano: EXIT: ctrl + X

`source .bashrc`     # refresh the current shell environment
`which docker-compose`
`docker-compose version`

`cd data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/`

`docker-compose up -d` # run in detached mode
`docker ps`

## Install pgcli

`pip install pgcli`
`pgcli -h localhost -U root -d ny_taxi`

`\dt`

Alternativelly install it with **conda**:

`pip uninstall pgcli`
`conda install -c conda-forge pgcli`
`pip install -U mycli`

# Forward Postgree container port to the local machine

Forward `5432` and `8080` and `8888` in VS Сode

http://localhost:8080/ # access PGAdmin from GCP

# Execute Jupyter from cloud and map to local

`cd data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql`
`jupyter notebook`

forward port 8888 and open `http://localhost:8888/?token=.....`

## Download data to the instance
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz

run notebook and upload data to DB

# Install terraform
take the last release from https://developer.hashicorp.com/terraform/downloads

`wget https://releases.hashicorp.com/terraform/1.3.7/terraform_1.3.7_linux_amd64.zip`
`sudo apt install unzip`
`unzip terraform_1.3.7_linux_amd64.zip`
`rm terraform_1.3.7_linux_amd64.zip`

terraform is already executable and .bin in the PATH

`terraform -version`
`cd /data-engineering-zoomcamp/week_1_basics_n_setup/1_terraform_gcp/terraform`

## Put credentials for service accaunt to remote machine

from local via SSH File Transfer Protocol (SFTP):
`sftp de-zoomcamp`
```
sftp> mkdir .gc
sftp> cd .gc
sftp> put gcp-service-account-authkeys.json
```

# Configure Google Cloud CLI

`export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/gcp-service-account-authkeys.json`

`gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS`

`cd /data-engineering-zoomcamp/week_1_basics_n_setup/1_terraform_gcp/terraform`

`terraform init` / `plan` / `apply`

# Shutdown instance

`sudo shutdown now`

Whenever the instance will be resumed - change an External IP in ssh conding