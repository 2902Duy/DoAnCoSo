import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

LINKS_URL='urls_gg'
MAX_IMAGES=350
os.makedirs(LINKS_URL, exist_ok=True)

def get_images_from_google(driver, delay, max_images):
    image_urls = set()

    def scroll_down():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    try:
        print("Đang tải trang Google Images...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "img"))
        )
        print("Trang đã tải xong cơ bản")

        attempts = 0
        max_attempts = 3
        while len(image_urls) < max_images and attempts < max_attempts:
            scroll_down()
            print(f"Cuộn trang lần {attempts + 1}...")
            images = driver.find_elements(By.XPATH,
                                          "//img[contains(@class, 'YQ4gaf') or contains(@class, 'rg_i') or @data-src or @src]")
            print(f"Tìm thấy {len(images)} ảnh trên trang")
            for img in images:
                try:
                    # Thử lấy src hoặc data-src (Google đôi khi dùng data-src cho lazy loading)
                    src = img.get_attribute('src') or img.get_attribute('data-src')
                    if (src and 'http' in src and not src.startswith('data:image') and src not in image_urls
                            and (int(img.get_attribute('width'))>150 and int(img.get_attribute('height'))>150)):
                        image_urls.add(src)
                    if len(image_urls) >= max_images:
                        break
                except Exception as e:
                    print(f"Lỗi khi lấy URL ảnh: {e}")
                    continue
            attempts += 1
            if not images:
                print("Không tìm thấy ảnh, thử in HTML để debug:")
                print(driver.page_source[:500])  # In 500 ký tự đầu của HTML để kiểm tra
    except TimeoutException:
        print("Hết thời gian chờ tải trang, có thể do mạng hoặc Google chặn")
        print("HTML của trang:", driver.page_source[:500])  # Debug HTML
    return image_urls

def main():
    search_query = input("Nhập từ khóa tìm kiếm trên Google Images: ")
    filename = f"{LINKS_URL}/{search_query}_urls.txt"
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(options=options)
        search_url = f"https://www.google.com/search?q={search_query}&tbm=isch&hl=vi=isz:l"
        driver.get(search_url)


        image_urls = get_images_from_google(driver, 2, MAX_IMAGES)

        if image_urls:
            with open(filename, 'w', encoding='utf-8') as f:
                images = driver.find_elements(By.CSS_SELECTOR, "img.rg_i.Q4LuWd")
                for i, img in enumerate(image_urls, 1):
                    f.write(f"{img}\n")

        else:
            print("Không tìm thấy URL ảnh nào!")

        return image_urls

    except WebDriverException as e:
        print(f"Lỗi WebDriver: {e}")
        print("Kiểm tra: 1) ChromeDriver có khớp phiên bản Chrome không, 2) Kết nối internet")
        return set()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()