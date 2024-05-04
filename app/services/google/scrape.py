import os

from app.services.google.service import GoogleImageScraper


__all__ = ['search_google']


def search_google(search_key):

    image_scraper = GoogleImageScraper(
        search_key=search_key,
    )

    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls)

    del image_scraper
