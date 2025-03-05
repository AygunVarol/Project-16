from .langchain_utils import get_optimized_query
from .query_analyzer import analyze_query

class QueryOptimizer:
    def __init__(self):
        # Initialize any required components (e.g., connection to LLM API) here.
        pass

    def optimize_query(self, query: str) -> str:
        """
        Optimize the given query using LangChain-based utilities.
        This function first analyzes the query for inefficiencies and then
        calls the optimization function to reformulate the query.
        """
        # Analyze the query for inefficiencies
        analysis = analyze_query(query)
        print(f"Query analysis: {analysis}")
        
        # Use the analysis result to guide optimization.
        # In a more advanced system, the analysis could adjust the LLM prompt.
        optimized_query = get_optimized_query(query)
        return optimized_query

if __name__ == "__main__":
    optimizer = QueryOptimizer()
    test_query = "how do I fix my laptop slow performance?"
    print("Original query:", test_query)
    print("Optimized query:", optimizer.optimize_query(test_query))
