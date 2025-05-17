import os
import shutil
import random

root_dir = "images/data"
output_dir = "images_split(1)"
train_ratio = 0.8

for split in ['train', 'test']:
    split_path = os.path.join(output_dir, split)
    if not os.path.exists(split_path):
        os.makedirs(split_path)

for class_name in os.listdir(root_dir):
    class_path = os.path.join(root_dir, class_name)
    if not os.path.isdir(class_path):
        continue

    images = os.listdir(class_path)
    random.shuffle(images)

    train_count = int(len(images) * train_ratio)
    train_images = images[:train_count]
    test_images = images[train_count:]

    for split, split_images in zip(['train', 'test'], [train_images, test_images]):
        split_class_dir = os.path.join(output_dir, split, class_name)
        os.makedirs(split_class_dir, exist_ok=True)

        for img in split_images:
            src = os.path.join(class_path, img)
            dst = os.path.join(split_class_dir, img)
            shutil.copyfile(src, dst)
    print(f"hoàn thành {class_name}")

print("Hoàn tất chia dữ liệu.")
