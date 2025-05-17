from flask import Flask, request, jsonify
import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights
from utils import preprocess_image
from label_map import label_map
app = Flask(__name__)

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

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    image_tensor = preprocess_image(file)
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        prediction = predicted.item()
        predicted_label = label_map[prediction]
        probs = torch.softmax(outputs, dim=1)
        confidence = probs[0][prediction].item()
    return jsonify({
        'predicted_class': prediction,
        'predicted_label': label_map[prediction],
        'confidence': round(confidence, 4)
    })

if __name__ == '__main__':
    app.run(debug=True)
