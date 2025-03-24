import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [caption, setCaption] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setCaption('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('image', selectedFile);

    setLoading(true);
    try {
      const response = await axios.post('https://your-backend-url.vercel.app/generate_caption', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setCaption(response.data.caption);
    } catch (error) {
      console.error('Error generating caption:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Image Caption Generator</h1>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} />
          <button type="submit" disabled={!selectedFile || loading}>
            {loading ? 'Generating...' : 'Generate Caption'}
          </button>
        </form>
        {selectedFile && (
          <div className="image-preview">
            <img src={URL.createObjectURL(selectedFile)} alt="Selected" />
          </div>
        )}
        {caption && (
          <div className="caption-result">
            <h2>Generated Caption:</h2>
            <p>{caption}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
