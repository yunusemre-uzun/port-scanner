from time import sleep
from kafka import KafkaConsumer, TopicPartition
from Logger.log_level import LogLevel
from scanner_controller import ScannerController
from Logger.log_action import Logger
import logging
import json
import sys

MAX_THREAD_COUNT = 4
logger = Logger("NmapScanner")


def main():
    kafka_url = "localhost"
    kafka_port = 29092
    if(len(sys.argv) == 3):
        kafka_url = sys.argv[1]
        kafka_port = sys.argv[2]
    with open('Logs/portScanner.log', mode="w") as file:
         file.write("\n") # erase the log file
    logging.basicConfig(filename='Logs/portScanner.log', level=logging.INFO)
    try :
        consumer = KafkaConsumer(bootstrap_servers='{}:{}'.format(kafka_url, kafka_port), value_deserializer=lambda v: json.loads(v.decode('utf-8')))
    except:
        return
    consumer.assign([TopicPartition('trendyol_port_scanner', 0)])
    for msg in consumer:
        scan_name = msg.value['name']
        host = msg.value["host"]
        ports = msg.value["ports"]
        arguments = msg.value["arguments"]
        os_scan = msg.value["os_scan"]
        scanner = ScannerController(MAX_THREAD_COUNT, kafka_url, kafka_port, scan_name, host, ports, arguments, os_scan)
        scanner.start()
    #result = nmapScanner.scan('127.0.0.1', False, '1-1000')
    #return result


if __name__ == "__main__":
    main()
    