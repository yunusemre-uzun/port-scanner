from elasticsearch import Elasticsearch
import logging
from uuid import uuid4
import json

class ElkController:

    _settings_json = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "members": {
                    "dynamic": "strict",
                    "properties": {
                        "name": {
                            "type": "text"
                        },
                        "result": {
                            "type": "nested"
                        },
                        "error": {
                            "type": "text"
                        }
                    }
                }
            }
        }
    _index_name = "scan_results"
    def __init__(self) -> None:
        self.__connect_elasticsearch()
        if self._connected:
            self.__create_index()
    
    def __connect_elasticsearch(self):
        logging.info("trying to connect elasticseach")
        self._elk = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
        self._connected = self.__connectionCheckElasticsearch()
    
    def __connectionCheckElasticsearch(self) -> bool:
        if self._elk.ping():
            logging.info("connected to elasticseach")
            return True
        else:
            logging.info("could not connect to elasticseach")
            return False
    
    def __create_index(self) -> bool:
        created = False
        try:
            if not self._elk.indices.exists(self._index_name):
                # Ignore 400 means to ignore "Index Already Exist" error.
                self._elk.indices.create(index=self._index_name, ignore=400, body=self.settings)
                logging.info('new index created with name {}'.format(self._index_name))
            created = True
        except Exception as ex:
            raise ex
        finally:
            return created
    
    def add_new_scan_result(self, message):
        if not self._connected:
            self.__connect_elasticsearch()
        try:
            logging.info("adding message with value: {}".format(message.value))
            response = self._elk.index(index='scan_result', id=uuid4(), body=json.dumps(message.value)) # Index new data
            logging.info(response)
        except Exception as ex:
            logging.error(ex)
        finally:
            return response