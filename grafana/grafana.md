Here's a detailed breakdown of **each block** in your **Grafana deployment YAML** file, explained in simple terms:

---

### 🚀 **1. Deployment Configuration**

This section defines how Grafana will be **deployed as a Pod in your cluster.**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: monitoring
```

* `apiVersion: apps/v1`: Uses Kubernetes Deployment API.
* `kind: Deployment`: Specifies this is a **Deployment** resource (manages Pods).
* `metadata`: Metadata for identifying the resource.

  * `name: grafana`: The name of the deployment.
  * `namespace: monitoring`: Deploys Grafana into the `monitoring` namespace.

---

### ⚙️ **2. Deployment Specifications**

Defines the actual **Pod and container settings.**

```yaml
spec:
  replicas: 1
```

* `replicas: 1`: Only **one instance** (Pod) of Grafana will run.

```yaml
  selector:
    matchLabels:
      app: grafana
```

* `selector`: Tells the Deployment to manage Pods **with the label `app: grafana`**.

```yaml
  template:
    metadata:
      labels:
        app: grafana
```

* `template`: Defines the **blueprint** for the Pods the Deployment creates.
* `labels`: Used for matching with the selector above.

```yaml
    spec:
      containers:
        - name: grafana
          image: grafana/grafana
          ports:
            - containerPort: 3000
```

* `containers`: List of containers to run in the Pod.

  * `name: grafana`: Name of the container.
  * `image: grafana/grafana`: Pulls the official **Grafana image** from Docker Hub.
  * `ports: containerPort: 3000`: Exposes **port 3000** (Grafana's default UI port) **inside the container**.

---

### 🌐 **3. Service Configuration**

Creates a **Service** to expose Grafana outside the cluster.

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: grafana-service
  namespace: monitoring
```

* `kind: Service`: Creates a **Kubernetes Service**.
* `name: grafana-service`: Name of the service.
* `namespace: monitoring`: Service is placed in the same namespace.

```yaml
spec:
  selector:
    app: grafana
```

* `selector`: This Service will route traffic to **Pods with `app: grafana` label** (the one created above).

```yaml
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
      nodePort: 32000  
```

* `port: 3000`: Port on which the Service is **exposed inside the cluster**.
* `targetPort: 3000`: **Forwards** traffic to **container port 3000**.
* `nodePort: 32000`: **Exposes** Grafana on **port 32000** on each Node's IP.

```yaml
  type: NodePort
```

* `type: NodePort`: Exposes the service **outside the cluster** via a **Node IP and port 32000**.

---

### ✅ Summary

| Component             | Purpose                                               |
| --------------------- | ----------------------------------------------------- |
| **Deployment**        | Runs Grafana as a container inside a Pod              |
| **Namespace**         | Deploys Grafana in the `monitoring` space             |
| **Selector & Labels** | Link between Deployment and Service                   |
| **Service**           | Makes Grafana accessible outside using NodePort 32000 |
| **Port 3000**         | Default Grafana UI port                               |

---

Let me know if you want to:

* Add **persistent volume** for dashboards.
* Set up **admin password** with `env`.
* Use **LoadBalancer** instead of NodePort for cloud access.
