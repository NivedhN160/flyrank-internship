from enum import Enum
from pydantic import BaseModel, Field

class CategoryEnum(str, Enum):
    BILLING = "billing"
    BUG = "bug"
    FEATURE = "feature"
    SECURITY = "security"
    OTHER = "other"

class UrgencyEnum(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

class TriageRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="Customer support message content (1-2000 chars)")

class TriageResponse(BaseModel):
    category: CategoryEnum
    urgency: UrgencyEnum
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")
    reason: str = Field(..., description="One short sentence explaining the classification decision")
