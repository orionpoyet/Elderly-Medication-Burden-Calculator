# external_apis.py
import requests
from typing import Optional, Dict, List
from functools import lru_cache

class RxNormAPI:
    BASE_URL = "https://rxnav.nlm.nih.gov/REST"
    
    @staticmethod
    @lru_cache(maxsize=1000)
    def get_rxcui(drug_name: str) -> Optional[str]:
        """Get RxNorm Concept Unique Identifier for a drug"""
        try:
            url = f"{RxNormAPI.BASE_URL}/rxcui.json?name={requests.utils.quote(drug_name)}&allsrc=1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'idGroup' in data and 'rxnormId' in data['idGroup']:
                    return data['idGroup']['rxnormId'][0]
            
            return None
        except Exception:
            return None
    
    @staticmethod
    @lru_cache(maxsize=500)
    def get_drug_info(rxcui: str) -> Dict:
        """Get comprehensive drug information from RxNorm"""
        try:
            url = f"{RxNormAPI.BASE_URL}/rxcui/{rxcui}/allrelated.json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('allRelatedGroup', {}).get('conceptGroup', [])
            
            return []
        except Exception:
            return {}
    
    @staticmethod
    def normalize_drug_name(drug_name: str) -> str:
        """Try to get the standard name from RxNorm"""
        rxcui = RxNormAPI.get_rxcui(drug_name)
        if rxcui:
            info = RxNormAPI.get_drug_info(rxcui)
            for group in info:
                if group.get('tty') == 'IN':  # Ingredient name (generic)
                    concepts = group.get('conceptProperties', [])
                    if concepts:
                        return concepts[0].get('name', drug_name)
        
        return drug_name
    
    @staticmethod
    def get_drug_classes(rxcui: str) -> List[str]:
        """Get drug classes from RxNorm"""
        try:
            url = f"{RxNormAPI.BASE_URL}/rxcui/{rxcui}/allrelated.json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                classes = []
                for group in data.get('allRelatedGroup', {}).get('conceptGroup', []):
                    tty = group.get('tty', '')
                    if tty in ['SCD', 'SBD', 'SCDC', 'SBDC']:
                        for concept in group.get('conceptProperties', []):
                            classes.append(concept.get('name'))
                return list(set(classes))[:5]
            
            return []
        except:
            return []
    
    @staticmethod
    def check_spelling(drug_name: str) -> Optional[str]:
        """Check for spelling suggestions"""
        try:
            url = f"{RxNormAPI.BASE_URL}/spellingsuggestions.json?name={requests.utils.quote(drug_name)}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                suggestions = data.get('suggestionGroup', {}).get('suggestionList', {}).get('suggestion', [])
                if suggestions:
                    return suggestions[0]
            
            return None
        except:
            return None