from flask import Flask, request, render_template
from Kafka.scan_request_producer import ScanRequestKafkaProducer
from Models.scan_request_model import ScanRequestModel

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main_page():
    return handle_get()

@app.route("/scan", methods=["POST"])
def scan():
    return handle_post()   

def handle_get():
    return render_template('main_page.html', name="Yunus")

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
    return ScanRequestModel(host, port_selection, ports_begin, ports_end, arguments)

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True, port=8085)



