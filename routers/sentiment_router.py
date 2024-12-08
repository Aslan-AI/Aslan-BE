from fastapi import APIRouter
from services.sentiment_service import analyze_sentiment_and_suggest

router = APIRouter()

@router.post("/analyze")
def analyze_sentiment(text: str):
    """
    Endpoint to analyze sentiment and return a coping strategy.
    """
    return analyze_sentiment_and_suggest(text)
