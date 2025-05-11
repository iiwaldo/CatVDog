import torch
import torchvision.transforms as transforms
from PIL import Image
import torch
from torch import nn
import os

class CatVDogV0(nn.Module):
    def __init__(self, input_shape=3, hidden_units=32, output_shape=2):
        super().__init__()

        self.conv_block_1 = nn.Sequential(
            nn.Conv2d(input_shape, hidden_units, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(hidden_units),
            nn.ReLU(),

            nn.Conv2d(hidden_units, hidden_units, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(hidden_units),
            nn.ReLU(),

            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.conv_block_2 = nn.Sequential(
            nn.Conv2d(hidden_units, hidden_units * 2, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(hidden_units * 2),
            nn.ReLU(),

            nn.Conv2d(hidden_units * 2, hidden_units * 2, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(hidden_units * 2),
            nn.ReLU(),

            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.conv_block_3 = nn.Sequential(
            nn.Conv2d(hidden_units*2, hidden_units * 4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(hidden_units * 4),
            nn.ReLU(),

            nn.Conv2d(hidden_units * 4, hidden_units * 4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(hidden_units * 4),
            nn.ReLU(),

            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(hidden_units * 4 * 28 * 28, output_shape)
        )

    def forward(self, x):
        x = self.conv_block_1(x)
        x = self.conv_block_2(x)
        #print(x.shape)
        x = self.conv_block_3(x)
        #print(x.shape)
        x = self.classifier(x)
        return x

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5],
                         std=[0.5, 0.5, 0.5])
])

# Load your saved model
def load_model():
    model = CatVDogV0(input_shape=3, hidden_units=32, output_shape=2)
    model_path = os.path.join(os.path.dirname(__file__), 'model_2_v3.pth')
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))) 
    return model

# Function to make a prediction
def predict_image(model, image):
    model.eval()
    image_tensor = transform(image).unsqueeze(0)
    class_names = ["Cat","Dog"]
    with torch.inference_mode():  # No need to track gradients
        output = model(image_tensor)
        probs = torch.softmax(output, dim=1)
        predicted = torch.argmax(probs, dim=1).item()
        print(class_names[predicted])
        return class_names[predicted]  # Return the class index
