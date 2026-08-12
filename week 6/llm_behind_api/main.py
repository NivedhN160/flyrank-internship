import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.routes.triage import router as triage_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

app = FastAPI(
    title="Support Message Triage AI API",
    description="Production-grade API endpoint putting an LLM behind a strict contract, timeout, retry policy, and validation schema.",
    version="1.0.0"
)

# Custom 400 Handler for Input Validation Failures (Stage 1 Requirement: Returns 400 Bad Request naming field)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first_err = errors[0] if errors else {}
    field_name = ".".join(str(x) for x in first_err.get("loc", []))
    msg = first_err.get("msg", "Invalid input parameter")
    return JSONResponse(
        status_code=400,
        content={
            "error": "Bad Request",
            "field": field_name,
            "message": f"Input validation failed on '{field_name}': {msg}"
        }
    )

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Support Message Triage AI API",
        "version": "1.0.0"
    }

app.include_router(triage_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
