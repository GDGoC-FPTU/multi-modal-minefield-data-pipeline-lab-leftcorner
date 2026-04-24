from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!

class UnifiedDocument(BaseModel):
    # TODO: Define the v1 schema. 
    # Suggested fields: document_id, content, source_type, author, timestamp, metadata
    
    document_id: str = Field(..., description="A unique identifier for the document")
    content: str = Field(..., description="The main content of the document")
    source_type: str = Field(..., description="The type of the source document")
    author: Optional[str] = Field(default="Unknown", description="The author of the document")
    timestamp: Optional[datetime] = Field(default=None, description="The timestamp of the document")

    # You might want a dict for source-specific metadata
    source_metadata: dict = Field(default_factory=dict)

    model_config = {
        "extra": "allow"
    }
