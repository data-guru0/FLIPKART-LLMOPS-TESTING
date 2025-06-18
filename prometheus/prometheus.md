Here’s a clear and detailed explanation of your **Prometheus Deployment YAML**, **Service YAML**, and **ConfigMap YAML**, broken down block by block in **simple language**.

---

## 📦 `prometheus-deployment.yaml`

### 🚀 **1. Deployment Block**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: monitoring
```

* `apiVersion: apps/v1`: Using the **Deployment** API from Kubernetes.
* `kind: Deployment`: Specifies you're deploying a **long-running Pod**.
* `metadata`: Identifiers.

  * `name`: Name of the deployment = `prometheus`.
  * `namespace`: Belongs to the `monitoring` namespace.

---

### ⚙️ **2. Deployment Specifications**

```yaml
spec:
  replicas: 1
```

* `replicas`: Run **1 copy** (Pod) of the Prometheus server.

```yaml
  selector:
    matchLabels:
      app: prometheus
```

* **Pod selector**: Match Pods with label `app: prometheus`.

```yaml
  template:
    metadata:
      labels:
        app: prometheus
```

* Defines the **Pod's labels**, matched by the selector above.

```yaml
    spec:
      containers:
        - name: prometheus
          image: prom/prometheus
```

* `containers`: Run the **Prometheus Docker image**.
* `image`: Pulls `prom/prometheus` from Docker Hub.

```yaml
          args:
            - "--config.file=/etc/prometheus/prometheus.yml"
```

* Overrides default args to **tell Prometheus to use your custom config file** from `/etc/prometheus/prometheus.yml`.

```yaml
          ports:
            - containerPort: 9090
```

* Opens **port 9090 inside the container** (Prometheus UI and API).

```yaml
          volumeMounts:
            - name: config-volume
              mountPath: /etc/prometheus
```

* **Mounts a ConfigMap** as a volume inside the container at `/etc/prometheus`.

```yaml
      volumes:
        - name: config-volume
          configMap:
            name: prometheus-config
```

* This volume gets its data from the **ConfigMap named `prometheus-config`** (defined below).

---

### 🌐 **3. Service Block**

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus-service
  namespace: monitoring
```

* This creates a **Service** to access Prometheus from outside the cluster.
* Named `prometheus-service` in `monitoring` namespace.

```yaml
spec:
  selector:
    app: prometheus
```

* Targets Pods with `app: prometheus` (matches the Deployment above).

```yaml
  ports:
    - protocol: TCP
      port: 9090
      targetPort: 9090
      nodePort: 32001 
```

* **port: 9090**: Service’s internal port.
* **targetPort: 9090**: Forwards to container’s 9090.
* **nodePort: 32001**: Exposes Prometheus **on this port on any Node's public IP**.

```yaml
  type: NodePort
```

* Makes Prometheus accessible outside the cluster at `NodeIP:32001`.

---

## 🧾 `prometheus-configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
```

* Defines a **ConfigMap** resource named `prometheus-config`.
* It will be mounted inside the Prometheus Pod.

```yaml
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
```

* Prometheus will **scrape targets every 15 seconds**.

```yaml
    scrape_configs:
      - job_name: 'prometheus'
        static_configs:
          - targets: ['localhost:9090']
```

* This block tells Prometheus to **monitor itself** (scraping its own metrics on `localhost:9090`).

```yaml
      - job_name: 'flask-app'
        metrics_path: /metrics
        static_configs:
          - targets: ['34.29.173.211:5000']
```

* Monitors an **external Flask app**:

  * `metrics_path: /metrics`: Flask must expose metrics at `/metrics`.
  * `target`: Replace `34.29.173.211` with your Flask app's IP.

---

## ✅ Final Summary

| Resource             | Purpose                                                   |
| -------------------- | --------------------------------------------------------- |
| **Deployment**       | Runs Prometheus container with custom config file         |
| **Service**          | Exposes Prometheus at `NodeIP:32001`                      |
| **ConfigMap**        | Provides custom `prometheus.yml` config file to container |
| **Flask App Scrape** | Adds external app to Prometheus monitoring                |

---

