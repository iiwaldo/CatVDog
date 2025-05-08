from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.predict import router as predict_router

app = FastAPI()

# Allow CORS for specific origins (React frontend running on localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the router for the /predict route
app.include_router(predict_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Cat vs Dog API!"}
