from PIL import Image
import io

# Convert uploaded file to a tensor
async def read_image(file):
    image = Image.open(io.BytesIO(await file.read()))  # Open image from byte stream 
    return image