from pydantic import BaseModel, Field
from typing import List, Optional


class RecommendRequest(BaseModel):
    food_id: Optional[int] = None
    food_name: str
    food_category: str
    moisture_sensitivity: int = Field(ge=1, le=5)
    oxygen_sensitivity: int = Field(ge=1, le=5)
    light_sensitivity: int = Field(ge=1, le=5)
    fat_content: int = Field(ge=1, le=5)
    storage_temperature_c: float
    relative_humidity: float
    expected_shelf_life_days: int
    cost_priority: int = Field(ge=1, le=5)
    sustainability_priority: int = Field(ge=1, le=5)


class MaterialResult(BaseModel):
    material_id: int
    material_name: str
    short_code: str
    material_form: str
    compatibility_score: float
    oxygen_barrier: int
    moisture_barrier: int
    light_barrier: int
    grease_resistance: int
    mechanical_strength: int
    heat_resistance: int
    cost_level: int
    sustainability_level: int
    recyclable: bool
    compostable: bool
    data_status: str
    example_applications: str
    advantages: List[str]
    limitations: List[str]
    reasons: List[str]


class RecommendResponse(BaseModel):
    recommendation_id: int
    food_name: str
    results: List[MaterialResult]


class CompareRequest(BaseModel):
    material_ids: List[int] = Field(min_length=2, max_length=3)
    expected_shelf_life_days: Optional[int] = None
