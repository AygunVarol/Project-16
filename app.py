from flask import Flask, request, jsonify
from flask_cors import CORS
from optimizer.query_optimizer import QueryOptimizer
from elasticsearch_integration import ElasticsearchClient

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

optimizer = QueryOptimizer()
es_client = ElasticsearchClient()

@app.route('/')
def home():
    return (
        "Welcome to the Query Optimizer API. "
        "Use /rewriter, /expander, or /deepseek endpoints to POST your query."
    )

def process_query(model_type):
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'Invalid request, "query" field is required'}), 400
    query = data['query']
    try:
        optimized_query = optimizer.optimize_query(query, model_type=model_type)
        es_client.index_query(query, optimized_query)
        return jsonify({'optimized_query': optimized_query})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rewriter', methods=['POST'])
def rewriter():
    return process_query("rewriter")

@app.route('/expander', methods=['POST'])
def expander():
    return process_query("expander")

@app.route('/deepseek', methods=['POST'])
def deepseek():
    return process_query("deepseek")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)