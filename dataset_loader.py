import pandas as pd

def load_google_search_queries(filepath: str):
    """
    Load the Google Search Query Dataset from a CSV file.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

if __name__ == "__main__":
    # Example usage (adjust the file path as needed)
    df = load_google_search_queries("google_search_queries.csv")
    if df is not None:
        print(df.head())
