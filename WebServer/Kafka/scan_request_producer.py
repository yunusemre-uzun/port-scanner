from kafka import KafkaProducer
from Models.scan_request_model import ScanRequestModel
import json

class ScanRequestKafkaProducer:

    def __init__(self) -> None:
        self.__producer: KafkaProducer = KafkaProducer(bootstrap_servers='kafka:9092', \
            value_serializer=lambda v: json.dumps(v).encode('utf-8')) #Create kafka producer
        return
    
    def sendNewRequest(self, scan_request: ScanRequestModel):
        # Use partition 0 to send scan request to scanner
        self.__producer.send('trendyol_port_scanner', scan_request.createScanRequest(), b'scan_request', partition=0)
    
