# FarAlpha Technologies

## Flask & MongoDB on Kubernetes

A containerized Flask REST API integrated with MongoDB and deployed on Kubernetes using Minikube. This project demonstrates persistent storage, internal service discovery, resource management, and horizontal pod autoscaling.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python) ![Flask](https://img.shields.io/badge/Flask-3.1.2-black?logo=flask) ![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green?logo=mongodb) ![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker) ![Kubernetes](https://img.shields.io/badge/Kubernetes-Deployed-326CE5?logo=kubernetes)

[**Docker Hub Image**](https://hub.docker.com/r/mudittak21/faralpha-flask)

---

## 1. Project Overview

This project demonstrates the deployment of a Flask-based REST API application with MongoDB as its database using Kubernetes.

The application supports:

- Displaying a welcome message with the current date and time.

- Inserting JSON records into MongoDB through a POST request.

- Retrieving stored records through a GET request.

- Running multiple Flask application replicas.

- Persistent MongoDB storage using PersistentVolume and PersistentVolumeClaim.

- Automatic scaling of Flask pods using Horizontal Pod Autoscaler (HPA).

- Internal MongoDB communication through Kubernetes DNS.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Application development |
| Flask 3.1.2 | REST API framework |
| PyMongo 4.15.3 | MongoDB connectivity |
| Gunicorn 23.0.0 | Production WSGI server |
| MongoDB 7.0 | Database |
| Docker | Containerization |
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes cluster |
| kubectl | Kubernetes management |
| Docker Hub | Container image registry |

## 3. Project Directory Structure

```

faralpha-k8s/

│

├── app/

│   ├── app.py

│   ├── requirements.txt

│   └── Dockerfile

│

├── k8s/

│   ├── namespace.yaml

│   ├── mongodb-pv.yaml

│   ├── mongodb-pvc.yaml

│   ├── mongodb-headless.yaml

│   ├── mongodb-service.yaml

│   ├── mongodb-statefulset.yaml

│   ├── flask-deployment.yaml

│   ├── flask-service.yaml

│   └── flask-hpa.yaml

│

├── tests/

│

├── screenshots/

│

└── README.md


```

## 4. Application API Endpoints

### GET /

Returns a welcome message with the current date and time.

Example response:

```

Welcome to the Flask app! The current time is: 2026-11-11 ...


```

### GET /health

Checks whether the Flask application can communicate with MongoDB.

Example response:

```
{

  "status": "healthy",

  "database": "connected"

}

```

### POST /data

Inserts a JSON object into the MongoDB collection named `data`.

Example request:

```
{

  "sampleKey": "sampleValue",

  "project": "FarAlpha Kubernetes",

  "database": "MongoDB"

}

```

Successful response:

```
{

  "status": "Data inserted"

}

```

### GET /data

Retrieves all stored records from MongoDB.

The application excludes MongoDB's internal `_id` field from the returned records.

## 5. Docker Configuration

The application uses Python 3.12 slim as its base image.

### Dockerfile

```
FROM python:3.12-slim



WORKDIR /app



ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1



COPY requirements.txt .



RUN pip install --no-cache-dir -r requirements.txt



COPY app.py .



EXPOSE 5000



CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "60", "app:app"]

```

### Build Docker Image

From the project directory:

```
cd D:\\Kubernetes\\projects\\faralpha-k8s\\app



docker build -t faralpha-flask:1.3 .

```

### Docker Hub Image

The application image was successfully published to Docker Hub.

Repository:

`mudittak21/faralpha-flask`

Tag:

`1.3`

Public image reference:

`mudittak21/faralpha-flask:1.3`

Docker Hub repository:

[https://hub.docker.com/r/mudittak21/faralpha-flask](https://hub.docker.com/r/mudittak21/faralpha-flask)

### Push Image to Docker Hub

```
docker login



docker tag faralpha-flask:1.3 mudittak21/faralpha-flask:1.3



docker push mudittak21/faralpha-flask:1.3

```

### Verify Published Image

```
docker manifest inspect mudittak21/faralpha-flask:1.3

```

The remote manifest was successfully retrieved. The published image includes a Linux AMD64 platform manifest.

## 6. Kubernetes Deployment

The project uses a dedicated namespace named `faralpha`.

### Step 1: Start Minikube

```
minikube start --driver=docker

```

Check cluster status:

```
kubectl get nodes

```

### Step 2: Create Namespace

```
kubectl apply -f .\\k8s\\namespace.yaml

```

### Step 3: Configure MongoDB Credentials

MongoDB authentication is configured using a Kubernetes Secret.

Create the Secret using your own credentials:

```
kubectl create secret generic mongodb-secret -n faralpha --from-literal=mongo-root-username=faralpha_admin --from-literal=mongo-root-password='YOUR_MONGODB_PASSWORD'

```

Replace `YOUR_MONGODB_PASSWORD` with the actual MongoDB password configured for your deployment.

Do not commit real credentials to a public Git repository.

### Step 4: Configure Persistent Storage

Apply the PersistentVolume:

```
kubectl apply -f .\\k8s\\mongodb-pv.yaml

```

Apply the PersistentVolumeClaim:

```
kubectl apply -f .\\k8s\\mongodb-pvc.yaml

```

Verify:

```
kubectl get pv

kubectl get pvc -n faralpha

```

### Step 5: Deploy MongoDB

Apply MongoDB services:

```
kubectl apply -f .\\k8s\\mongodb-headless.yaml

kubectl apply -f .\\k8s\\mongodb-service.yaml

```

Deploy MongoDB StatefulSet:

```
kubectl apply -f .\\k8s\\mongodb-statefulset.yaml

```

Check status:

```
kubectl get statefulset -n faralpha

kubectl get pods -n faralpha

```

### Step 6: Load Flask Image into Minikube

The local development deployment uses the locally built Docker image.

```
minikube image load faralpha-flask:1.3

```

Verify:

```
minikube image ls

```

### Step 7: Deploy Flask Application

```
kubectl apply -f .\\k8s\\flask-deployment.yaml

```

Expose Flask through its Kubernetes Service:

```
kubectl apply -f .\\k8s\\flask-service.yaml

```

Check:

```
kubectl get deployments -n faralpha

kubectl get services -n faralpha

kubectl get pods -n faralpha

```

### Step 8: Configure Horizontal Pod Autoscaler

```
kubectl apply -f .\\k8s\\flask-hpa.yaml

```

Check HPA:

```
kubectl get hpa -n faralpha

```

## 7. Accessing the Flask Application

The Flask Service uses NodePort 30080.

For local testing, port forwarding is used:

```
kubectl port-forward service/flask-service 5000:5000 -n faralpha

```

Keep this terminal window running.

Open another PowerShell window and access:

`http://localhost:5000/`

### Test the Root Endpoint

```
Invoke-WebRequest http://localhost:5000/ -UseBasicParsing

```

### Test Health Endpoint

```
Invoke-RestMethod http://localhost:5000/health

```

### Test POST Endpoint

```
$body = @{

    sampleKey = "sampleValue"

    project = "FarAlpha Kubernetes"

    database = "MongoDB"

} | ConvertTo-Json



Invoke-RestMethod -Uri http://localhost:5000/data -Method POST -ContentType "application/json" -Body $body

```

### Test GET Endpoint

```
Invoke-RestMethod http://localhost:5000/data

```

## 8. Kubernetes DNS Configuration

Kubernetes provides an internal DNS mechanism that allows applications to communicate with Services using their DNS names rather than hard-coded IP addresses.

The MongoDB Service is located in the `faralpha` namespace.

Its fully qualified DNS name is:

`mongodb.faralpha.svc.cluster.local`

Breakdown:

- `mongodb`: Service name.

- `faralpha`: Kubernetes namespace.

- `svc`: Identifies a Kubernetes Service.

- `cluster.local`: Default Kubernetes cluster DNS domain.

The Flask application uses this hostname through the `MONGO_HOST` environment variable.

### DNS Verification

Command:

```
kubectl exec deployment/flask-app -n faralpha -- python -c "import socket; print('MongoDB DNS:', socket.gethostbyname('mongodb.faralpha.svc.cluster.local'))"

```

Actual verification output:

```

MongoDB DNS: 10.97.32.147


```

This confirms that the Flask pod successfully resolved the MongoDB Service hostname to its ClusterIP.

MongoDB is exposed through an internal ClusterIP Service and is not directly exposed outside the cluster.

## 9. Persistent Storage

MongoDB uses Kubernetes PersistentVolume (PV) and PersistentVolumeClaim (PVC).

| Configuration | Value |
|---|---|
| PV Name | mongodb-pv |
| PVC Name | mongodb-pvc |
| Capacity | 2Gi |
| Access Mode | ReadWriteOnce |
| Reclaim Policy | Retain |
| Storage Type | hostPath |
| Mount Path | /data/db |

The MongoDB StatefulSet mounts the PVC at `/data/db`, ensuring database files are stored outside the container's writable layer.

**Storage limitation:** The current Minikube implementation uses hostPath at `/data/mongodb`. This is suitable for local development but is not production-grade shared or highly available storage. Deleting the Minikube cluster can affect access to this data.

## 10. Resource Requests and Limits

Both Flask and MongoDB have configured CPU and memory requests and limits.

| Resource | Request | Limit |
|---|---:|---:|
| CPU | 200m | 500m |
| Memory | 250Mi | 500Mi |

### Explanation

**Requests:** The minimum CPU and memory resources Kubernetes uses when scheduling a container.

**Limits:** The maximum CPU and memory resources a container can consume.

CPU is measured in millicores:

- 200m = 0.2 CPU core.

- 500m = 0.5 CPU core.

Memory is specified in MiB:

- 250Mi = 250 mebibytes.

- 500Mi = 500 mebibytes.

### Resource Verification

```
kubectl describe deployment flask-app -n faralpha



kubectl describe statefulset mongodb -n faralpha

```

Both workloads were verified to have the required requests and limits.

## 11. Horizontal Pod Autoscaler (HPA)

The Flask application uses Horizontal Pod Autoscaler to automatically adjust the number of replicas according to CPU utilization.

Configuration:

| Setting | Value |
|---|---|
| HPA Name | flask-hpa |
| Target Deployment | flask-app |
| CPU Target | 70% |
| Minimum Replicas | 2 |
| Maximum Replicas | 5 |

### HPA Verification

```
kubectl get hpa -n faralpha

```

### Actual Scaling Test

A CPU-intensive workload was executed inside both Flask application pods.

The HPA successfully scaled the Flask Deployment:

`2 replicas → 5 replicas`

After the CPU-intensive workload stopped, the HPA automatically scaled down:

`5 replicas → 2 replicas`

Verified final HPA output:

```

NAME        REFERENCE             TARGETS   MINPODS   MAXPODS   REPLICAS

flask-hpa   Deployment/flask-app  1%/70%    2         5         2


```

The final observed CPU utilization was 1%, and the Deployment returned to its minimum of two replicas.

## 12. Testing and Results

The following tests were performed in the local Minikube environment.

| Test | Result |
|---|---|
| Minikube cluster health | Passed |
| Flask deployment | Passed |
| Two Flask replicas | Passed |
| MongoDB StatefulSet | Passed |
| MongoDB authentication | Passed |
| MongoDB persistent volume binding | Passed |
| Root API endpoint | Passed |
| Health endpoint | Passed |
| POST data insertion | Passed |
| GET data retrieval | Passed |
| Kubernetes DNS resolution | Passed |
| Flask resource verification | Passed |
| MongoDB resource verification | Passed |
| HPA scale-up from 2 to 5 | Passed |
| HPA scale-down from 5 to 2 | Passed |
| Docker Hub image push | Passed |
| Remote image manifest verification | Passed |

### High CPU Load Test

A CPU-intensive process was executed inside both Flask pods. The HPA detected increased CPU usage and increased the replica count to five.

After stopping the load, the number of replicas automatically returned to two.

The test verified the autoscaling configuration in the local environment.

### Testing Limitation

During an earlier concurrent HTTP request test, the local port-forward connection reported a Windows socket disconnection. The port-forward was restarted and subsequent API checks succeeded. This was not confirmed as an application crash.

## 13. Design Choices and Alternatives

### Flask Deployment

A Deployment is used for Flask because it is a stateless application. Kubernetes can easily create, replace, and scale Flask replicas.

Alternative: A StatefulSet could be used, but it is unnecessary for this stateless API.

### MongoDB StatefulSet

A StatefulSet is used because MongoDB requires persistent identity and stable storage.

Alternative: A Deployment with a PVC is possible for some database setups, but StatefulSet is more appropriate for stateful workloads.

### MongoDB Service

A ClusterIP Service provides internal-only database access.

Alternative: NodePort or LoadBalancer could expose MongoDB externally, but this is unnecessary and less secure for the current architecture.

### Persistent Storage

A hostPath-backed PV is used for local Minikube testing.

Alternative: Production deployments should use cloud or infrastructure-backed persistent storage such as AWS EBS, Azure Disk, or an appropriate CSI storage provisioner.

### Autoscaling

HPA is configured with CPU utilization at 70%, a minimum of two replicas, and a maximum of five replicas.

Alternative: HPA can also scale using memory or custom metrics when suitable metrics adapters are configured.

## 14. Troubleshooting

### Check Kubernetes Pods

```
kubectl get pods -n faralpha

```

### Check Flask Logs

```
kubectl logs deployment/flask-app -n faralpha

```

### Check MongoDB Logs

```
kubectl logs mongodb-0 -n faralpha

```

### Check Services

```
kubectl get services -n faralpha

```

### Check Persistent Storage

```
kubectl get pv

kubectl get pvc -n faralpha

```

### Check HPA

```
kubectl get hpa -n faralpha

kubectl top pods -n faralpha

```

### Restart Port Forwarding

If localhost becomes inaccessible, stop the old port-forward process and run:

```
kubectl port-forward service/flask-service 5000:5000 -n faralpha

```

## 15. Screenshots

The `screenshots/` directory contains the captured evidence of project execution and verification.

| Screenshot | Description |
|---|---|
| 01-root-endpoint.png | Flask root endpoint |
| 02-health-check.png | Database health check |
| 03-post-insertion.png | POST request |
| 04-get-retrieval.png | GET request |
| 05-kubernetes-cluster.png | Kubernetes cluster |
| 06-application-pods.png | Application pods |
| 07-deployments.png | Deployment and StatefulSet |
| 08-kubernetes-services.png | Kubernetes Services |
| 09-persistent-storage.png | PV and PVC |
| 10-hpa-scale-up-5.png | HPA scale-up |
| 11-resource-utilization.png | Resource utilization |
| 12-hpa-scale-down-2.png | HPA scale-down |
| 13-docker-image.png | Local Docker image |
| 14-minikube-image.png | Minikube image |
| 15-kubernetes-dns.png | DNS resolution |

## 16. Production Considerations and Limitations

This project is implemented and tested using a local Minikube cluster.

The following improvements would be recommended for production:

1. Use a managed Kubernetes cluster.

2. Use managed MongoDB or a properly configured MongoDB replica set.

3. Use cloud-backed persistent storage.

4. Use Kubernetes Secrets with an external secret manager.

5. Configure TLS and HTTPS.

6. Add monitoring and centralized logging.

7. Configure database backups and recovery.

8. Configure readiness, liveness, and resource monitoring.

9. Use a private container registry if the application requires restricted access.

The current MongoDB configuration uses one replica and should not be considered a highly available database deployment.

## 17. Conclusion

The project successfully demonstrates containerizing a Flask REST API, connecting it to an authenticated MongoDB database, and deploying both components using Kubernetes.

Persistent storage, Kubernetes DNS, CPU and memory resource management, and Horizontal Pod Autoscaler were configured and verified.

The Flask application was tested using GET and POST requests, and the HPA successfully scaled from two to five replicas under CPU load before returning to two
