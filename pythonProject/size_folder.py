import os

path_name = "F:\DoAnCoSo\pythonProject\images\data"
total_files = 0
total_folder =0
lens = []


for folder_name in os.listdir(path_name):
    folder_path = os.path.join(path_name, folder_name)

    if os.path.isdir(folder_path):

        file_count = len([
            f for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ])
        print(f"\"{folder_name}\",")
        total_files += file_count
        lens.append(file_count)
    total_folder+=1

print(f"\nTổng số file: {total_files}")
print(f"\nTổng số folder: {total_folder}")
print(f"Số file theo từng thư mục: {lens}")