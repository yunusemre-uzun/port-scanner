import logging
from kafka import KafkaConsumer, TopicPartition
from Elk.elk_controller import ElkController
import json


class ElasticSearchKafkaConsumer:
    def __init__(self) -> None:
        try:
            self._consumer = KafkaConsumer(bootstrap_servers='kafka:9092', value_deserializer=lambda v: json.loads(v.decode('utf-8')))
        except Exception as err:
            raise err
        self._consumer.assign([TopicPartition('trendyol_port_scanner', 1)])
        self._elk_controller = ElkController()


    def getMessages(self):
        for message in self._consumer:
            logging.info("elk got new message: {}".format(message.value))
            try:
                logging.info("adding message with value: {}".format(message.value))
                response = self._elk_controller.add_new_scan_result(message)
                logging.info(response)
            except Exception as ex:
                logging.error(ex)
                continue
            
