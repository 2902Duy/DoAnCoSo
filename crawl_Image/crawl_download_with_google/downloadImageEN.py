import shutil
import requests
import os
import time
from urllib.parse import urlparse, parse_qs
from parameter import SAVE_ROOT

save_dir = SAVE_ROOT ##url
link_folder ="urls_gg"
ARCHIVE_FOLDER='urls'
os.makedirs(save_dir, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def download_image(url, filename):
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()

        # Xác định định dạng ảnh từ URL hoặc Content-Type
        content_type = response.headers.get('content-type', '')
        if 'jpeg' in content_type or 'jpg' in content_type:
            ext = '.jpg'
        elif 'png' in content_type:
            ext = '.png'
        else:
            # Nếu không xác định được, kiểm tra tham số URL
            parsed = urlparse(url)
            if 'jpg' in parsed.path.lower():
                ext = '.jpg'
            elif 'png' in parsed.path.lower():
                ext = '.png'
            else:
                ext = '.jpg'  # Mặc định

        full_path = f"{filename}{ext}"

        with open(full_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Đã tải: {full_path}")
        return True

    except Exception as e:
        print(f"Lỗi khi tải {url}: {str(e)}")
        return False

for file in os.listdir(link_folder):
    if file.endswith('.txt'):
        hashtag = file.replace('.txt', '')
        save_dir = os.path.join(save_dir, hashtag)
        os.makedirs(save_dir, exist_ok=True)
        txt_path = os.path.join(link_folder, file)
        with open(os.path.join(link_folder, file), 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]

        print(f"\n[INFO] Đang tải {len(urls)} ảnh từ #{hashtag}...")

        for idx, url in enumerate(urls):
            download_image(url, os.path.join(save_dir, f"image_{idx}"))
            time.sleep(1)
        shutil.move(txt_path, os.path.join(ARCHIVE_FOLDER, file))
        print(f"[INFO] Đã chuyển {file} vào {ARCHIVE_FOLDER}/")

print("Hoàn thành tải ảnh!")