import binascii
import hashlib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

import time
from urllib.parse import urlparse
import os
import requests
import io
from PIL import Image

from scrapers.google import patch
from config import settings
from logger.logger import logger


class GoogleImageScraper:
    def __init__(
            self,
            webdriver_path,
            image_path,
            search_key="iPhone 8",
            number_of_images=1,
            headless=True,
            min_resolution=(0, 0),
            max_resolution=(1920, 1080),
            max_missed=10,
    ):
        self.image_path = os.path.join(image_path, search_key)
        self.number_of_images = (
            number_of_images if isinstance(number_of_images, int) else 1
        )
        self.headless = headless
        self.setup_directories(self.image_path)
        self.driver = self.setup_driver(webdriver_path, headless)
        self.search_key = search_key
        self.webdriver_path = webdriver_path
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.max_missed = max_missed
        self.url = settings.GOOGLE_SEARCH_URL
        self.existing_files = self.get_existing_files()

    def get_existing_files(self):
        files = [f for f in os.listdir(self.image_path) if os.path.isfile(os.path.join(self.image_path, f))]
        return set(files)

    @staticmethod
    def setup_directories(image_path):
        if not os.path.exists(image_path):
            try:
                os.makedirs(image_path)
                logger.info("Image path not found. Creating a new folder.")
            except Exception as e:
                raise IOError(f"Failed to create directory {image_path}: {str(e)}")

    @staticmethod
    def setup_driver(webdriver_path, headless):
        if not os.path.isfile(webdriver_path):
            is_patched = patch.download_latest_chromedriver()
            if not is_patched:
                raise RuntimeError(
                    "Please update the chromedriver in the webdriver folder according to your Chrome version"
                )

        options = Options()
        if headless:
            options.add_argument("--headless")

        try:
            driver = webdriver.Chrome(options=options)
            driver.set_window_size(1400, 1050)
            driver.get("https://www.google.com")
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "W0wltc"))
                ).click()
            except Exception as e:
                logger.warn(f"Accepting cookies failed: {str(e)}")
        except Exception as e:
            raise WebDriverException(f"Failed to initialize WebDriver: {str(e)}")

        return driver

    def find_image_urls(self):
        """
        This function search and return a list of image urls based on the search key.
        Example:
            google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
            image_urls = google_image_scraper.find_image_urls()

        """
        logger.info("Gathering image links")

        self.driver.get(self.url)
        image_urls = []
        count = 0
        missed_count = 0
        indx_1 = 0
        indx_2 = 0
        search_string = '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'
        time.sleep(3)

        while self.number_of_images > count and missed_count < self.max_missed:
            if indx_2 > 0:
                try:
                    imgurl = self.driver.find_element(
                        By.XPATH, search_string % (indx_1, indx_2 + 1)
                    )
                    imgurl.click()
                    indx_2 = indx_2 + 1
                    missed_count = 0
                except Exception:
                    try:
                        imgurl = self.driver.find_element(
                            By.XPATH, search_string % (indx_1 + 1, 1)
                        )
                        imgurl.click()
                        indx_2 = 1
                        indx_1 = indx_1 + 1
                    except:
                        indx_2 = indx_2 + 1
                        missed_count = missed_count + 1
            else:
                try:
                    imgurl = self.driver.find_element(
                        By.XPATH, search_string % (indx_1 + 1)
                    )
                    imgurl.click()
                    missed_count = 0
                    indx_1 = indx_1 + 1
                except Exception:
                    try:
                        imgurl = self.driver.find_element(
                            By.XPATH,
                            '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'
                            % (indx_1, indx_2 + 1),
                        )
                        imgurl.click()
                        missed_count = 0
                        indx_2 = indx_2 + 1
                        search_string = (
                            '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'
                        )
                    except Exception:
                        indx_1 = indx_1 + 1
                        missed_count = missed_count + 1

            try:
                time.sleep(1)
                class_names = ["n3VNCb", "iPVvYb", "r48jcc", "pT0Scc"]
                images = [
                    self.driver.find_elements(By.CLASS_NAME, class_name)
                    for class_name in class_names
                    if len(self.driver.find_elements(By.CLASS_NAME, class_name)) != 0
                ][0]
                for image in images:
                    src_link = image.get_attribute("src")
                    if self.validate_src_link(src_link):
                        logger.info(f"{self.search_key} \t #{count} \t {src_link}")
                        image_urls.append(src_link)
                        count += 1
                        break
            except Exception:
                logger.info("Unable to get link")

            try:
                if count % 3 == 0:
                    self.driver.execute_script(
                        "window.scrollTo(0, " + str(indx_1 * 60) + ");"
                    )
                element = self.driver.find_element(By.CLASS_NAME, "mye4qd")
                element.click()
                logger.info("Loading next page")
                time.sleep(3)
            except Exception:
                time.sleep(1)

        self.driver.quit()
        logger.info("Google search ended")
        return image_urls

    def validate_src_link(self, src_link: str):
        if self.hash_url(src_link) in self.existing_files:
            logger.warn("Duplicate image")
            return 0

        if not ("http" in src_link) or ("encrypted" in src_link):
            return 0
        return 1

    @staticmethod
    def hash_url(url: str):
        url_encoded = url.encode('utf-8')

        hasher = hashlib.sha256()
        hasher.update(url_encoded)

        hash_bytes = hasher.digest()

        hash_hex = binascii.hexlify(hash_bytes).decode('utf-8')

        return hash_hex

    def save_images(self, image_urls):
        """
            This function takes in an array of image urls and save it into the given image path/directory.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls=["https://example_1.jpg","https://example_2.jpg"]
                google_image_scraper.save_images(image_urls)

        """
        logger.info("Saving image, please wait...")
        for idx, image_url in enumerate(image_urls):
            try:
                logger.info(f"Image url:{image_url}")
                image = requests.get(image_url, timeout=5)
                if image.status_code == 200:
                    self.save_image(
                        image, image_url, idx
                    )
            except Exception as e:
                logger.error("Download failed: ", e)
                pass
        logger.info("--------------------------------------------------")
        logger.info(
            "Downloads completed. Please note that some photos were not downloaded as they were not in the correct format (e.g. jpg, jpeg, png)"
        )

    def save_image(self, image, image_url, idx):
        with Image.open(io.BytesIO(image.content)) as image_from_web:
            try:
                filename = "%s.%s" % (self.hash_url(image_url), image_from_web.format.lower())

                image_path = os.path.join(self.image_path, filename)
                logger.info(
                    f"{self.search_key} \t {idx} \t Image saved at: {image_path}"
                )
                image_from_web.save(image_path)
            except OSError:
                rgb_im = image_from_web.convert("RGB")
                rgb_im.save(image_path)
            image_resolution = image_from_web.size

            if image_resolution is not None:
                if (
                        image_resolution[0] < self.min_resolution[0]
                        or image_resolution[1] < self.min_resolution[1]
                        or image_resolution[0] > self.max_resolution[0]
                        or image_resolution[1] > self.max_resolution[1]
                ):
                    image_from_web.close()
                    os.remove(image_path)

            image_from_web.close()
