"""
Video Generator Module - Creates Quran reel videos
"""

import cv2
import numpy as np
import logging
from PIL import Image, ImageDraw, ImageFont
import os
from typing import Dict, Optional
from config import (
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, VIDEO_DURATION,
    FONT_SIZE, FONT_COLOR, BACKGROUND_COLOR, THEMES,
    OUTPUT_DIR, VIDEO_FORMAT
)

logger = logging.getLogger(__name__)

class VideoGenerator:
    def __init__(self, width: int = VIDEO_WIDTH, height: int = VIDEO_HEIGHT, fps: int = VIDEO_FPS):
        self.width = width
        self.height = height
        self.fps = fps
        self.total_frames = int(VIDEO_DURATION * fps)
        
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
    
    def create_frame(self, verse_text: str, translation: Optional[str] = None, 
                    surah_info: str = "", theme: str = "dark") -> np.ndarray:
        """
        Create a single frame with text overlay
        
        Args:
            verse_text: Arabic verse text
            translation: English translation
            surah_info: Surah and Ayah info
            theme: Visual theme (dark, light, gradient)
            
        Returns:
            NumPy array representing the frame
        """
        # Create PIL image
        img = Image.new('RGB', (self.width, self.height), THEMES[theme]["bg_color"])
        draw = ImageDraw.Draw(img)
        
        try:
            # Try to load a nice font, fallback to default
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        # Add Surah and Ayah info at top
        draw.text((50, 100), surah_info, fill=THEMES[theme]["accent_color"], font=small_font)
        
        # Add main verse text (centered)
        y_position = 400
        self._draw_wrapped_text(draw, verse_text, font, y_position, 
                               THEMES[theme]["text_color"], self.width - 100)
        
        # Add translation if provided
        if translation:
            trans_y = y_position + 300
            self._draw_wrapped_text(draw, translation, small_font, trans_y,
                                   THEMES[theme]["text_color"], self.width - 100)
        
        # Convert to numpy array
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return frame
    
    def _draw_wrapped_text(self, draw, text: str, font, y_position: int, 
                          color: tuple, max_width: int):
        """
        Draw text with word wrapping
        
        Args:
            draw: PIL ImageDraw object
            text: Text to draw
            font: Font object
            y_position: Y coordinate to start
            color: Text color (RGB)
            max_width: Maximum width for wrapping
        """
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines
        line_spacing = 80
        for i, line in enumerate(lines):
            draw.text((50, y_position + i * line_spacing), line, fill=color, font=font)
    
    def create_video(self, verse_data: Dict, output_filename: str, theme: str = "dark") -> str:
        """
        Create a complete video file
        
        Args:
            verse_data: Dictionary containing verse information
            output_filename: Name of output video file
            theme: Visual theme to use
            
        Returns:
            Path to created video file
        """
        try:
            # Setup video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
            
            # Prepare text
            verse_text = verse_data.get("text", "")
            translation = verse_data.get("translation", "")
            surah_info = f"Surah {verse_data.get('surah', {}).get('number', '')} : Ayah {verse_data.get('numberInSurah', '')}"
            
            # Create frame
            frame = self.create_frame(verse_text, translation, surah_info, theme)
            
            # Write frame multiple times to create video duration
            for _ in range(self.total_frames):
                out.write(frame)
            
            out.release()
            logger.info(f"Video created: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error creating video: {str(e)}")
            raise
