import requests

files = {'file': open('images/banh_beo_1.jpg', 'rb')}
res = requests.post('http://127.0.0.1:5000/predict', files=files)
print(res.json())
