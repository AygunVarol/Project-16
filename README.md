# Project-16

## ![DALL·E 2025-03-12 09 22 36 - A cartoon-style duck dressed as a PhD graduate  The duck wears a black academic gown, a mortarboard cap with a tassel, and round glasses  It holds a d - Kopya](https://github.com/user-attachments/assets/2e35cf31-4e02-4e33-8fe4-c80e519a09a2) Team 23: Ducktor 




## Members: Fujia Yu, Aygün Varol

# Query Analysis of Large Language Models Using LangChain for Multimedia Application

## Overview
This project aims to optimize poorly structured user queries by analyzing and rewriting them using advanced techniques inspired by LangChain and visual reasoning research (e.g., “Rethinking Step-by-step Visual Reasoning in LLMs”). The optimized queries are then indexed in ElasticSearch for improved search performance. A user interface (to be developed in React.js) will allow users to enter queries and receive optimized versions.

# Workflow
![Başlıksız Diyagram](https://github.com/user-attachments/assets/faa079a4-6f68-4aa5-b681-0fe96fc96299)

# User Interface
![resim](https://github.com/user-attachments/assets/0d120919-60fd-482a-a481-b05cef2765e5)

## How to Start
1. **Collect Dataset:**  
   Collect a dataset of user queries (e.g., Google Search Query Dataset). Use the provided `dataset_loader.py` script to ingest your data.

2. **Analyze Query Inefficiencies:**  
   Identify common issues in user queries—such as ambiguity, brevity, or missing keywords. The module `optimizer/query_analyzer.py` provides basic analysis logic.

3. **Optimize Query Structures:**  
   Use LangChain to reformat and optimize the queries for better AI comprehension. The module `optimizer/langchain_utils.py` contains functions to interface with your LLM (or a placeholder transformation) for query optimization.

4. **Query Reformulation System:**  
   Develop an AI-powered system that leverages the analysis and optimization modules to improve search intent recognition.

5. **ElasticSearch Integration:**  
   Integrate with ElasticSearch (via `elasticsearch_integration.py`) to index and test the performance of the optimized queries.

6. **User Interface (React.js):**  
   Build a user interface where users can input queries and receive optimized versions. The Flask backend is designed to be easily integrated with a React.js frontend.

## Application Components
- **Backend API:** Python-based API built with Flask.
- **Query Analysis & Optimization:** Combines inefficiency analysis (in `optimizer/query_analyzer.py`) and query reformulation using LangChain utilities.
- **Search Indexing:** ElasticSearch integration for storing and testing query performance.
- **Frontend:** Planned React.js interface (not included in this repository).

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

