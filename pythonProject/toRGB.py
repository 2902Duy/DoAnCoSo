from PIL import Image
import os

folder_path = "images/data"

for root, dirs, files in os.walk(folder_path):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext == '.jpg':
            img_path = os.path.join(root, file)
            try:
                with Image.open(img_path) as img:
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                        img.save(img_path)
                        print(f"Đã chuyển {img_path} về RGB")
            except Exception as e:
                print(f"Lỗi xử lý ảnh {img_path}: {e}")
