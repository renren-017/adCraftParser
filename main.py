import concurrent.futures

from scrapers.google.main import worker_thread

if __name__ == "__main__":
    search_keys = list({"iPhone 7", "iPhone 8"})
    number_of_workers = 6

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=number_of_workers
    ) as executor:
        executor.map(worker_thread, search_keys)
