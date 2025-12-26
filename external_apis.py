# external_apis.py
# Wrapper for external API calls (RxNorm, etc.)

import requests
from typing import Optional, List, Dict

class RxNormAPI:
    """Wrapper for RxNorm API calls"""
    
    BASE_URL = "https://rxnav.nlm.nih.gov/REST"
    
    @staticmethod
    def get_rxcui(drug_name: str) -> Optional[str]:
        """
        Get RxCUI (RxNorm Concept Unique Identifier) for a drug name
        
        Args:
            drug_name: Name of the drug (brand or generic)
            
        Returns:
            RxCUI string if found, None otherwise
        """
        try:
            url = f"{RxNormAPI.BASE_URL}/rxcui.json"
            params = {"name": drug_name}
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            rxcui_list = data.get("idGroup", {}).get("rxnormId", [])
            
            return rxcui_list[0] if rxcui_list else None
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting RxCUI for {drug_name}: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"Error parsing RxCUI response for {drug_name}: {e}")
            return None
    
    @staticmethod
    def get_drug_info(rxcui: str) -> List[Dict]:
        """
        Get drug information for a given RxCUI
        
        Args:
            rxcui: RxNorm Concept Unique Identifier
            
        Returns:
            List of drug information dictionaries
        """
        try:
            url = f"{RxNormAPI.BASE_URL}/rxcui/{rxcui}/allrelated.json"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            concepts = data.get("allRelatedGroup", {}).get("conceptGroup", [])
            
            return concepts
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting drug info for RxCUI {rxcui}: {e}")
            return []
        except (KeyError, IndexError) as e:
            print(f"Error parsing drug info for RxCUI {rxcui}: {e}")
            return []
    
    @staticmethod
    def get_spelling_suggestions(query: str, max_results: int = 10) -> List[str]:
        """
        Get spelling suggestions for a drug name query
        
        Args:
            query: Partial or misspelled drug name
            max_results: Maximum number of suggestions to return
            
        Returns:
            List of suggested drug names
        """
        try:
            url = f"{RxNormAPI.BASE_URL}/spellingsuggestions.json"
            params = {"name": query}
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            suggestions = data.get("suggestionGroup", {}).get("suggestionList", {}).get("suggestion", [])
            
            return suggestions[:max_results]
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting spelling suggestions for {query}: {e}")
            return []
        except (KeyError, IndexError) as e:
            print(f"Error parsing spelling suggestions for {query}: {e}")
            return []
    
    @staticmethod
    def search_approximate(query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Approximate search for drug names
        
        Args:
            query: Search term
            max_results: Maximum number of results
            
        Returns:
            List of dictionaries with 'name' and 'rxcui' keys
        """
        try:
            url = f"{RxNormAPI.BASE_URL}/approximateTerm.json"
            params = {
                "term": query,
                "maxEntries": max_results
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            candidates = data.get("approximateGroup", {}).get("candidate", [])
            
            results = []
            for candidate in candidates:
                results.append({
                    "name": candidate.get("name", ""),
                    "rxcui": candidate.get("rxcui", ""),
                    "rank": candidate.get("rank", 0)
                })
            
            # Sort by rank (lower is better)
            results.sort(key=lambda x: x.get("rank", 999))
            
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"Error in approximate search for {query}: {e}")
            return []
        except (KeyError, IndexError) as e:
            print(f"Error parsing approximate search results for {query}: {e}")
            return []


# Example usage and testing
if __name__ == "__main__":
    # Test RxCUI lookup
    print("Testing RxNorm API...")
    
    test_drugs = ["warfarin", "lipitor", "aspirin"]
    
    for drug in test_drugs:
        print(f"\nDrug: {drug}")
        rxcui = RxNormAPI.get_rxcui(drug)
        print(f"  RxCUI: {rxcui}")
        
        if rxcui:
            info = RxNormAPI.get_drug_info(rxcui)
            print(f"  Info groups: {len(info)}")
    
    # Test spelling suggestions
    print("\n\nTesting spelling suggestions for 'warfrin'...")
    suggestions = RxNormAPI.get_spelling_suggestions("warfrin")
    print(f"  Suggestions: {suggestions}")
    
    # Test approximate search
    print("\n\nTesting approximate search for 'liptor'...")
    results = RxNormAPI.search_approximate("liptor")
    for result in results[:5]:
        print(f"  - {result['name']} (RxCUI: {result['rxcui']}, Rank: {result['rank']})")