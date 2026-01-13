import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    genre: '',
    artist: '',
    track: ''
  });
  const [songs, setSongs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Failed to fetch songs');
      }

      const data = await response.json();
      setSongs(data.songs);
    } catch (err) {
      setError('Failed to fetch songs. Make sure the backend is running.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFormData({
      genre: '',
      artist: '',
      track: ''
    });
    setSongs([]);
    setError('');
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Spotify Playlist Recommender</h1>
        
        <form onSubmit={handleSubmit} className="search-form">
          <div className="form-group">
            <label htmlFor="genre">Genre:</label>
            <input
              type="text"
              id="genre"
              name="genre"
              value={formData.genre}
              onChange={handleInputChange}
              placeholder="e.g., pop, rock, jazz"
            />
          </div>

          <div className="form-group">
            <label htmlFor="artist">Artist:</label>
            <input
              type="text"
              id="artist"
              name="artist"
              value={formData.artist}
              onChange={handleInputChange}
              placeholder="e.g., Taylor Swift"
            />
          </div>

          <div className="form-group">
            <label htmlFor="track">Track Name:</label>
            <input
              type="text"
              id="track"
              name="track"
              value={formData.track}
              onChange={handleInputChange}
              placeholder="e.g., Love Song"
            />
          </div>

          <div className="button-group">
            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? 'Searching...' : 'Search Songs'}
            </button>
            <button type="button" onClick={handleClear} className="clear-btn">
              Clear
            </button>
          </div>
        </form>

        {error && <div className="error-message">{error}</div>}

        {songs.length > 0 && (
          <div className="results">
            <h2>Top 10 Recommended Songs</h2>
            <div className="songs-list">
              {songs.map((song, index) => (
                <div key={song.id} className="song-card">
                  <div className="song-number">{index + 1}</div>
                  <div className="song-info">
                    <h3>{song.name}</h3>
                    <p className="artist">{song.artist}</p>
                    <p className="album">{song.album}</p>
                    {song.external_url && song.external_url !== '#' && (
                      <a
                        href={song.external_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="spotify-link"
                      >
                        Open in Spotify
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
