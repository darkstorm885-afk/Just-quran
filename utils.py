"""
Utility functions for Just-Quran
"""

import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def setup_logging(log_file: str = "just_quran.log", level: str = "INFO"):
    """
    Setup logging configuration
    
    Args:
        log_file: Path to log file
        level: Logging level
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger.info(f"Logging initialized. Level: {level}")

def validate_surah_ayah(surah: int, ayah: int) -> bool:
    """
    Validate Surah and Ayah numbers
    
    Args:
        surah: Surah number
        ayah: Ayah number
        
    Returns:
        True if valid, False otherwise
    """
    if surah < 1 or surah > 114:
        logger.error(f"Invalid Surah number: {surah}. Must be between 1-114")
        return False
    
    if ayah < 1:
        logger.error(f"Invalid Ayah number: {ayah}. Must be at least 1")
        return False
    
    return True

def get_timestamp_filename(prefix: str = "reel", extension: str = "mp4") -> str:
    """
    Generate timestamped filename
    
    Args:
        prefix: Filename prefix
        extension: File extension
        
    Returns:
        Timestamped filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def create_directory(path: str):
    """
    Create directory if it doesn't exist
    
    Args:
        path: Directory path
    """
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Created directory: {path}")
