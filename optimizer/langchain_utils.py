import config
import logging
import requests  # Required if Groq client uses HTTP calls internally
from groq import Groq
from config import GROQ_AI_API_KEY

# Initialize the Groq client with your Groq AI API key.
groq_client = Groq(api_key=GROQ_AI_API_KEY)

def get_optimized_query(prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
    """
    Optimizes a user query using Groq's deepseek‑r1‑distill‑llama‑70b model.
    
    This function is part of our Query Analysis project for multimedia applications.
    It prepares a conversation history with a system prompt and the user's query,
    then calls the Groq API to generate an optimized version of the query for improved search performance.
    
    Parameters:
      prompt (str): The user query to be optimized.
      max_tokens (int, optional): Maximum number of tokens for the response. Defaults to 150.
      temperature (float, optional): Temperature for response generation. Defaults to 0.7.
    
    Returns:
      str: The optimized query from the Groq deepseek model, or an error message if the generation fails.
    """
    if not prompt:
        return "Error: Prompt cannot be empty."
    
    # Prepare conversation history with a project-specific system prompt.
    chat_history = [
        {
            "role": "system",
            "content": (
                "You are a query optimization assistant for a multimedia application. "
                "Rewrite and optimize the following query for improved search performance."
            )
        },
        {"role": "user", "content": prompt}
    ]
    
    try:
        response = groq_client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            #model="llama-3.3-70b-versatile",
            messages=chat_history,
            max_tokens=max_tokens,
            temperature=temperature
        )
        # Extract and return the optimized query from the API response.
        optimized_query = response.choices[0].message.content
        return optimized_query
    except Exception as e:
        logging.exception("Error during deepseek model query optimization")
        return f"Error during query optimization: {str(e)}"

if __name__ == "__main__":
    sample_prompt = "best ways to repair a smartphone screen"
    print("Optimized Query:", get_optimized_query(sample_prompt))