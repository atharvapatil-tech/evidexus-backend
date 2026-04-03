import json
import logging
from openai import AsyncOpenAI
from app.core.config import settings
from app.services.evidence_retrieval import evidence_retriever

logger = logging.getLogger(__name__)

class AIReasoningService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def classify_intent(self, query: str) -> str:
        """Classify incoming query into 5 supported intents via GPT-4"""
        if not settings.OPENAI_API_KEY:
            # Fallback
            if "search" in query.lower() or "find" in query.lower():
                return "literature_search"
            elif "interact" in query.lower():
                return "drug_interaction"
            return "clinical_qa"

        system_prompt = (
            "You are a medical router. Classify the user query into exactly one of these five intents:\n"
            "clinical_qa, literature_search, treatment_comparison, drug_interaction, content_review.\n"
            "Return ONLY the exact string of the intent."
        )
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.0
            )
            intent = response.choices[0].message.content.strip().lower()
            return intent
        except Exception as e:
            logger.error(f"Intent Classification Error: {e}")
            return "clinical_qa"

    async def process_clinical_qa(self, query: str) -> dict:
        """RAG pipeline extracting sentences returning structured Citations"""
        evidence_docs = await evidence_retriever.get_pubmed_abstracts(query, limit=5)
        
        context = ""
        for index, doc in enumerate(evidence_docs):
            context += f"Doc {index+1}: {doc['title']} ({doc['year']}) URL: {doc['pubmed_link']}\n"
            
        system_prompt = (
            "You are a clinical reasoning AI. Use the provided context to answer the clinical question. "
            "Output strictly raw JSON matching the following schema. For evidence, supply an array of objects "
            "with exactly keys: title, journal, year, pubmed_link.\n"
            "{\n"
            "  \"clinical_summary\": \"string\",\n"
            "  \"pathophysiology\": \"string\",\n"
            "  \"evidence\": [{\"title\": \"str\", \"journal\": \"str\", \"year\": \"str\", \"pubmed_link\": \"str\"}],\n"
            "  \"treatment_options\": [\"string\"],\n"
            "  \"confidence_level\": \"string\"\n"
            "}"
        )
        
        user_prompt = f"Context:\n{context}\n\nClinical Query: {query}"
        try:
            if not settings.OPENAI_API_KEY:
                return {"clinical_summary": "Simulated output", "pathophysiology": "Sim", "evidence": evidence_docs, "treatment_options": [], "confidence_level": "Low"}
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2
            )
            raw_content = response.choices[0].message.content
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:-3]
            return json.loads(raw_content)
        except Exception as e:
            logger.error(f"GPT-4 RAG Error: {e}")
            return {}

reasoning_service = AIReasoningService()
