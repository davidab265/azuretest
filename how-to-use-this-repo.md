# Deploying GetApp on Kubernetes
To deploy GetApp on Kubernetes, follow these steps:

### 1. Download the sorce code from this release. then unzip the archive, and `cd` into the directory. 

### 2. Download Images from Development Harbor Repository

Download the images from the development Harbor repository. Run the script `getapp-images-to-tar.sh`. This script utilizes the file `getapp-images-list.txt` to download all images of GetApp, saving them to separate tar files. Then, it zips all of them into one file with the name `getapp-<current_date>.zip`.

```
./getapp-images-to-tar.sh
```

### 3. Upload Images to Local Image Repository

Configure the URL, username, and password in the top section of the `load-images.sh` script. Then, execute the script to upload the images to your local image repository.
```
./load-images.sh
```
### 4. Deploy the Helm Chart

Deploy the Helm chart using the following command:
```
helm upgrade -n <NAMESPACE> -i <HELM_PROJECT_NAME> -f ./integration-chart/Values.yaml ./integration-chart

```
Replace "NAMESPACE" with the desired Kubernetes namespace and "HELM_PROJECT_NAME" with the name you want to assign to your Helm project.

### Here are some important points to note about this chart:

**Deployment Target:** , and uses the 'strimzi` operator for deploying kafka, and the 'crunchy data' operator to deploy postgres. so here are some importent things you shuold note:
1. **Route:** This chart is designed specifically for deployment on OpenShift, and uses a "Route" for exposing services, rather than an "Ingress". If you intend to deploy it on a platform other than OpenShift, you'll need to set up an Ingress to expose the route.

### Variables:
these are the variables you need to configure in this deployment:
**Keycloak / sso**
  `AUTH_SERVER_URL`
  `REALM`
  `CLIENT_ID`
  `SECRET_KEY`
  `COOKIE_KEY`

**Kafka**
  `KAFKA_BROKER_URL` 
  `KAFKAJS_NO_PARTITIONER_WARNING` "1"


**Postgres**
  `POSTGRES_HOST`
  `POSTGRES_PORT`
  `POSTGRES_USER`
  `POSTGRES_PASSWORD`
  `POSTGRES_DB`
