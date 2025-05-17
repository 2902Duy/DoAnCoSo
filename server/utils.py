from PIL import Image
import torch
from torchvision import transforms

def convert_image_mode(img):
    if img.mode == 'P' or img.mode == 'LA':
        img = img.convert('RGB')
    return img

test_transform = transforms.Compose([
    transforms.Lambda(convert_image_mode),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

def preprocess_image(image_bytes):
    image = Image.open(image_bytes)
    image = test_transform(image)
    return image.unsqueeze(0)  # thêm batch dimension
