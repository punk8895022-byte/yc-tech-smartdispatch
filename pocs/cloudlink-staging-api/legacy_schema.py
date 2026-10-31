"""CloudLink legacy category mapping. No money flows; reject unsupported types."""
from typing import Literal
from pydantic import BaseModel, Field

class LegacyRequest(BaseModel):
    categoryId: Literal["net", "cctv", "access"]
    region: str = Field(min_length=2, max_length=60)
    description: str = Field(min_length=12, max_length=1000)

CATEGORY_MAP = {"net": "network", "cctv": "cctv", "access": "access"}

def normalize_legacy_request(body: LegacyRequest) -> dict[str, str]:
    return {"category": CATEGORY_MAP[body.categoryId],
            "region": body.region, "description": body.description}
