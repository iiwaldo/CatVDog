from fastapi import APIRouter, File, UploadFile
from app.models.model import load_model, predict_image
from app.utils.image_utils import read_image

router = APIRouter()
model = load_model()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = await read_image(file)  # Convert the uploaded file into an image tensor
    result = predict_image(model, image)  # Get the prediction from the model
    return {"prediction": result}
