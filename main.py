"""
Main module - Entry point for Just-Quran Reel Generator
"""

import logging
import sys
from quran_api import QuranAPI
from video_generator import VideoGenerator
from audio_processor import AudioProcessor
from config import OUTPUT_DIR, RECITER_ID

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QuranReelGenerator:
    def __init__(self):
        self.api = QuranAPI()
        self.video_gen = VideoGenerator()
        self.audio_proc = AudioProcessor()
    
    def create_reel(self, surah: int, ayah: int, language: str = "en", 
                   theme: str = "dark", add_audio: bool = True) -> str:
        """
        Create a complete Quran reel
        
        Args:
            surah: Surah number (1-114)
            ayah: Ayah number
            language: Translation language
            theme: Visual theme (dark, light, gradient)
            add_audio: Whether to include audio recitation
            
        Returns:
            Path to generated video file
        """
        try:
            logger.info(f"Starting reel generation for Surah {surah}, Ayah {ayah}")
            
            # Fetch verse data
            verse_data = self.api.get_verse(surah, ayah, language)
            logger.info("Verse data fetched successfully")
            
            # Create video
            output_filename = f"reel_surah_{surah}_ayah_{ayah}.mp4"
            video_path = self.video_gen.create_video(verse_data, output_filename, theme)
            logger.info(f"Video created: {video_path}")
            
            # Add audio if requested
            if add_audio:
                try:
                    audio_url = self.api.get_audio_url(surah, ayah, RECITER_ID)
                    if audio_url:
                        audio_path = self.audio_proc.download_audio(audio_url, f"{surah}-{ayah}")
                        final_output = f"{OUTPUT_DIR}/reel_surah_{surah}_ayah_{ayah}_final.mp4"
                        self.audio_proc.merge_audio_video(video_path, audio_path, final_output)
                        logger.info(f"Final reel with audio: {final_output}")
                        return final_output
                except Exception as e:
                    logger.warning(f"Could not add audio: {str(e)}, returning video only")
            
            return video_path
        
        except Exception as e:
            logger.error(f"Error creating reel: {str(e)}")
            raise
    
    def batch_create_reels(self, verses: list, language: str = "en", theme: str = "dark"):
        """
        Create multiple reels in batch
        
        Args:
            verses: List of (surah, ayah) tuples
            language: Translation language
            theme: Visual theme
        """
        for surah, ayah in verses:
            try:
                self.create_reel(surah, ayah, language, theme)
            except Exception as e:
                logger.error(f"Failed to create reel for {surah}:{ayah} - {str(e)}")


if __name__ == "__main__":
    logger.info("Just-Quran Reel Generator Started")
    
    try:
        generator = QuranReelGenerator()
        
        # Example: Create a single reel
        # Surah Al-Fatiha (1), Ayah 1
        reel_path = generator.create_reel(
            surah=1,
            ayah=1,
            language="en",
            theme="dark",
            add_audio=True
        )
        
        logger.info(f"Reel generated successfully: {reel_path}")
        
        # Example: Create batch of reels
        # verses = [(1, 1), (2, 1), (36, 1)]
        # generator.batch_create_reels(verses, language="en", theme="dark")
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)
