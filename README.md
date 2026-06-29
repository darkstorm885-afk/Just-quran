# Just-Quran

A Python-based tool that generates beautiful Quran reels and short-form video content automatically.

## Features

- 🕌 Fetch Quran verses from Al-Quran Cloud API
- 🎬 Generate MP4 video files with verse overlays
- 🔊 Add Quran recitations (audio)
- 📝 Create text overlays with translations
- 🎨 Customize video styling and themes
- 📤 Ready for social media posting (TikTok, Instagram, YouTube Shorts)

## Installation

```bash
git clone https://github.com/darkstorm885-afk/Just-quran.git
cd Just-quran
pip install -r requirements.txt
```

## Quick Start

```python
from just_quran import QuranReelGenerator

generator = QuranReelGenerator()
video = generator.create_reel(
    surah=1,
    ayah=1,
    language="en",
    theme="dark"
)
video.save("output/reel.mp4")
```

## Configuration

Edit `config.py` to customize:
- Video resolution and frame rate
- Font styles and colors
- Background effects
- Audio settings

## Requirements

- Python 3.8+
- FFmpeg
- OpenCV
- PIL/Pillow

## License

MIT

## Author

Created by darkstorm885-afk
