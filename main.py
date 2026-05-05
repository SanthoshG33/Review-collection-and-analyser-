from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

import models
import database
from sentiment import analyze_sentiment

# ✅ CREATE APP FIRST
app = FastAPI()

# Templates
templates = Jinja2Templates(directory="templates")

# Create DB tables
database.Base.metadata.create_all(bind=database.engine)

# DB Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ HOME ROUTE
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

# ✅ SUBMIT REVIEW
@app.post("/submit")
def submit_review(
    request: Request,
    business_name: str = Form(...),
    review_text: str = Form(...),
    db: Session = Depends(get_db)
):
    sentiment = analyze_sentiment(review_text)

    new_review = models.Review(
        business_name=business_name,
        review_text=review_text,
        sentiment=sentiment
    )

    db.add(new_review)
    db.commit()

    return RedirectResponse(url="/dashboard", status_code=303)

# ✅ DASHBOARD
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, query: str = "", db: Session = Depends(get_db)):

    if query:
        reviews = db.query(models.Review).filter(
            models.Review.business_name.contains(query)
        ).all()
    else:
        reviews = db.query(models.Review).all()

    positive = sum(1 for r in reviews if r.sentiment == "Positive")
    negative = sum(1 for r in reviews if r.sentiment == "Negative")
    neutral = sum(1 for r in reviews if r.sentiment == "Neutral")

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "reviews": reviews,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "query": query
        }
    )