from flask import Flask, Response

import prometheus_client
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR
import time
import requests


CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

class CustomCollector(object):
    def __init__(self):
        pass

    def get_respomse_time(self,url):
        res = requests.get(url)
        #return res.elapsed.total_seconds * 1000
        return res


    def collect(self):

        # c = CounterMetricFamily("HttpRequests", 'Help text', labels=['app'])
        # c.add_metric(["example"], 2000)
        # yield c

        url_200="https://httpstat.us/200"
        response_200 = self.get_respomse_time(url_200)
        c1 = GaugeMetricFamily("sample_external_url_up", 'App status', labels=['url'])

        if response_200.status_code == 200:
            c1.add_metric([url_200], 1)
        else:
            c1.add_metric([url_200], 0)
        yield c1


        g1 = GaugeMetricFamily("sample_external_url_response_ms", 'Response time in ms', labels=['url'])
        g1.add_metric([url_200], response_200.elapsed.total_seconds()*1000)
        yield g1

        url_503 = "https://httpstat.us/503"
        response_503 = self.get_respomse_time(url_503)
        c2 = GaugeMetricFamily("sample_external_url_up", 'App status', labels=['url'])

        if response_503.status_code == 200:
            c2.add_metric([url_503], 1)
        else:
            c2.add_metric([url_503], 0)
        yield c2

        g2 = GaugeMetricFamily("sample_external_url_response_ms", 'Response time in ms', labels=['url'])
        g2.add_metric(["https://httpstat.us/503"], response_503.elapsed.total_seconds() * 1000)
        yield g2

app = Flask(__name__)

@app.route('/test/')
def test():
    return 'rest'

@app.route('/')
def test1():
    return 'landing page'

@app.errorhandler(500)
def handle_500(error):
    return str(error), 500

@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    REGISTRY.register(CustomCollector())
    REGISTRY.unregister(PROCESS_COLLECTOR)
    REGISTRY.unregister(PLATFORM_COLLECTOR)
    REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])

    app.run(host='0.0.0.0')
