"""
Audio Processor Module - Handles audio download and processing
"""

import requests
import logging
import os
from pathlib import Path
from config import OUTPUT_DIR

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self):
        self.audio_dir = os.path.join(OUTPUT_DIR, "audio")
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)
    
    def download_audio(self, audio_url: str, verse_identifier: str) -> str:
        """
        Download audio from URL
        
        Args:
            audio_url: URL to audio file
            verse_identifier: Identifier for the verse (e.g., "1-1")
            
        Returns:
            Path to downloaded audio file
        """
        try:
            filename = f"ayah_{verse_identifier}.mp3"
            filepath = os.path.join(self.audio_dir, filename)
            
            # Don't re-download if exists
            if os.path.exists(filepath):
                logger.info(f"Audio already exists: {filepath}")
                return filepath
            
            response = requests.get(audio_url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Downloaded audio to: {filepath}")
            return filepath
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading audio: {str(e)}")
            raise
    
    def merge_audio_video(self, video_path: str, audio_path: str, output_path: str):
        """
        Merge audio with video using ffmpeg
        
        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_path: Path for output video with audio
        """
        import subprocess
        
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                output_path,
                '-y'  # Overwrite output file
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Audio merged with video: {output_path}")
        
        except subprocess.CalledProcessError as e:
            logger.error(f"Error merging audio with video: {str(e)}")
            raise
