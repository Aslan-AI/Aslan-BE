from transformers import pipeline

# Initializing the model
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)

COPING_STRATEGIES = {
    "POSITIVE": [
        "Keep up the good work and stay focused on your goals!",
        "Celebrate this moment—small wins matter.",
        "Use this positive energy to tackle a task you've been postponing.",
    ],
    "NEGATIVE": [
        "Take a few deep breaths and remind yourself it's okay to feel this way.",
        "Consider journaling your feelings to gain some clarity.",
        "Reach out to a trusted friend or family member for support.",
    ],
}

EMOTION_MAPPING = {
    "POSITIVE": ["calm", "happy"],
    "NEGATIVE": ["sad", "angry"],
}

def analyze_sentiment_and_suggest(text):
    """
    Analyze the sentiment of the input text and provide a coping strategy.
    """
    result = sentiment_analyzer(text)[0]
    label = result["label"]
    score = result["score"]

    emotions = EMOTION_MAPPING["POSITIVE" if label == "POSITIVE" else "NEGATIVE"]
    strategies = COPING_STRATEGIES["POSITIVE" if label == "POSITIVE" else "NEGATIVE"]
    strategy = strategies[0]
    
# Determine color flag
    if score >= 0.85:
        color_flag = "green"
    elif score >= 0.6:
        color_flag = "yellow"
    else:
        color_flag = "red"


    return {
        "sentiment": label,
        "emotions": emotions,
        "confidence": round(score, 2),
        "strategy": strategy,
        "color_flag": color_flag,
    }
