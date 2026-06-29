"""
Quran API Module - Handles all API calls to Al-Quran Cloud API
"""

import requests
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class QuranAPI:
    def __init__(self, base_url: str = "https://api.alquran.cloud/v1"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_verse(self, surah: int, ayah: int, language: str = "en") -> Dict:
        """
        Fetch a specific verse from Quran
        
        Args:
            surah: Chapter number (1-114)
            ayah: Verse number
            language: Language code (en, ar, etc.)
            
        Returns:
            Dictionary containing verse data
        """
        try:
            # Get Arabic text
            url = f"{self.base_url}/ayah/{surah}:{ayah}"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()["data"]
            
            # Get translation if language specified
            if language != "ar":
                trans_url = f"{self.base_url}/ayah/{surah}:{ayah}/editions/{language}"
                trans_response = self.session.get(trans_url)
                if trans_response.status_code == 200:
                    trans_data = trans_response.json()["data"]
                    if trans_data:
                        data["translation"] = trans_data[0]["text"]
            
            logger.info(f"Fetched verse {surah}:{ayah}")
            return data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching verse {surah}:{ayah}: {str(e)}")
            raise
    
    def get_surah_info(self, surah: int) -> Dict:
        """
        Get information about a specific Surah
        
        Args:
            surah: Chapter number (1-114)
            
        Returns:
            Dictionary containing Surah information
        """
        try:
            url = f"{self.base_url}/surah/{surah}"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()["data"]
            logger.info(f"Fetched Surah {surah} info")
            return data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Surah {surah} info: {str(e)}")
            raise
    
    def get_audio_url(self, surah: int, ayah: int, reciter: str = "ar.alafasy") -> str:
        """
        Get audio URL for a specific verse
        
        Args:
            surah: Chapter number
            ayah: Verse number
            reciter: Reciter identifier
            
        Returns:
            URL to audio file
        """
        try:
            url = f"{self.base_url}/ayah/{surah}:{ayah}/editions/{reciter}"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()["data"]
            
            if data and len(data) > 0:
                audio_url = data[0].get("audio")
                if audio_url:
                    logger.info(f"Got audio URL for {surah}:{ayah}")
                    return audio_url
            
            logger.warning(f"No audio found for {surah}:{ayah}")
            return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching audio for {surah}:{ayah}: {str(e)}")
            raise
    
    def search_verses(self, query: str, language: str = "en") -> List[Dict]:
        """
        Search for verses containing specific text
        
        Args:
            query: Search query
            language: Language code
            
        Returns:
            List of matching verses
        """
        try:
            url = f"{self.base_url}/search/{query}/{language}"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()["data"]["matches"]
            logger.info(f"Found {len(data)} verses matching '{query}'")
            return data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching verses: {str(e)}")
            raise
