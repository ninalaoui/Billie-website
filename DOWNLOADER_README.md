# 🎵 Billie Eilish Song Downloader

This script downloads audio files for the Billie Eilish playlist website.

## 🚀 Quick Start

### Option 1: Run the batch file (Windows)
```bash
download_songs.bat
```

### Option 2: Manual installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the downloader
python download_songs.py
```

## 📁 What it does

1. **Downloads audio files** from YouTube URLs
2. **Saves them** in the `audio/` folder
3. **Generates** `songs_data.js` with local file paths
4. **Updates** the website to use local audio files

## 🔧 Configuration

Edit `download_songs.py` and update the `SONGS_DATA` array with actual Billie Eilish YouTube URLs:

```python
SONGS_DATA = [
    {
        "id": 1,
        "title": "LUNCH",
        "artist": "Billie Eilish",
        "album": "Hit Me Hard and Soft",
        "duration": "3:30",
        "image": "https://i.pinimg.com/736x/f1/55/1d/f1551d10cd1d18817760f04efc8d8f70.jpg",
        "youtube_url": "https://www.youtube.com/watch?v=ACTUAL_BILLIE_EILISH_URL"  # Replace this!
    },
    # ... more songs
]
```

## 📂 File Structure

After running:
```
Billie-website/
├── audio/                    # Downloaded audio files
│   ├── 01_LUNCH.mp3
│   ├── 02_WILDFLOWER.mp3
│   └── ...
├── songs_data.js            # Generated JavaScript data
├── download_songs.py        # Main script
├── requirements.txt         # Python dependencies
└── download_songs.bat       # Windows batch file
```

## 🎯 Next Steps

1. **Update YouTube URLs** in `download_songs.py` with real Billie Eilish song URLs
2. **Run the script** to download audio files
3. **Copy the content** from `songs_data.js` into `songs.html`
4. **Test the playlist** - songs should now play!

## ⚠️ Important Notes

- **Replace the placeholder YouTube URLs** with actual Billie Eilish song URLs
- **Audio quality** is set to 192K MP3
- **Files are named** with ID and sanitized title
- **Script skips** already downloaded files

## 🛠️ Troubleshooting

### "yt-dlp not found"
```bash
pip install yt-dlp
```

### "Permission denied"
Make sure you have write permissions in the project folder.

### "Download failed"
Check that the YouTube URLs are valid and accessible.

## 📝 Legal Notice

This script is for educational purposes only. Make sure you have the right to download and use the audio content.
