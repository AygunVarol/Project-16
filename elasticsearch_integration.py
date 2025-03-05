from elasticsearch import Elasticsearch
import config

class ElasticsearchClient:
    def __init__(self):
        self.es = Elasticsearch([{'host': config.ELASTICSEARCH_HOST, 'port': config.ELASTICSEARCH_PORT}])
        self.index = config.INDEX_NAME
        self._ensure_index_exists()

    def _ensure_index_exists(self):
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index)
            print(f"Created index: {self.index}")

    def index_query(self, query: str, optimized_query: str):
        """
        Index a document with the original and optimized queries.
        """
        doc = {
            "query": query,
            "optimized_query": optimized_query
        }
        response = self.es.index(index=self.index, document=doc)
        return response

    def search_query(self, query: str):
        """
        Search for a query document in the ElasticSearch index.
        """
        response = self.es.search(index=self.index, query={"match": {"query": query}})
        return response

if __name__ == "__main__":
    # Simple test indexing
    es_client = ElasticsearchClient()
    response = es_client.index_query("example query", "Optimized: example query")
    print(response)
