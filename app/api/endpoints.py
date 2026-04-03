from fastapi import APIRouter, Request
from app.models.schemas import UnifiedMobileRequest, UnifiedMobileResponse
from app.services.ai_reasoning import reasoning_service
from app.services.evidence_retrieval import evidence_retriever

router = APIRouter()

@router.post("/ask-clinical-question", response_model=UnifiedMobileResponse)
async def ask_clinical_question(request: Request, payload: UnifiedMobileRequest):
    """
    Unified Orchestrator Endpoint for the Mobile App.
    Accepts any clinical string, uses GPT-4 to classify intent, and delegates to the appropriate pipeline.
    """
    query = payload.query
    
    # Rate limiting applied in main.py via request object if needed
    
    intent = await reasoning_service.classify_intent(query)
    
    data = {}
    
    if intent == "clinical_qa":
        data = await reasoning_service.process_clinical_qa(query)
        
    elif intent == "literature_search":
        docs = await evidence_retriever.get_pubmed_abstracts(query, limit=10)
        data = {"papers": docs}
        
    elif intent == "drug_interaction":
        # MVP heuristic to split 2 drugs from query e.g. "interaction between Warfarin and Fluconazole" 
        # (A production version would use an LLM entity extractor here)
        words = query.replace(" and ", " ").split()
        d_a = words[-2] if len(words) >= 2 else "DrugA"
        d_b = words[-1] if len(words) >= 2 else "DrugB"
        
        res = await evidence_retriever.get_openfda_interaction(d_a, d_b)
        res["drug_a"] = d_a
        res["drug_b"] = d_b
        data = res
        
    elif intent == "treatment_comparison":
        data = {
            "comparison_table": [{
                "treatment_name": "Treatment A",
                "mechanism_of_action": "Sample Mech",
                "advantages": ["Advantage 1"],
                "disadvantages": ["Disadvantage 1"],
                "evidence_level": "Moderate"
            }],
            "conclusion": f"MVP comparison placeholder for {query}"
        }
        
    elif intent == "content_review":
        data = {
            "accuracy_score": 90,
            "misleading_claims": [],
            "evidence_support": "Supported",
            "suggested_corrections": []
        }
    else:
        # Fallback
        intent = "clinical_qa"
        data = await reasoning_service.process_clinical_qa(query)
        
    return UnifiedMobileResponse(intent=intent, data=data)
