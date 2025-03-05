from flask import Flask, request, jsonify
from optimizer.query_optimizer import QueryOptimizer
from elasticsearch_integration import ElasticsearchClient

app = Flask(__name__)

optimizer = QueryOptimizer()
es_client = ElasticsearchClient()

@app.route('/optimize', methods=['POST'])
def optimize_query():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'Invalid request, "query" field is required'}), 400

    query = data['query']
    try:
        # Analyze and optimize the query
        optimized_query = optimizer.optimize_query(query)
        # Index both the original and optimized query into ElasticSearch
        es_client.index_query(query, optimized_query)
        return jsonify({'optimized_query': optimized_query})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
