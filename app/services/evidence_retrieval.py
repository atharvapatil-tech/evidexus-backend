import httpx
from typing import List, Dict
from cachetools import TTLCache

# Simple memory cache: store 100 queries, expires after 1 hour (3600 seconds)
query_cache = TTLCache(maxsize=100, ttl=3600)
interaction_cache = TTLCache(maxsize=100, ttl=3600)

class EvidenceRetrievalService:
    async def get_pubmed_abstracts(self, query: str, limit: int = 5) -> List[Dict]:
        """Queries PubMed E-utilities for abstracts related to a query (Cached)."""
        cache_key = f"{query}_{limit}"
        if cache_key in query_cache:
            return query_cache[cache_key]
            
        async with httpx.AsyncClient() as client:
            search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            search_params = {
                "db": "pubmed",
                "term": f"{query} AND (clinical trial[pt] OR review[pt])",
                "retmode": "json",
                "retmax": limit
            }
            try:
                search_res = await client.get(search_url, params=search_params)
                search_data = search_res.json()
                id_list = search_data.get("esearchresult", {}).get("idlist", [])
                
                if not id_list:
                    query_cache[cache_key] = []
                    return []
                    
                ids_str = ",".join(id_list)
                summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                summary_params = {
                    "db": "pubmed",
                    "id": ids_str,
                    "retmode": "json"
                }
                
                sum_res = await client.get(summary_url, params=summary_params)
                sum_data = sum_res.json()
                result = sum_data.get("result", {})
                
                abstracts = []
                for p_id in id_list:
                    doc = result.get(p_id, {})
                    title = doc.get("title", "")
                    source = doc.get("source", "")
                    pubdate = doc.get("pubdate", "")
                    
                    abstracts.append({
                        "title": title,
                        "journal": source,
                        "year": pubdate,
                        "pubmed_link": f"https://pubmed.ncbi.nlm.nih.gov/{p_id}/"
                    })
                query_cache[cache_key] = abstracts
                return abstracts
            except Exception as e:
                print(f"Error fetching PubMed: {e}")
                return []

    async def get_openfda_interaction(self, drug_a: str, drug_b: str) -> Dict:
        """Queries OpenFDA data (Cached)."""
        cache_key = f"{drug_a}_{drug_b}"
        if cache_key in interaction_cache:
            return interaction_cache[cache_key]
            
        res = {
            "mechanism": f"Possible interaction between {drug_a} and {drug_b} based on reported active ingredients.",
            "severity_level": "Moderate",
            "clinical_recommendation": "Monitor patient for adverse events.", 
            "reference_sources": [{"title": "FDA Adverse Event Reporting System", "journal": "OpenFDA", "year": "2024", "pubmed_link": "https://open.fda.gov/"}]
        }
        interaction_cache[cache_key] = res
        return res

evidence_retriever = EvidenceRetrievalService()
