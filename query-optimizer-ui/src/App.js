import React, { useState, useCallback } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [optimizedQuery, setOptimizedQuery] = useState('');
  const [selectedModel, setSelectedModel] = useState('deepseek');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const endpoints = {
    rewriter: "http://localhost:8000/rewriter",
    expander: "http://localhost:8000/expander",
    deepseek: "http://localhost:8000/deepseek"
  };

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a query before submitting.');
      return;
    }

    setOptimizedQuery('');
    setError(null);
    setIsLoading(true);

    try {
      const response = await fetch(endpoints[selectedModel], {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query.trim() })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.optimized_query) {
        throw new Error('No optimized query received from the server.');
      }

      setOptimizedQuery(data.optimized_query);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred. Please try again.');
      console.error('Optimization error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [query, selectedModel, endpoints]);

  const handleQueryChange = (e) => {
    const sanitizedQuery = e.target.value.replace(/[<>]/g, '');
    setQuery(sanitizedQuery);
  };

  const handleModelChange = (e) => {
    setSelectedModel(e.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Query Optimizer</h1>
        <p>Choose your model and optimize your query for the best results!</p>
        <form onSubmit={handleSubmit} className="form-container">
          <div className="form-group">
            <label htmlFor="modelSelect">Select Model:</label>
            <select
              id="modelSelect"
              value={selectedModel}
              onChange={handleModelChange}
              className="model-select"
            >
              <option value="rewriter">ML-QRECC Rewriter</option>
              <option value="expander">Query Expander</option>
              <option value="deepseek">DeepSeek</option>
            </select>
          </div>
          <div className="form-group">
            <input
              type="text"
              value={query}
              onChange={handleQueryChange}
              placeholder="Enter your query here..."
              className="query-input"
              maxLength={200}
            />
          </div>
          <button 
            type="submit" 
            className="submit-btn" 
            disabled={isLoading || !query.trim()}
          >
            {isLoading ? "Optimizing..." : "Optimize"}
          </button>
        </form>
        
        {error && <p className="error">{error}</p>}
        
        {optimizedQuery && (
          <div className="result">
            <h2>Optimized Query:</h2>
            <div className="optimized-query-content">
              {optimizedQuery.split('\n').map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;