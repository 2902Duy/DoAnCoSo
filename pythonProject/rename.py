import os

folder_path = "images/data"

image_extensions = [".jpeg", ".png", ".bmp", ".tiff", ".webp", ".jfif", ".heic", ".jpg"]

for root, dirs, files in os.walk(folder_path):
    idx=0
    for filename in files:
        file_ext = os.path.splitext(filename)[1].lower()

        if file_ext in image_extensions:
            name_without_ext = os.path.splitext(filename)[0]
            new_filename =f"image_{idx}.jpg"
            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, new_filename)

            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"Đã đổi: {old_path} → {new_path}")
        idx+=1



