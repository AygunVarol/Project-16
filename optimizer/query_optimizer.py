from .langchain_utils import get_optimized_query

class QueryOptimizer:
    def __init__(self):
        # Initialize any required components (e.g., connection to LLM API) here.
        pass

    def optimize_query(self, query: str) -> str:
        """
        Optimize the given query using LangChain-based utilities.
        """
        optimized_query = get_optimized_query(query)
        return optimized_query

if __name__ == "__main__":
    # Simple test of the query optimizer
    optimizer = QueryOptimizer()
    test_query = "how do I fix my laptop slow performance?"
    print("Original query:", test_query)
    print("Optimized query:", optimizer.optimize_query(test_query))
