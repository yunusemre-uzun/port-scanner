from flask import Flask, request, render_template
from Kafka.scan_request_producer import ScanRequestKafkaProducer
from Models.scan_request_model import ScanRequestModel
from Elasticsearch.elk_controller import ElasticsearchController

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main_page():
    return handle_get()

@app.route("/scan", methods=["POST"])
def scan():
    return handle_post()

@app.route('/<document_id>', methods=["GET"])
def getDocument(document_id):
    elk_controller = ElasticsearchController()
    document = elk_controller.getScanResult(document_id)
    return document

def handle_get():
    elk_controller = ElasticsearchController()
    scan_results = elk_controller.getAllScanResults()
    return render_template('main_page.html', name="Yunus", scan_results=scan_results)

def handle_post():
    kafka_request = ScanRequestKafkaProducer()
    kafka_request.sendNewRequest(createScanRequestModel())
    return str(request.form)

def createScanRequestModel():
    host = request.form['host']
    port_selection = request.form['portSelection']
    ports_begin = request.form['portsBegin']
    ports_end = request.form['portsEnd']
    arguments = request.form['arguments']
    if 'os_scan' in request.form:
        os_scan = request.form['os_scan']
    else:
        os_scan = False
    return ScanRequestModel(host, port_selection, ports_begin, ports_end, arguments, os_scan)

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True, port=8085)



