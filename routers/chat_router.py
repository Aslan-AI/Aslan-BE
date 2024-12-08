from fastapi import APIRouter
from services.sentiment_service import analyze_sentiment_and_suggest

router = APIRouter()

chat_sessions = {}

@router.post("/api/chat/session")
def start_chat_session(client_id: str):
    """
    Start a new chat session.
    """
    if client_id not in chat_sessions:
        chat_sessions[client_id] = []
    return {"message": f"Chat session started for client {client_id}"}

@router.post("/api/chat/message")
def save_chat_message(client_id: str, message: str):
    """
    Save a message to the chat session and analyze its sentiment.
    """
    if client_id not in chat_sessions:
        return {"error": "Chat session not found for client"}, 404
    
    analysis = analyze_sentiment_and_suggest(message)
    chat_sessions[client_id].append({"message": message, "analysis": analysis})
    return {"message": "Message saved", "analysis": analysis}

@router.get("/api/chat/history")
def get_chat_history(client_id: str):
    """
    Retrieve the chat history for a client.
    """
    if client_id not in chat_sessions:
        return {"error": "Chat session not found for client"}, 404

    return {"chat_history": chat_sessions[client_id]}
