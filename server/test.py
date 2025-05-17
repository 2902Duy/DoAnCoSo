import json

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights
from utils import preprocess_image
from label_map import label_map

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model
num_classes = 98
model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
model.fc = nn.Sequential(
    nn.Linear(model.fc.in_features, 512),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(512, num_classes)
)
model.load_state_dict(torch.load("model/ResNet50.pth", map_location=torch.device('cpu')))
model.eval()

with open("food_data.json","r",encoding="utf-8") as f:
    food_data=json.load(f)

def get_food_info_by_key(key):
    for food in food_data:
        if food.get("key") == key:
            return food
    return None

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'status': 'fail', 'message': 'No image provided'}), 400

    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        image_tensor = preprocess_image(filepath)
        with torch.no_grad():
            outputs = model(image_tensor)
            _, predicted = torch.max(outputs, 1)
            prediction = predicted.item()
            probs = torch.softmax(outputs, dim=1)
            confidence = probs[0][prediction].item()
        food_info= get_food_info_by_key(label_map[prediction])

        return jsonify({
            # 'status': 'success',
            # 'filename': filename,
            'food_info': food_info if food_info else {},
            'predicted_class': prediction,
            'predicted_label': label_map[prediction],
            'confidence': round(confidence, 4)

        }), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
