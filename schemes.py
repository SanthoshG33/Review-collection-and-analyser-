from pydantic import BaseModel

class ReviewCreate(BaseModel):
    business_name: str
    review_text: str