from kafka import KafkaConsumer, TopicPartition
from scanner_controller import ScannerController
import logging
import json

MAX_THREAD_COUNT = 4


def main():
    with open('Logs/portScanner.log', mode="w") as file:
         file.write("\n") # erase the log file
    logging.basicConfig(filename='Logs/portScanner.log', level=logging.INFO)
    consumer = KafkaConsumer(bootstrap_servers='localhost:29092', value_deserializer=lambda v: json.loads(v.decode('utf-8')))
    consumer.assign([TopicPartition('trendyol_port_scanner', 0)])
    print(consumer)
    for msg in consumer:
        scanner = ScannerController(MAX_THREAD_COUNT)
        host = msg.value["host"]
        ports = msg.value["ports"]
        arguments = msg.value["arguments"]
        scanner.run(host, ports, arguments)
    #result = nmapScanner.scan('127.0.0.1', False, '1-1000')
    #return result


if __name__ == "__main__":
    main()
    