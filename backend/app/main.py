from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routes import chat, upload
# from app.services.vector_store import load_vectorstore
import logging

# --------------------------------------------------
# App Initialization
# --------------------------------------------------

app = FastAPI(
    title="RAG Chatbot Service",
    version="1.0.0",
    description="Microservice for RAG-based PDF chatbot"
)

# --------------------------------------------------
# CORS (For Streamlit / Frontend)
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Startup Events
# --------------------------------------------------

# @app.on_event("startup")
# def startup_event():
#     print("🚀 Starting RAG Service...")

#     # Create DB tables
#     Base.metadata.create_all(bind=engine)

#     # Load FAISS vector store
#     load_vectorstore()

#     print("✅ Service Ready")

# --------------------------------------------------
# Health Check (Important for Microservices)
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# --------------------------------------------------
# Include Routers
# --------------------------------------------------

app.include_router(upload.router,prefix="/api")
app.include_router(chat.router,prefix="/api")
# app.include_router(upload.router, prefix="/api")