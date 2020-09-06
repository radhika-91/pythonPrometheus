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
- #####Docker build
docker build -t flask_prometheus .
docker tag flask_prometheus radhikavya91/flask_prometheus:6
docker push radhikavya91/flask_prometheus:6

- #####Application Deployment
kubectl apply -f myapp_deployment_svc.yaml

- #####Prometheus Deployment
kubectl create configmap prometheus-cm --from-file prometheus.yml
kubectl apply -f prometheus_deployment_svc.yaml

- #####Grafana Deployment
kubectl apply -f grafana_deployment_svc.yaml

####Testing
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
#####Prometheus 
- Check for the tragets monitried by Promethues.
- Check for metrics sample_external_url_up and sample_external_url_response_ms in its Expression dashboard .


#####Grafana
- Add Prometheus as datasource to caliberate graphs for the metrics obtained.

Related images are added in images folder.

