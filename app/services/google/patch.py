import os
import urllib.request
import re
import zipfile
import stat
import json
import shutil
from sys import platform

from app.logger.logger import logger


def webdriver_executable():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        return "chromedriver"
    return "chromedriver.exe"


def download_latest_chromedriver(current_chrome_version=""):
    def get_platform_filename():
        filename = ""

        if platform == "linux" or platform == "linux2":
            filename += "linux64"
        elif platform == "darwin":
            filename += "mac-x64"
        elif platform == "win32":
            filename += "win32"

        return filename

    result = False
    try:
        url = "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"

        stream = urllib.request.urlopen(url)
        content = json.loads(stream.read().decode("utf-8"))

        if current_chrome_version != "":
            match = re.search(r"\d+", current_chrome_version)
            downloads = content["milestones"][match.group()]

        else:
            for milestone in content["milestones"]:
                downloads = content["milestones"][milestone]

        for download in downloads["downloads"]["chromedriver"]:
            if download["platform"] == get_platform_filename():
                driver_url = download["url"]

        logger.info(
            "downloading chromedriver ver: %s: %s"
            % (current_chrome_version, driver_url)
        )
        file_name = driver_url.split("/")[-1]
        app_path = os.getcwd()
        chromedriver_path = os.path.normpath(
            os.path.join(app_path, "webdriver", webdriver_executable())
        )
        file_path = os.path.normpath(os.path.join(app_path, "webdriver", file_name))
        urllib.request.urlretrieve(driver_url, file_path)

        webdriver_path = os.path.normpath(os.path.join(app_path, "webdriver"))
        with zipfile.ZipFile(file_path, "r") as zip_file:
            for member in zip_file.namelist():
                filename = os.path.basename(member)
                if not filename:
                    continue
                source = zip_file.open(member)
                target = open(os.path.join(webdriver_path, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)

        st = os.stat(chromedriver_path)
        os.chmod(chromedriver_path, st.st_mode | stat.S_IEXEC)
        logger.info("Latest chromedriver downloaded")

        os.remove(file_path)
        result = True
    except Exception as e:
        logger.error(e)
        logger.warn(
            "Unable to download lastest chromedriver. the system will use the local version instead."
        )

    return result
