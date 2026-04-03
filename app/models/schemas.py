from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# Shared Citations
class Citation(BaseModel):
    title: str
    journal: str
    year: str
    pubmed_link: str

# 1. Clinical QA Schema
class ClinicalQAResponse(BaseModel):
    clinical_summary: str
    pathophysiology: str
    evidence: List[Citation]
    treatment_options: List[str]
    confidence_level: str

# 2. Literature Search Schema
class DocumentItem(BaseModel):
    title: str
    authors: List[str]
    journal: str
    year: str
    abstract: str
    pubmed_link: str

class LiteratureSearchResponse(BaseModel):
    papers: List[DocumentItem]

# 3. Treatment Comparison Schema
class TreatmentComparisonTable(BaseModel):
    treatment_name: str
    mechanism_of_action: str
    advantages: List[str]
    disadvantages: List[str]
    evidence_level: str

class TreatmentComparisonResponse(BaseModel):
    comparison_table: List[TreatmentComparisonTable]
    conclusion: str

# 4. Content Review Schema
class ContentReviewResponse(BaseModel):
    accuracy_score: int
    misleading_claims: List[str]
    evidence_support: str
    suggested_corrections: List[str]

# 5. Drug Interaction Schema
class DrugInteractionResponse(BaseModel):
    drug_a: str
    drug_b: str
    interaction_mechanism: str
    severity_level: str
    clinical_recommendation: str
    reference_sources: List[Citation]

# Mobile Unified Wrapper
class UnifiedMobileRequest(BaseModel):
    query: str

class UnifiedMobileResponse(BaseModel):
    intent: str
    data: Dict[str, Any]
