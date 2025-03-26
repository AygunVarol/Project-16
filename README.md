# Project-16

## Team 23: Ducktor ![DALL·E 2025-03-12 09 22 36 - A cartoon-style duck dressed as a PhD graduate  The duck wears a black academic gown, a mortarboard cap with a tassel, and round glasses  It holds a d - Kopya](https://github.com/user-attachments/assets/2e35cf31-4e02-4e33-8fe4-c80e519a09a2)

## Members: Fujia Yu, Aygün Varol

# Query Analysis of Large Language Models Using LangChain for Multimedia Application

## Overview
This project aims to optimize poorly structured user queries by analyzing and rewriting them using advanced techniques inspired by LangChain and visual reasoning research (e.g., “Rethinking Step-by-step Visual Reasoning in LLMs”). The optimized queries are then indexed in ElasticSearch for improved search performance. A user interface (to be developed in React.js) will allow users to enter queries and receive optimized versions.

# Workflow
![Başlıksız Diyagram](https://github.com/user-attachments/assets/faa079a4-6f68-4aa5-b681-0fe96fc96299)

# User Interface
![resim](https://github.com/user-attachments/assets/9e9b57fb-b06b-46a1-a3f0-0df06509d175)

## How to Start
1. **Collect Dataset:**  
   We use two key datasets to train our system:
   - ML‑QRECC Dataset: Provides query-rewriting pairs to help transform vague or ambiguous queries into clearer ones. [ML‑QRECC dataset](https://github.com/apple/ml-qrecc)
   - Query Expansion Dataset: Offers query-expansion pairs to enrich queries with additional relevant keywords. [Query Expansion Dataset](https://huggingface.co/datasets/s-emanuilov/query-expansion)

2. **Fine-tuning:**
   We fine-tuned the LLaMA-3.2-1B-Instruct model on these datasets to create specialized models for different optimization tasks. Both models are available on Hugging Face:
   - Query Expansion Model: [llama-query-expansion-finetuned](https://huggingface.co/Aygun/llama-query-expansion-finetuned)
   - Query Rewriter Model: [llama-3.2-1B-MLQRECC-Rewriter](https://huggingface.co/Aygun/llama-3.2-1B-MLQRECC-Rewriter)

3. **Analyze Query Inefficiencies:**
   Our system first identifies common issues in user queries—such as ambiguity, brevity, or missing keywords—using the logic provided in `optimizer/query_analyzer.py`.

4. **Optimize Query Structures:**  
   We leverage advanced techniques via LangChain and custom prompt engineering to reformat and optimize queries for better AI comprehension. See `optimizer/langchain_utils.py` for functions that interface with our language models (or an external service) to perform query optimization.

5. **Query Reformulation System:**  
   By combining the analysis and optimization modules, our AI-powered system improves search intent recognition by generating refined and enriched versions of user queries.

6. **ElasticSearch Integration:**  
   The optimized queries are indexed and tested for performance using ElasticSearch. Integration details can be found in `elasticsearch_integration.py`.

7. **User Interface (React.js):**  
   A user-friendly React.js interface allows users to input queries and select which optimization method to apply (rewriter, expander, or DeepSeek). The Flask backend is designed to seamlessly integrate with this frontend.

## Application Components
- **Backend API:** Python-based API built with Flask.
- **Query Analysis & Optimization:** Combines query inefficiency analysis (in `optimizer/query_analyzer.py`) with advanced query reformulation using custom prompt engineering. For external query optimization services, the system now leverages LangChain utilities to call the Groq API (see `optimizer/langchain_utils.py`) to generate optimized queries.
- **Search Indexing:** Integrated with ElasticSearch via `elasticsearch_integration.py` to index both the original and optimized queries, enabling performance testing and enhanced retrieval.
- **Frontend:** A planned React.js interface that allows users to submit queries and choose between multiple optimization methods (rewriter, expander, or DeepSeek).

## Setup and Running
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
    ```
2. Configure `config.py` with your settings (ElasticSearch host/port, API keys, etc.).
3. Run the Flask API server:
   ```bash
   python app.py
   ```
4. Use the `/optimize` endpoint to submit queries and receive optimized versions.

5. Create a React UI
   ```
   npx create-react-app query-optimizer-ui
   cd query-optimizer-ui
   npm start
   ```

## Requirements

```plaintext
Flask==2.0.2
langchain==0.0.148
elasticsearch==7.17.0
pandas
openai
```

# Structure

```
query_analysis_project/
├── README.md
├── requirements.txt
├── config.py
├── app.py
├── dataset_loader.py
├── elasticsearch_integration.py
└── optimizer/
    ├── __init__.py
    ├── query_analyzer.py
    ├── query_optimizer.py
    └── langchain_utils.py
```

# Fine-tuned Model 1 - [llama-query-expansion-finetuned](https://huggingface.co/Aygun/llama-query-expansion-finetuned) 

## Dataset 1 - [Query Expansion Dataset](https://huggingface.co/datasets/s-emanuilov/query-expansion)

# Fine-tuned Model 2 - [llama-3.2-1B-MLQRECC-Rewriter](https://huggingface.co/Aygun/llama-3.2-1B-MLQRECC-Rewriter)

## Dataset 2 - [ML‑QRECC dataset](https://github.com/apple/ml-qrecc) 
