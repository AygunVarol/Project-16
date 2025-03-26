import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from .langchain_utils import get_optimized_query

class QueryOptimizer:
    """
    A class for rewriting and expanding user queries.
    It supports:
        - 'rewriter' for producing a clear and refined version
        - 'expander' for generating additional keyword-enriched queries
        - 'deepseek' to offload the query optimization to an external service
    """
    
    def __init__(self):
        # Determine the best device for model loading
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        try:
            # Load the Rewriter Model
            self.rewriter_tokenizer = AutoTokenizer.from_pretrained("llama-3.2-1B-MLQRECC-Rewriter")
            self.rewriter_model = AutoModelForCausalLM.from_pretrained(
                "llama-3.2-1B-MLQRECC-Rewriter",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            ).to(self.device)

            # Load the Expander Model
            self.expander_tokenizer = AutoTokenizer.from_pretrained("llama-query-expansion-finetuned")
            self.expander_model = AutoModelForCausalLM.from_pretrained(
                "llama-query-expansion-finetuned",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            ).to(self.device)

        except Exception as e:
            print(f"Error loading models: {e}")
            raise

    def _inference(self, query: str, prompt_template: str, tokenizer, model) -> str:
        """
        Helper method to generate a response from the model given a prompt template.
        """
        try:
            # Create the final prompt
            prompt = prompt_template.format(query=query)

            # Prepare inputs on the correct device
            inputs = tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=64,
                temperature=0.3,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )

            # Decode the model output, removing the prompt if repeated
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return generated_text.replace(prompt, "").strip()

        except Exception as e:
            print(f"Inference error: {e}")
            # Fallback to original query if inference fails
            return query

    def optimize_query(self, query: str, model_type: str = "rewriter") -> str:
        """
        Optimize the given query with the specified model type.

        model_type options:
          - "rewriter" : For rewriting the query in a clearer, more refined manner
          - "expander" : For generating keyword-enriched variants
          - "deepseek" : Offloads to the external get_optimized_query() method using the same prompt settings
        """
        if model_type == "rewriter":
            prompt_template = (
                "You are an expert assistant that rewrites user queries to be clearer and more explicit.\n"
                "Original query: {query}\n\n"
                "Please rewrite the above query in a concise, well-structured format:\n"
                "Rewritten query:"
            )
            return self._inference(query, prompt_template, self.rewriter_tokenizer, self.rewriter_model)

        elif model_type == "expander":
            prompt_template = (
                "You are an expert at expanding queries to include additional keywords and context.\n"
                "Original query: {query}\n\n"
                "Please generate an expanded version of this query that adds relevant keywords:\n"
                "Expanded query:"
            )
            return self._inference(query, prompt_template, self.expander_tokenizer, self.expander_model)

        elif model_type == "deepseek":
            # Use the same prompt settings for deepseek as for rewriter
            prompt_template = (
                "You are an expert assistant that rewrites user queries to be clearer and more explicit.\n"
                "Original query: {query}\n\n"
                "Please rewrite the above query in a concise, well-structured format:\n"
                "Optimized query:"
            )
            prompt = prompt_template.format(query=query)
            return get_optimized_query(prompt)

        else:
            raise ValueError("Invalid model type. Choose 'rewriter', 'expander', or 'deepseek'.")

if __name__ == "__main__":
    optimizer = QueryOptimizer()
    test_query = "how do I fix my laptop slow performance?"
    print("Original query:", test_query)

    rewritten = optimizer.optimize_query(test_query, model_type="rewriter")
    print("Rewritten query:", rewritten)

    expanded = optimizer.optimize_query(test_query, model_type="expander")
    print("Expanded query:", expanded)

    deepseek_opt = optimizer.optimize_query(test_query, model_type="deepseek")
    print("DeepSeek optimized query:", deepseek_opt)