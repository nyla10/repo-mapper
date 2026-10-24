
import { useState } from 'react';
import { cloneRepository } from './services/api';
import './App.css';

function App() {
  const [repoUrl, setRepoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!repoUrl.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await cloneRepository(repoUrl);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>RepoMapper Visualizer</h1>
      <p>Enter a public GitHub repository URL to scan and map its structure.</p>

      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="https://github.com/username/repository"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          style={{ flex: 1, padding: '10px', fontSize: '16px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
        <button 
          type="submit" 
          disabled={loading}
          style={{ padding: '10px 20px', fontSize: '16px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          {loading ? 'Cloning...' : 'Map Repo'}
        </button>
      </form>

      {error && (
        <div style={{ padding: '15px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '20px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div style={{ padding: '20px', backgroundColor: '#e2f0d9', borderRadius: '4px' }}>
          <h3>Successfully Scanned!</h3>
          <p><strong>Total Files Found:</strong> {result.total_files}</p>
          <h4>File Preview (First 50):</h4>
          <ul style={{ maxHeight: '300px', overflowY: 'auto', backgroundColor: '#fff', padding: '15px', borderRadius: '4px' }}>
            {result.files.map((file, index) => (
              <li key={index} style={{ fontSize: '14px', fontFamily: 'monospace' }}>{file}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;