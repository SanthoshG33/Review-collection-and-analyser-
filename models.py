from sqlalchemy import Column, Integer, String
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String)
    review_text = Column(String)
    sentiment = Column(String)