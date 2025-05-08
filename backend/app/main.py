from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.predict import router as predict_router

app = FastAPI()

# Allow CORS for specific origins
origins = [
    "https://fcatvdog.onrender.com",  # your deployed frontend
    "http://localhost:5173",          # local dev frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # or use ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router for the /predict route
app.include_router(predict_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Cat vs Dog API!"}
