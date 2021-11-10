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
    _index_name = "scan_result"
    def __init__(self) -> None:
        self.__connect_elasticsearch()
        if self._connected:
            is_created = self.create_index()
            logging.info("creating index: {}".format(is_created))
    
    def __connect_elasticsearch(self):
        logging.info("trying to connect elasticseach")
        self._elk = Elasticsearch([{"host": "elasticsearch", "port": 9200}])
        self._connected = self.__connectionCheckElasticsearch()
    
    def __connectionCheckElasticsearch(self) -> bool:
        if self._elk.ping():
            logging.info("connected to elasticseach")
            return True
        else:
            logging.info("could not connect to elasticseach")
            return False
    
    def create_index(self) -> bool:
        created = False
        try:
            logging.info("creating index. current indices: {}".format(self._elk.indices.exists(self._index_name)))
            if not self._elk.indices.exists(self._index_name):
                # Ignore 400 means to ignore "Index Already Exist" error.
                logging.info("Settings {}".format(self._settings_json))
                response = self._elk.indices.create(index=self._index_name, ignore=400, body=self._settings_json)
                logging.info("new index created with response {}".format(response))
            created = True
        except Exception as ex:
            logging.error(ex)
            raise ex
        finally:
            return created
    
    def add_new_scan_result(self, message):
        if not self._connected:
            self.__connect_elasticsearch()
        try:
            logging.info("adding message with value: {}".format(message.value))
            response = self._elk.index(index="scan_result", id=uuid4(), body=json.dumps(message.value)) # Index new data
            logging.info(response)
        except Exception as ex:
            logging.error(ex)
        finally:
            return response