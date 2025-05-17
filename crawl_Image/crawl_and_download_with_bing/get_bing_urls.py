import os
from icrawler.builtin import BingImageCrawler
from icrawler.downloader import Downloader



# Danh sách từ khóa tìm kiếm
keywords = [
    'lòng luộc'

]


MAX_LINKS = 200
SAVE_DIR = ("urls_bing")
OUTPUT_FILE = os.path.join(SAVE_DIR, f"{keywords[0]}_all_urls.txt")

# Tạo thư mục nếu chưa có
os.makedirs(SAVE_DIR, exist_ok=True)

class LinkCollectorDownloader(Downloader):
    def __init__(self, *args, **kwargs):
        self.urls = set()
        super().__init__(*args, **kwargs)

    def download(self, task, default_ext, timeout=5, **kwargs):
        file_url = task.get('file_url')
        if file_url:
            self.urls.add(file_url)



all_urls = set()

for kw in keywords:
    print(f"[INFO] Đang thu thập URL cho: {kw}")

    crawler = BingImageCrawler(
        downloader_cls=LinkCollectorDownloader,
        feeder_threads=1,
        parser_threads=2,
        downloader_threads=2,
        storage={'root_dir': 'ignore'}
    )

    crawler.crawl(keyword=kw, max_num=MAX_LINKS)

    all_urls.update(crawler.downloader.urls)

print(f"[INFO] Tổng số URL thu thập được: {len(all_urls)}")

# Ghi tất cả URL vào một file duy nhất
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write("\n".join(all_urls))

print(f"[INFO] Đã lưu {len(all_urls)} URL vào {OUTPUT_FILE}")
