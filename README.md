# Spotify Playlist Recommender

A simple web application to recommend Spotify songs based on user preferences. Built with React for the frontend and Flask for the backend.

## Features

- Search for songs by genre, artist, and track name
- Display top 10 song recommendations
- Clear and resubmit search functionality
- Responsive design
- Mock data support when Spotify credentials are not configured

## Project Structure

```
spotify-agent/
├── backend/          # Flask API
│   ├── app.py       # Main Flask application
│   └── requirements.txt
├── frontend/        # React application
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   └── package.json
└── README.md
```

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set Spotify API credentials as environment variables:
   ```bash
   export SPOTIFY_CLIENT_ID=your_client_id
   export SPOTIFY_CLIENT_SECRET=your_client_secret
   ```
   
   Note: If credentials are not set, the app will use mock data.

4. (Optional) Enable debug mode for development:
   ```bash
   export FLASK_DEBUG=True
   ```
   
   Note: Debug mode is disabled by default for security. Only enable for development.

5. Run the Flask server:
   ```bash
   python app.py
   ```

   The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

   The frontend will open automatically at `http://localhost:3000`

## Usage

1. Start both the backend (Flask) and frontend (React) servers
2. Open your browser to `http://localhost:3000`
3. Fill in the search form with:
   - Genre (e.g., pop, rock, jazz)
   - Artist name (e.g., Taylor Swift)
   - Track name (e.g., Love Song)
4. Click "Search Songs" to get recommendations
5. View the top 10 recommended songs
6. Click "Clear" to reset the form and search again

## API Endpoints

### POST /api/search
Search for songs based on user input.

**Request Body:**
```json
{
  "genre": "pop",
  "artist": "Taylor Swift",
  "track": "Love"
}
```

**Response:**
```json
{
  "success": true,
  "songs": [
    {
      "id": "123",
      "name": "Song Name",
      "artist": "Artist Name",
      "album": "Album Name",
      "preview_url": "url",
      "external_url": "spotify_url"
    }
  ],
  "count": 10
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Getting Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Create a new app
4. Copy the Client ID and Client Secret
5. Set them as environment variables before running the backend

## Technologies Used

- **Frontend**: React, CSS3
- **Backend**: Flask, Flask-CORS
- **API**: Spotify Web API
- **HTTP Client**: Requests (Python), Fetch API (JavaScript)

## License

MIT
