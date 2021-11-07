import logging
from kafka import KafkaConsumer, TopicPartition
from elasticsearch import Elasticsearch
import json

class ElasticSearchKafkaConsumer:
    def __init__(self) -> None:
        try:
            self._consumer = KafkaConsumer(bootstrap_servers='kafka:9092', value_deserializer=lambda v: json.loads(v.decode('utf-8')))
        except Exception as err:
            raise err
        self._consumer.assign([TopicPartition('trendyol_port_scanner', 1)])
        self._elk = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
    
    def __connectionCheckElasticsearch(self):
        if self._elk.ping():
            return True
        else:
            return False
    
    def _create_index(self, index_name='recipes'):
        created = False
        # index settings
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "members": {
                    "dynamic": "strict",
                    "properties": {
                        "title": {
                            "type": "text"
                        },
                        "submitter": {
                            "type": "text"
                        },
                        "description": {
                            "type": "text"
                        },
                        "calories": {
                            "type": "integer"
                        },
                    }
                }
            }
        }
        try:
            if not self._elk.indices.exists(index_name):
                # Ignore 400 means to ignore "Index Already Exist" error.
                self._elk.indices.create(index=index_name, ignore=400, body=settings)
                logging.info('new index created with name{}'.format(index_name))
            created = True
        except Exception as ex:
            logging.error(ex)
        finally:
            return created

    def getMessages(self) -> KafkaConsumer:
        for message in self._consumer:
            if self.__connectionCheckElasticsearch():
                self._create_index()
            else:
                logging.error("Can not connect elasticsearch server")
            logging.info(message)
