import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [caption, setCaption] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('/generate_caption', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setCaption(response.data.caption);
    } catch (error) {
      console.error('Error generating caption:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Image Caption Generator</h1>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} />
          <button type="submit">Generate Caption</button>
        </form>
        {caption && (
          <div>
            <h2>Generated Caption:</h2>
            <p>{caption}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
