from kubernetes import client, config, watch
from openshift.dynamic import DynamicClient, exceptions
from flask import Flask, render_template

app = Flask(__name__)
k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)
v1 = client.CoreV1Api(k8s_client)

@app.route('/')
def index():
    v1_pods = dyn_client.resources.get(api_version='v1', kind='Pod')
    v1_pods.get()

    return render_template('index.html', items=v1_pods.get().items)

@app.route('/log/<namespace>/<id>')
def log(namespace, id):
    return render_template('stream.html', namespace=namespace, id=id)

@app.route('/stream/<namespace>/<id>')
def stream(namespace, id):
    def generate():
        w = watch.Watch()

        for line in w.stream(v1.read_namespaced_pod_log, name=id, namespace=namespace):
            yield(line + '\n')

    return app.response_class(generate(), mimetype='text/plain')

app.run()
