from elasticsearch import Elasticsearch

class ElasticsearchController:
    
    def __init__(self) -> None:
        self._elk = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
    
    def getAllScanResults(self):
        all_results = self._elk.search(index="scan_result", query={"match_all": {}}, stored_fields=[], _source=["name"], size= 100)["hits"]["hits"]
        scan_result_ids = []
        for result in all_results:
            print(result)
            name = result["_source"]["name"]
            id = result["_id"]
            scan_result_ids.append(["{}({})".format(name, id), id])
        return scan_result_ids
    
    def getScanResult(self, id):
        result = self._elk.search(index="scan_result", query={"terms": { "_id": [ id ] }}, stored_fields=["_id"], _source=[])["hits"]["hits"][0]
        return result