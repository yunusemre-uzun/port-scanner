import logging
from kafka import KafkaConsumer, TopicPartition
import json

class ElasticSearchKafkaConsumer:
    def __init__(self) -> None:
        self._consumer = KafkaConsumer(bootstrap_servers='kafka:9092', value_deserializer=lambda v: json.loads(v.decode('utf-8')))
        self._consumer.assign([TopicPartition('trendyol_port_scanner', 1)])

    def getMessages(self) -> KafkaConsumer:
        for message in self._consumer:
            logging.info(message)
