from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):

    predicted_category: str = Field(..., description="The predicted insurance premium category", example="high")

    confidence: float = Field(..., description="The confidence score of the prediction", example=0.85)

    class_probabilities: Dict[str, float] = Field(..., description="The probabilities for each insurance premium category", example={"low": 0.01, "medium": 0.15, "high": 0.85})