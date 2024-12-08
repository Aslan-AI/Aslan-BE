import os
import logging
from logging import getLogger

from dotenv import load_dotenv  # type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.user_services import router as user_router

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = getLogger(__name__)

PROXY_PREFIX = os.getenv("PROXY_PREFIX", "/api")
app = FastAPI(root_path=PROXY_PREFIX)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include other routers as needed
app.include_router(user_router)

@app.get("/health-check")
def health_check():
    return {"status": "ok"}

@app.get("/")
def home():
    return {"message": "Aslan AI welcomes you to the backend of the project."}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
