import os
import time
import random
import hashlib
import logging
from typing import Dict, Any, Tuple, Optional
from openai import OpenAI, APIError, APIConnectionError, RateLimitError, APITimeoutError, AuthenticationError
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("LLMClient")

# In-Memory Cache Store (Hash key -> Triage dict)
_CACHE_STORE: Dict[str, Dict[str, Any]] = {}

def get_openai_client() -> OpenAI:
    base_url = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    api_key = os.getenv("LLM_API_KEY", "sk-or-v1-mock_key")
    # Set explicit timeout of 30 seconds (Default 10 min SDK timeout is NOT allowed)
    return OpenAI(base_url=base_url, api_key=api_key, timeout=30.0)

def call_llm(
    system_prompt: str,
    user_message: str,
    prompt_version: str = "v1.0.0",
    repair_attempt: bool = False
) -> Tuple[str, Dict[str, Any]]:
    """
    Executes an LLM API call with explicit timeout, retries (timeouts/429/5xx only),
    kill-switch check, stub-mode check, cost logging, and optional response caching.
    """
    # 1. Kill Switch Check (Stage 4)
    if os.getenv("LLM_ENABLED", "true").lower() == "false":
        logger.info("🛑 Kill Switch ACTIVE (LLM_ENABLED=false). Returning safe fallback.")
        fallback = {
            "category": "other",
            "urgency": "normal",
            "confidence": 0.5,
            "reason": "Kill switch enabled: LLM calls disabled in current environment."
        }
        import json
        return json.dumps(fallback), {"prompt_version": prompt_version, "model": "kill-switch", "input_tokens": 0, "output_tokens": 0, "duration_ms": 0, "from_cache": False}

    # 2. Stub Mode Check (Stage 1)
    if os.getenv("LLM_STUB", "0") == "1":
        logger.info("🧪 Stub Mode ACTIVE (LLM_STUB=1). Returning hard-coded valid response (0 model calls).")
        stub_data = {
            "category": "bug",
            "urgency": "high",
            "confidence": 0.95,
            "reason": "Stub response: Classified as high-urgency bug for testing contract."
        }
        import json
        return json.dumps(stub_data), {"prompt_version": prompt_version, "model": "stub", "input_tokens": 0, "output_tokens": 0, "duration_ms": 0, "from_cache": False}

    # 3. Optional In-Memory Cache Check
    cache_enabled = os.getenv("LLM_CACHE", "true").lower() == "true"
    cache_key = hashlib.sha256(f"{prompt_version}:{user_message}".encode("utf-8")).hexdigest() if cache_enabled else ""
    if cache_enabled and not repair_attempt and cache_key in _CACHE_STORE:
        logger.info(f"⚡ Cache HIT for key '{cache_key[:8]}...'. Returning cached response.")
        cached = _CACHE_STORE[cache_key]
        import json
        return json.dumps(cached), {"prompt_version": prompt_version, "model": "cache", "input_tokens": 0, "output_tokens": 0, "duration_ms": 0, "from_cache": True}

    client = get_openai_client()
    model = os.getenv("LLM_MODEL", "openrouter/free")

    max_retries = 3
    attempt = 0
    start_time = time.time()

    while attempt < max_retries:
        attempt += 1
        try:
            logger.info(f"📡 Sending API Call (Attempt {attempt}/{max_retries}) | Model: {model}")
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.1 # Low temperature for deterministic output
            )

            duration_ms = int((time.time() - start_time) * 1000)
            content = response.choices[0].message.content or ""
            
            usage = response.usage
            input_tokens = usage.prompt_tokens if usage else 0
            output_tokens = usage.completion_tokens if usage else 0

            metrics = {
                "prompt_version": prompt_version,
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "duration_ms": duration_ms,
                "attempts": attempt,
                "from_cache": False
            }

            logger.info(f"📊 Model Call Metrics | Duration: {duration_ms}ms | Input Tokens: {input_tokens} | Output Tokens: {output_tokens}")
            
            return content, metrics

        except AuthenticationError as e:
            # 401 Unauthorized -> NEVER RETRY! (Stage 4 requirement)
            logger.error("❌ Authentication Error (401 Bad Key). Failing fast without retrying.")
            raise e

        except (RateLimitError, APITimeoutError, APIConnectionError) as e:
            # Retriable errors: Timeout, 429, 5xx
            if attempt >= max_retries:
                logger.error(f"❌ Max retries reached after retriable error: {e}")
                raise e

            # Exponential backoff with jitter: 1s, 2s, 4s + random(0-0.5s)
            sleep_time = (2 ** (attempt - 1)) + random.uniform(0, 0.5)
            logger.warning(f"⚠️ Retriable error encountered ({type(e).__name__}). Retrying in {sleep_time:.2f}s...")
            time.sleep(sleep_time)

        except APIError as e:
            if e.status_code and e.status_code in [400, 401, 403]:
                logger.error(f"❌ Non-retriable HTTP {e.status_code} API Error. Failing fast.")
                raise e
            if attempt >= max_retries:
                raise e
            sleep_time = (2 ** (attempt - 1)) + random.uniform(0, 0.5)
            time.sleep(sleep_time)

    raise RuntimeError("LLM Call failed after all retries.")

def store_in_cache(prompt_version: str, user_message: str, parsed_dict: Dict[str, Any]):
    if os.getenv("LLM_CACHE", "true").lower() == "true":
        cache_key = hashlib.sha256(f"{prompt_version}:{user_message}".encode("utf-8")).hexdigest()
        _CACHE_STORE[cache_key] = parsed_dict
