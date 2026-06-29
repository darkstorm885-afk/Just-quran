# Configuration for Just-Quran Reel Generator

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # Portrait format for mobile/social media
VIDEO_FPS = 30
VIDEO_DURATION = 15  # seconds
VIDEO_CODEC = 'mp4v'

# API Settings
QURAN_API_BASE = "https://api.alquran.cloud/v1"
RECITER_ID = "ar.alafasy"  # Default reciter

# Text Settings
FONT_SIZE = 60
FONT_COLOR = (255, 255, 255)  # White
FONT_PATH = "./fonts/Arial.ttf"  # Update with actual font path
TRANSLATION_FONT_SIZE = 40

# Background Settings
BACKGROUND_COLOR = (0, 0, 0)  # Black
THEMES = {
    "dark": {
        "bg_color": (0, 0, 0),
        "text_color": (255, 255, 255),
        "accent_color": (0, 150, 136)
    },
    "light": {
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "accent_color": (0, 150, 136)
    },
    "gradient": {
        "bg_color": (25, 25, 112),  # Midnight blue
        "text_color": (255, 255, 255),
        "accent_color": (255, 215, 0)  # Gold
    }
}

# Output Settings
OUTPUT_DIR = "./output"
VIDEO_FORMAT = "mp4"

# Audio Settings
AUDIO_VOLUME = 0.8
AUDIO_FADE_IN = 1  # seconds
AUDIO_FADE_OUT = 1  # seconds

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "just_quran.log"
