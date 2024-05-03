import os
from scrapers.google.GoogleImageScraper import GoogleImageScraper
from scrapers.google.patch import webdriver_executable


def worker_thread(search_key):
    image_scraper = GoogleImageScraper(
        search_key=search_key,
        webdriver_path=os.path.normpath(
            os.path.join(os.getcwd(), "webdriver", webdriver_executable())
        ),
        image_path=os.path.normpath(os.path.join(os.getcwd(), "data")),
        number_of_images=50,
        headless=True,
        min_resolution=(0, 0),
        max_resolution=(9999, 9999),
        max_missed=10,
    )
    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls)

    del image_scraper
