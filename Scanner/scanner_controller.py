import threading
import json

from kafka import KafkaProducer

from nmap_scanner import NmapScanner

class ScannerController(threading.Thread):

    def __init__(self, max_number_of_threads) -> None:
        threading.Thread.__init__(self)
        self._nmapScanner = NmapScanner(max_number_of_threads)
        self._producer = KafkaProducer(bootstrap_servers='localhost:29092', \
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def run(self, target, ports, arguments):
        result =  self._nmapScanner.scan(target, True, ports, arguments)
        self.kafkaProducerElasticSearchIndex(result)
        return result
    
    def kafkaProducerElasticSearchIndex(self, result):
        # Use partition 1 to send scan result to elastiksearch
        self.__producer.send('trendyol_port_scanner', result, b'scan_result', partition=1)
