import pandas as pd

def load_ml_qrecc_queries(filepath: str):
    """
    Load the ML-QRECC dataset from a JSON file.
    
    The ML-QRECC dataset is available at: https://github.com/apple/ml-qrecc
    Please ensure the repository is cloned locally and the correct JSON file is provided.
    This function assumes that the dataset is in JSON lines format.
    """
    try:
        df = pd.read_json(filepath, lines=True)
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

if __name__ == "__main__":
    # Example usage: adjust the file path to point to your local copy of the ML-QRECC dataset.
    df = load_ml_qrecc_queries("ml_qrecc_train.json")
    if df is not None:
        print(df.head())