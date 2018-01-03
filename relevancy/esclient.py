from elasticsearch import Elasticsearch
import json
import certifi

class EsClient:
    def __init__(self, url, index_name, doc_type ='candidate'):
        self.doc_type = doc_type
        self.index_name = index_name
        self.url = url
        self.es = Elasticsearch([url], use_ssl=True, ca_certs=certifi.where())

    def execute_query(self, query_str):
        query = json.loads(query_str)
        try:
            res = self.es.search(index=self.index_name, doc_type=self.doc_type,
                            body={"_source": "_id", "query": query})
        except Exception:
            return []
        return [doc['_id'] for doc in res['hits']['hits']]


