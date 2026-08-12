import os
import logging
from fastapi import APIRouter, HTTPException, status
from src.llm.schema import TriageRequest, TriageResponse
from src.llm.repair import process_and_validate_triage

logger = logging.getLogger("TriageRoute")

router = APIRouter()

PROMPT_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "prompts", "triage-v1.md")

def load_system_prompt() -> str:
    if not os.path.exists(PROMPT_FILE):
        raise RuntimeError(f"System prompt file missing at '{PROMPT_FILE}'.")
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()

@router.post("/triage", response_model=TriageResponse)
def triage_support_message(req: TriageRequest):
    """
    POST /api/v1/triage
    Classifies a customer support message into category, urgency, confidence, and reason.
    - Validates input length (1-2000 chars) -> Returns 400 on invalid input before calling model.
    - Loads versioned system prompt from prompts/triage-v1.md.
    - Enforces schema validation, 1 repair retry, quarantine log on failure, and explicit timeout.
    """
    # System prompt loading
    system_prompt = load_system_prompt()
    
    # Process & Validate (Handles repair, quarantine, kill switch, stub mode)
    validated_response, metrics = process_and_validate_triage(
        system_prompt=system_prompt,
        user_message=req.text,
        prompt_version="v1.0.0"
    )
    
    return validated_response
