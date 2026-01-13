from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import base64

app = Flask(__name__)
CORS(app)

# Spotify API credentials (should be set as environment variables)
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', '')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '')

def get_spotify_token():
    """Get Spotify API access token"""
    if not CLIENT_ID or not CLIENT_SECRET:
        return None
    
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get('access_token')
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def search_songs(query_params):
    """Search for songs using Spotify API"""
    token = get_spotify_token()
    
    if not token:
        # Return mock data if no credentials are set
        return get_mock_songs(query_params)
    
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Build search query
    search_parts = []
    if query_params.get('genre'):
        search_parts.append(f"genre:{query_params['genre']}")
    if query_params.get('artist'):
        search_parts.append(f"artist:{query_params['artist']}")
    if query_params.get('track'):
        search_parts.append(query_params['track'])
    
    q = ' '.join(search_parts) if search_parts else 'popular'
    
    params = {
        'q': q,
        'type': 'track',
        'limit': 10
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        tracks = []
        for item in data.get('tracks', {}).get('items', []):
            track = {
                'id': item['id'],
                'name': item['name'],
                'artist': ', '.join([artist['name'] for artist in item['artists']]),
                'album': item['album']['name'],
                'preview_url': item.get('preview_url'),
                'external_url': item['external_urls'].get('spotify')
            }
            tracks.append(track)
        
        return tracks
    except Exception as e:
        print(f"Error searching songs: {e}")
        return get_mock_songs(query_params)

def get_mock_songs(query_params):
    """Return mock song data for testing"""
    genre = query_params.get('genre', 'pop')
    artist = query_params.get('artist', 'Various')
    
    mock_songs = [
        {
            'id': '1',
            'name': f'Sample Song 1 ({genre})',
            'artist': artist if artist else 'Artist One',
            'album': 'Greatest Hits Vol. 1',
            'preview_url': None,
            'external_url': '#'
        },
        {
            'id': '2',
            'name': f'Sample Song 2 ({genre})',
            'artist': artist if artist else 'Artist Two',
            'album': 'Greatest Hits Vol. 2',
            'preview_url': None,
            'external_url': '#'
        },
        {
            'id': '3',
            'name': f'Sample Song 3 ({genre})',
            'artist': artist if artist else 'Artist Three',
            'album': 'Greatest Hits Vol. 3',
            'preview_url': None,
            'external_url': '#'
        },
        {
            'id': '4',
            'name': f'Sample Song 4 ({genre})',
            'artist': artist if artist else 'Artist Four',
            'album': 'Greatest Hits Vol. 4',
            'preview_url': None,
            'external_url': '#'
        },
        {
            'id': '5',
            'name': f'Sample Song 5 ({genre})',
            'artist': artist if artist else 'Artist Five',
            'album': 'Greatest Hits Vol. 5',
            'preview_url': None,
            'external_url': '#'
        },
        {
            'id': '6',
            'name': f'Sample Song 6 ({genre})',
            'artist': artist if artist else 'Artist Six',
            'album': 'Greatest Hits Vol. 6',
            'preview_url': None,
            'external_url': '#'
        },
        {
            'id': '7',
            'name': f'Sample Song 7 ({genre})',
            'artist': artist if artist else 'Artist Seven',
            'album': 'Greatest Hits Vol. 7',
            'preview_url': None,
            'external_url': '#'
        },
        {
            'id': '8',
            'name': f'Sample Song 8 ({genre})',
            'artist': artist if artist else 'Artist Eight',
            'album': 'Greatest Hits Vol. 8',
            'preview_url': None,
            'external_url': '#'
        },
        {
            'id': '9',
            'name': f'Sample Song 9 ({genre})',
            'artist': artist if artist else 'Artist Nine',
            'album': 'Greatest Hits Vol. 9',
            'preview_url': None,
            'external_url': '#'
        },
        {
            'id': '10',
            'name': f'Sample Song 10 ({genre})',
            'artist': artist if artist else 'Artist Ten',
            'album': 'Greatest Hits Vol. 10',
            'preview_url': None,
            'external_url': '#'
        }
    ]
    
    return mock_songs

@app.route('/api/search', methods=['POST'])
def search():
    """Endpoint to search for songs based on user input"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No search parameters provided'}), 400
    
    query_params = {
        'genre': data.get('genre', ''),
        'artist': data.get('artist', ''),
        'track': data.get('track', '')
    }
    
    songs = search_songs(query_params)
    
    return jsonify({
        'success': True,
        'songs': songs,
        'count': len(songs)
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
