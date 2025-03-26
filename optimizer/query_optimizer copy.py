import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .langchain_utils import get_optimized_query
from .query_analyzer import analyze_query

class QueryOptimizer:
    def __init__(self):
        # Determine the best device for model loading
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        try:
            # Load the ML-QRECC Rewriter model
            self.rewriter_tokenizer = AutoTokenizer.from_pretrained("llama-3.2-1B-MLQRECC-Rewriter")
            self.rewriter_model = AutoModelForCausalLM.from_pretrained(
                "llama-3.2-1B-MLQRECC-Rewriter",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            ).to(self.device)
            
            # Load the Query Expander model
            self.expander_tokenizer = AutoTokenizer.from_pretrained("llama-query-expansion-finetuned")
            self.expander_model = AutoModelForCausalLM.from_pretrained(
                "llama-query-expansion-finetuned", 
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            ).to(self.device)
        
        except Exception as e:
            print(f"Error loading models: {e}")
            raise
    
    def _inference(self, query: str, prompt_template: str, tokenizer, model) -> str:
        try:
            prompt = prompt_template.format(query=query)
            # Ensure inputs are on the same device as the model
            inputs = tokenizer(prompt, return_tensors="pt").to(self.device)
            
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=50,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
            
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove the prompt from the generated text if present
            return generated_text.replace(prompt, "").strip()
        
        except Exception as e:
            print(f"Inference error: {e}")
            return query  # Fallback to original query if inference fails
    
    def optimize_query(self, query: str, model_type: str = "rewriter") -> str:
        """
        Optimize the given query using the specified model type.
        
        model_type: "rewriter", "expander", or "deepseek"
        """
        analysis = analyze_query(query)
        print(f"Query analysis: {analysis}")
        
        if model_type == "rewriter":
            prompt_template = "Rewrite the question: {query}\n\nRewritten question:"
            return self._inference(query, prompt_template, self.rewriter_tokenizer, self.rewriter_model)
        elif model_type == "expander":
            prompt_template = "Generate expanded versions of this query: {query}\n\nExpanded queries:"
            return self._inference(query, prompt_template, self.expander_tokenizer, self.expander_model)
        elif model_type == "deepseek":
            return get_optimized_query(query)
        else:
            raise ValueError("Invalid model type. Choose 'rewriter', 'expander', or 'deepseek'.")

if __name__ == "__main__":
    optimizer = QueryOptimizer()
    test_query = "how do I fix my laptop slow performance?"
    print("Original query:", test_query)
    print("Rewritten query:", optimizer.optimize_query(test_query, model_type="rewriter"))
    print("Expanded query:", optimizer.optimize_query(test_query, model_type="expander"))
    print("DeepSeek optimized query:", optimizer.optimize_query(test_query, model_type="deepseek"))