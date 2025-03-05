from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from optimizer.query_optimizer import QueryOptimizer
from elasticsearch_integration import ElasticsearchClient

app = FastAPI(title="Query Analysis API")
optimizer = QueryOptimizer()
es_client = ElasticsearchClient()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    optimized_query: str

@app.post("/optimize", response_model=QueryResponse)
def optimize_query(request: QueryRequest):
    query = request.query
    try:
        # Optimize the query using LangChain
        optimized_query = optimizer.optimize_query(query)
        # Index both the original and optimized query into ElasticSearch
        es_client.index_query(query, optimized_query)
        return QueryResponse(optimized_query=optimized_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
