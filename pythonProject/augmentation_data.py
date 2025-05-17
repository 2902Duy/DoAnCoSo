import os
from PIL import Image
from torchvision import transforms
import random


root_dir = "images_split(1)/train"
target_count = 400


augmentation = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(30),
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3),
    transforms.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0)),
])


for class_name in os.listdir(root_dir):
    class_path = os.path.join(root_dir, class_name)
    if not os.path.isdir(class_path):
        continue

    images = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    current_count = len(images)

    if current_count >= target_count:
        print(f"{class_name}: đã đủ ({current_count})")
        continue

    print(f"{class_name}: {current_count} ảnh, augment thêm {target_count - current_count} ảnh")

    index = 0
    while current_count < target_count:
        img_name = random.choice(images)
        img_path = os.path.join(class_path, img_name)

        try:
            img = Image.open(img_path).convert("RGB")
            aug_img = augmentation(img)

            # Lưu ảnh mới
            save_name = f"aug_{index}_{img_name}"
            save_path = os.path.join(class_path, save_name)
            aug_img.save(save_path)

            current_count += 1
            index += 1
        except Exception as e:
            print(f"Lỗi với ảnh {img_name}: {e}")

print("Hoàn thành.")
