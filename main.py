from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import detect_handler

app = FastAPI(
    title="Healthy-eye API",
    description="API for detecting fruits & vegetables in meal images",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "Welcome to Healthy-eye API"}

# Include routers
app.include_router(detect_handler.handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 