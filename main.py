from app.services.google.scrape import worker_thread

if __name__ == "__main__":
    search_keys = ["iPhone 7", "iPhone 8"]
    number_of_workers = 6
    worker_thread(search_key="samsung a71")

    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        try:
            executor.map(worker_thread, search_keys)
        except KeyboardInterrupt:
            logger.info("Finishing with KeyboardInterrupt")
        except Exception as e:
            logger.error("An error occurred", e)
