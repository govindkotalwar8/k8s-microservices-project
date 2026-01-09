# k8s-microservices-project

## Project Overview

This project demonstrates the migration of a monolithic-style application into a cloud-native microservices architecture using Kubernetes. The application is deployed on a Kubernetes cluster created using **kind (Kubernetes in Docker)** running on an **AWS EC2 instance**.

The focus of this project is to implement production-like Kubernetes concepts including containerization, deployments, service discovery, autoscaling, and persistent storage.

---

## Microservices Architecture

**Architecture:**

* `screenshots/architecture.png`



The application is composed of two independent microservices:

### 1. Product Service

* Stateless service
* Returns a list of products
* Horizontally scalable using HPA

### 2. Order Service

* Stateful service
* Persists order data using Kubernetes Persistent Volumes
* Data survives pod restarts

Each microservice is built, containerized, and deployed independently.

---

## Tools and Technologies Used

* Kubernetes (kind)
* Docker & Docker Hub
* Python (Flask)
* kubectl
* AWS EC2
* Kubernetes Metrics Server
* BusyBox (for load generation)

---

## Project Structure

```
project/
├── product-service/
│   ├── app.py
│   ├── Dockerfile
│   ├── product-deployment.yaml
│   └── product-service.yaml
│
├── order-service/
│   ├── app.py
│   ├── Dockerfile
│   ├── order-deployment.yaml
│   ├── pv.yaml
│   └── pvc.yaml
│
├── product-hpa.yaml
├── README.md
└── screenshots/
```

---

## Kubernetes Cluster Setup

A Kubernetes cluster was created using **kind** on an AWS EC2 instance.
The `kubectl` CLI was configured to interact with the cluster.

### Verification Commands

```bash
kubectl get nodes
kubectl cluster-info
```

**Screenshot:**

* `screenshots/01-cluster-nodes.png`

---

## Containerization

Each microservice has its **own Dockerfile** and is built independently.

### Docker Images

* `<dockerhub-username>/product-service:v1`
* `<dockerhub-username>/order-service:v1`

Images were built and pushed to Docker Hub.

**Screenshot:**

* `screenshots/02-docker-images.png`

---

## Kubernetes Deployments

### Product Service Deployment

* Multiple replicas
* CPU requests defined for autoscaling

### Order Service Deployment

* Single replica
* Persistent volume mounted at `/data`

### Commands Used

```bash
kubectl apply -f product-deployment.yaml
kubectl apply -f order-deployment.yaml
```

**Screenshots:**

* `screenshots/03-product-and-orders-pods-running.png`

---

## Service Discovery and Networking

Both microservices are exposed using **ClusterIP Services** for internal communication.

* Product service accessed via Kubernetes DNS:

  ```
  http://product-service
  ```
* Order service tested using port forwarding.

### Commands

```bash
kubectl get svc
kubectl port-forward deployment/order-service 5002:5002
```

**Screenshot:**

* `screenshots/05-services-list.png`

---

## Horizontal Pod Autoscaling (HPA)

A Horizontal Pod Autoscaler was configured for the **product-service** based on CPU utilization.

### Load Generation

Artificial load was generated using a BusyBox pod:

```bash
kubectl run load-test --rm -it --image=busybox -- sh
while true; do wget -q -O- http://product-service; done
```

### Result

* Product service pods scaled up automatically under load
* Pods scaled down after load stopped

**Screenshots:**

* `screenshots/07-hpa-pods-scaling.png`

---

## Persistent Storage and Data Persistence

### Persistent Volume and Claim

* A statically provisioned PersistentVolume named `testpv` was created
* A PersistentVolumeClaim (`order-pvc`) was explicitly bound to this volume
* Storage was mounted inside the order service container at `/data`

### Verification

```bash
kubectl get pv,pvc
```

**Screenshot:**

* `screenshots/08-pv-pvc-bound.png`

---

## Data Persistence Validation

The order service writes data to a file inside the mounted volume.

### Test Procedure

1. Create order data using the order service API
2. Delete the order-service pod
3. Allow Kubernetes to recreate the pod
4. Verify previously stored data is still available

This confirms that data persists across pod restarts.

**Screenshots:**

* `screenshots/09-order-data-before-restart.png`
* `screenshots/10-order-data-after-restart.png`

---

## Challenges Faced and Solutions

### PVC Stuck in Pending State

**Issue:** PVC remained in `Pending` due to default StorageClass behavior
**Solution:** Disabled StorageClass and explicitly bound PVC to a static PV

### No LoadBalancer Support in kind

**Issue:** kind does not support cloud LoadBalancers
**Solution:** Used ClusterIP services and port forwarding for access

### HPA Not Scaling Initially

**Issue:** Metrics not available
**Solution:** Installed Kubernetes Metrics Server and configured CPU requests

---

## Conclusion

This project successfully demonstrates:

* Microservices deployment using Kubernetes
* Independent containerization with separate Dockerfiles
* Service discovery using Kubernetes DNS
* Horizontal Pod Autoscaling under load
* Persistent storage using PV and PVC
* Data durability across pod restarts

The setup closely reflects real-world Kubernetes deployments and common DevOps troubleshooting scenarios.