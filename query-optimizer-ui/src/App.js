import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [optimizedQuery, setOptimizedQuery] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setOptimizedQuery('');
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/optimize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query })
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setOptimizedQuery(data.optimized_query);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Query Optimizer</h1>
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            value={query} 
            onChange={(e) => setQuery(e.target.value)} 
            placeholder="Enter your query" 
          />
          <button type="submit">Optimize</button>
        </form>
        {error && <p style={{ color: 'red' }}>Error: {error}</p>}
        {optimizedQuery && (
          <div>
            <h2>Optimized Query:</h2>
            <p>{optimizedQuery}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
