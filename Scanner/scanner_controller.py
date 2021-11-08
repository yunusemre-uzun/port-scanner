import logging
import threading
import json

from kafka import KafkaProducer
from Models.scan_result import ScanResult

from nmap_scanner import NmapScanner

class ScannerController(threading.Thread):

    def __init__(self, max_number_of_threads, kafka_url, kafka_port) -> None:
        threading.Thread.__init__(self)
        self._nmapScanner = NmapScanner(max_number_of_threads)
        logging.info("nmap scanner: {}".format(self._nmapScanner))
        self._producer = KafkaProducer(bootstrap_servers='{}:{}'.format(kafka_url, kafka_port), \
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def run(self, target, ports, arguments, scan_name):
        result =  self._nmapScanner.scan(target, True, ports, arguments)
        self.kafkaProducerElasticSearchIndex(result, scan_name)
        return result
    
    def kafkaProducerElasticSearchIndex(self, result: ScanResult, scan_name):
        # Use partition 1 to send scan result to elastiksearch
        logging.info("Sending scan result with message: {} from partition: {}".format(result.toJSON(), 1))
        self._producer.send('trendyol_port_scanner', {"name": scan_name, 'result': result.toJSON()}, b'scan_result', partition=1)
        result.onResponseSent()
