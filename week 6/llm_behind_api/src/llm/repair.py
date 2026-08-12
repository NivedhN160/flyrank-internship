import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Tuple
from fastapi import HTTPException
from pydantic import ValidationError
from src.llm.schema import TriageResponse
from src.llm.client import call_llm, store_in_cache

logger = logging.getLogger("LLMRepairEngine")

QUARANTINE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
os.makedirs(QUARANTINE_DIR, exist_ok=True)
QUARANTINE_FILE = os.path.join(QUARANTINE_DIR, "quarantine.jsonl")

def clean_and_parse_json(raw_text: str) -> Dict[str, Any]:
    """Strips markdown code fences (e.g. ```json ... ```) and parses JSON string."""
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return json.loads(text)

def log_to_quarantine(user_message: str, raw_output: str, error_detail: str, prompt_version: str):
    """Logs raw un-repairable model outputs to logs/quarantine.jsonl for audit."""
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt_version": prompt_version,
        "user_input": user_message,
        "raw_model_output": raw_output,
        "validation_error": error_detail
    }
    with open(QUARANTINE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    logger.warning(f"☣️ Quarantined failed model output into {QUARANTINE_FILE}")

def process_and_validate_triage(
    system_prompt: str,
    user_message: str,
    prompt_version: str = "v1.0.0"
) -> Tuple[TriageResponse, Dict[str, Any]]:
    """
    Parses & validates model output against TriageResponse.
    - If initial output fails, executes exactly ONE repair retry handing model its error.
    - If repair retry fails, logs to logs/quarantine.jsonl and returns HTTP 422.
    """
    # 1. Initial Model Call
    raw_output, metrics = call_llm(system_prompt, user_message, prompt_version=prompt_version)
    
    try:
        parsed_json = clean_and_parse_json(raw_output)
        validated_response = TriageResponse.model_validate(parsed_json)
        store_in_cache(prompt_version, user_message, validated_response.model_dump())
        return validated_response, metrics
    
    except (json.JSONDecodeError, ValidationError) as initial_err:
        logger.warning(f"⚠️ Initial LLM output failed schema validation: {initial_err}. Triggering REPAIR RETRY (1/1)...")
        
        # 2. Repair Retry (Exactly ONCE)
        repair_user_msg = (
            f"Original Input: \"{user_message}\"\n\n"
            f"Your Previous Raw Response:\n\"{raw_output}\"\n\n"
            f"Validation Error:\n{str(initial_err)}\n\n"
            f"Please correct your answer. Return ONLY a valid JSON object matching the required schema."
        )
        
        try:
            repaired_raw, repair_metrics = call_llm(
                system_prompt,
                repair_user_msg,
                prompt_version=prompt_version,
                repair_attempt=True
            )
            
            repaired_json = clean_and_parse_json(repaired_raw)
            validated_response = TriageResponse.model_validate(repaired_json)
            
            metrics["repaired"] = True
            metrics["repair_tokens"] = repair_metrics.get("input_tokens", 0) + repair_metrics.get("output_tokens", 0)
            
            logger.info("✅ Repair Retry SUCCEEDED! Schema validation passed on second attempt.")
            store_in_cache(prompt_version, user_message, validated_response.model_dump())
            return validated_response, metrics
        
        except (json.JSONDecodeError, ValidationError) as repair_err:
            error_msg = f"Repair retry failed schema validation: {repair_err}"
            logger.error(f"❌ {error_msg}")
            
            # 3. Quarantine on Double Failure & Return HTTP 422
            log_to_quarantine(user_message, raw_output, str(repair_err), prompt_version)
            
            raise HTTPException(
                status_code=422,
                detail=f"Unprocessable Entity: Model output failed schema validation after repair retry. {str(repair_err)}"
            )
