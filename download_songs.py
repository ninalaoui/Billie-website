#!/usr/bin/env python3
"""
Billie Eilish Song Downloader
Downloads audio files for the playlist and updates the website
"""

import os
import requests
import json
from pathlib import Path
import yt_dlp
import re

# Create audio directory
AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

# Song data with YouTube URLs (you can update these with actual Billie Eilish song URLs)
SONGS_DATA = [
    {
        "id": 1,
        "title": "LUNCH",
        "artist": "Billie Eilish",
        "album": "Hit Me Hard and Soft",
        "duration": "3:30",
        "image": "https://i.pinimg.com/736x/f1/55/1d/f1551d10cd1d18817760f04efc8d8f70.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with actual Billie Eilish song URLs
    },
    {
        "id": 2,
        "title": "WILDFLOWER",
        "artist": "Billie Eilish", 
        "album": "Hit Me Hard and Soft",
        "duration": "3:40",
        "image": "https://i.pinimg.com/736x/f1/55/1d/f1551d10cd1d18817760f04efc8d8f70.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    {
        "id": 3,
        "title": "BIRDS OF A FEATHER",
        "artist": "Billie Eilish",
        "album": "Hit Me Hard and Soft", 
        "duration": "3:27",
        "image": "https://i.pinimg.com/736x/f1/55/1d/f1551d10cd1d18817760f04efc8d8f70.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    {
        "id": 4,
        "title": "CHIHIRO",
        "artist": "Billie Eilish",
        "album": "Hit Me Hard and Soft",
        "duration": "3:44", 
        "image": "https://i.pinimg.com/736x/f1/55/1d/f1551d10cd1d18817760f04efc8d8f70.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    {
        "id": 5,
        "title": "L'AMOUR DE MA VIE",
        "artist": "Billie Eilish",
        "album": "Hit Me Hard and Soft",
        "duration": "3:42",
        "image": "https://i.pinimg.com/736x/f1/55/1d/f1551d10cd1d18817760f04efc8d8f70.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    {
        "id": 6,
        "title": "THE GREATEST",
        "artist": "Billie Eilish",
        "album": "Hit Me Hard and Soft",
        "duration": "3:46",
        "image": "https://i.pinimg.com/736x/f1/55/1d/f1551d10cd1d18817760f04efc8d8f70.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    {
        "id": 7,
        "title": "MY STRANGE ADDICTION",
        "artist": "Billie Eilish",
        "album": "When We All Fall Asleep",
        "duration": "3:00",
        "image": "https://i.pinimg.com/1200x/44/a2/0d/44a20d676e22c932d1d18b28924093b7.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    {
        "id": 8,
        "title": "EVERYTHING I WANTED",
        "artist": "Billie Eilish",
        "album": "Single",
        "duration": "4:05",
        "image": "https://i.pinimg.com/736x/40/d9/39/40d9394551378af2f6f75ab6e656434a.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    {
        "id": 9,
        "title": "OCEAN EYES",
        "artist": "Billie Eilish",
        "album": "Don't Smile at Me",
        "duration": "3:20",
        "image": "https://i.pinimg.com/736x/96/bf/96/96bf964dc2cd6ce3e45dba35b6db6688.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    {
        "id": 10,
        "title": "LOVELY",
        "artist": "Billie Eilish",
        "album": "Don't Smile at Me",
        "duration": "3:20",
        "image": "https://i.pinimg.com/736x/63/e4/6f/63e46fe38c7b115bc9be2f2dc3194587.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    {
        "id": 11,
        "title": "HAPPIER THAN EVER",
        "artist": "Billie Eilish",
        "album": "Happier Than Ever",
        "duration": "4:58",
        "image": "https://i.pinimg.com/736x/0b/a8/a4/0ba8a46bb68cfb2a47ac042cfdcac447.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    {
        "id": 12,
        "title": "GUESS",
        "artist": "Billie Eilish",
        "album": "Hit Me Hard and Soft",
        "duration": "3:33",
        "image": "https://i.pinimg.com/736x/c7/01/44/c70144a86faf698a87a442f68dff8699.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
]

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_audio(song_data):
    """Download audio for a single song"""
    title = sanitize_filename(song_data['title'])
    filename = f"{song_data['id']:02d}_{title}.mp3"
    filepath = AUDIO_DIR / filename
    
    # Skip if file already exists
    if filepath.exists():
        print(f"{song_data['title']} already exists")
        return str(filepath)
    
    print(f"Downloading {song_data['title']}...")
    
    # yt-dlp options for audio only
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(filepath),
        'extractaudio': True,
        'audioformat': 'mp3',
        'audioquality': '192K',
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song_data['youtube_url']])
        print(f"Downloaded {song_data['title']}")
        return str(filepath)
    except Exception as e:
        print(f"Failed to download {song_data['title']}: {e}")
        return None

def update_songs_data(songs_data):
    """Update songs data with local file paths"""
    updated_songs = []
    
    for song in songs_data:
        title = sanitize_filename(song['title'])
        filename = f"{song['id']:02d}_{title}.mp3"
        filepath = AUDIO_DIR / filename
        
        # Update the song data with local path
        updated_song = song.copy()
        if filepath.exists():
            updated_song['audioUrl'] = f"audio/{filename}"
        else:
            updated_song['audioUrl'] = "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav"  # Fallback
        
        updated_songs.append(updated_song)
    
    return updated_songs

def generate_js_songs_data(songs_data):
    """Generate JavaScript songs array for the website"""
    js_content = "const songs = [\n"
    
    for i, song in enumerate(songs_data):
        js_content += "  {\n"
        js_content += f"    id: {song['id']},\n"
        js_content += f"    title: \"{song['title']}\",\n"
        js_content += f"    artist: \"{song['artist']}\",\n"
        js_content += f"    album: \"{song['album']}\",\n"
        js_content += f"    duration: \"{song['duration']}\",\n"
        js_content += f"    image: \"{song['image']}\",\n"
        js_content += f"    audioUrl: \"{song['audioUrl']}\"\n"
        js_content += "  }"
        
        if i < len(songs_data) - 1:
            js_content += ","
        js_content += "\n"
    
    js_content += "];"
    return js_content

def main():
    """Main function"""
    print("Billie Eilish Song Downloader")
    print("=" * 40)
    
    # Download all songs
    downloaded_files = []
    for song in SONGS_DATA:
        filepath = download_audio(song)
        if filepath:
            downloaded_files.append(filepath)
    
    print(f"\nDownload Summary:")
    print(f"Successfully downloaded: {len(downloaded_files)} songs")
    print(f"Failed downloads: {len(SONGS_DATA) - len(downloaded_files)} songs")
    
    # Update songs data with local paths
    updated_songs = update_songs_data(SONGS_DATA)
    
    # Generate JavaScript for the website
    js_content = generate_js_songs_data(updated_songs)
    
    # Save to file
    with open("songs_data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    
    print(f"\nGenerated songs_data.js with local file paths")
    print(f"Audio files saved in: {AUDIO_DIR.absolute()}")
    
    print(f"\nNext steps:")
    print(f"1. Replace the songs array in songs.html with the content from songs_data.js")
    print(f"2. Make sure the audio folder is accessible by your web server")
    print(f"3. Test the playlist!")

if __name__ == "__main__":
    main()
