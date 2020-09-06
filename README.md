### pythonPrometheus

- Application monitors urls https://httpstat.us/200 and https://httpstat.us/503
and send the response time and application status in below format.
- It exposes response time and status of these url in /metrics endpoint in below format using promethues client library.
```
curl localhost:5000/metrics
# HELP sample_external_url_up App status
# TYPE sample_external_url_up gauge
sample_external_url_up{url="https://httpstat.us/200"} 1.0
# HELP sample_external_url_response_ms Response time in ms
# TYPE sample_external_url_response_ms gauge
sample_external_url_response_ms{url="https://httpstat.us/200"} 58.827999999999996
# HELP sample_external_url_up App status
# TYPE sample_external_url_up gauge
sample_external_url_up{url="https://httpstat.us/503"} 0.0
# HELP sample_external_url_response_ms Response time in ms
# TYPE sample_external_url_response_ms gauge
sample_external_url_response_ms{url="https://httpstat.us/503"} 37.602
```
- These metrics are scrapped by Promethues.
- Grafana is uisng Prometues Data source to get these metrics and can ne used further to make dashborad from them.


### Steps
##### - Docker build
docker build -t flask_prometheus .
docker tag flask_prometheus radhikavya91/flask_prometheus:6
docker push radhikavya91/flask_prometheus:6

##### - Application Deployment
kubectl apply -f myapp_deployment_svc.yaml

##### - Prometheus Deployment
kubectl create configmap prometheus-cm --from-file prometheus.yml
kubectl apply -f prometheus_deployment_svc.yaml

##### - Grafana Deployment
kubectl apply -f grafana_deployment_svc.yaml

```
 kubectl get deployments
 
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
grafana                 1/1     1            1           18h
prometheus-deployment   2/2     2            2           19h
radhika-app             2/2     2            2           18h

kubectl get svc

NAME                  TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
grafanasvc            NodePort    10.104.8.207   <none>        3000:32645/TCP   18h
kubernetes            ClusterIP   10.96.0.1      <none>        443/TCP          20h
prometheus-service    NodePort    10.97.44.114   <none>        9090:30900/TCP   19h
radhika-flaskappsvc   NodePort    10.99.111.3    <none>        5000:30901/TCP   18h
```

### Testing
To test on metrics exposed by application on /metrics
```
curl localhost:5000/metrics
# HELP sample_external_url_up App status
# TYPE sample_external_url_up gauge
sample_external_url_up{url="https://httpstat.us/200"} 1.0
# HELP sample_external_url_response_ms Response time in ms
# TYPE sample_external_url_response_ms gauge
sample_external_url_response_ms{url="https://httpstat.us/200"} 58.827999999999996
# HELP sample_external_url_up App status
# TYPE sample_external_url_up gauge
sample_external_url_up{url="https://httpstat.us/503"} 0.0
# HELP sample_external_url_response_ms Response time in ms
# TYPE sample_external_url_response_ms gauge
sample_external_url_response_ms{url="https://httpstat.us/503"} 37.602
```
##### Prometheus 
- Check for the tragets monitried by Promethues.
- Check for metrics sample_external_url_up and sample_external_url_response_ms in its Expression dashboard .


##### Grafana
- Add Prometheus as datasource to caliberate graphs for the metrics obtained.

Related images are added in images folder.

