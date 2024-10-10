find . -type f \( -name "*.session" -o -name "*.pyc" -o -name "*.session-journal" -o -name "*.MP4" -o -name "*.pdf" -o -name "*.mp4" -o -name "*.aria2" -o -name "*.part" \) -delete
find . -type f \( -name "*.MP4" -o -name "*.pdf" -o -name "*.mp4" -o -name "*.aria2" -o -name "*.part" \) -delete
find . -type d \( -name "__pycache__" -o -name "downloads" \) -exec rm -rf {} +