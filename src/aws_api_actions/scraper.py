import os
from typing import List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# from selenium import webdriver
from seleniumwire import webdriver

from aws_api_actions.constants import USER_AGENT
from aws_api_actions.geckodriver import (
    get_geckodriver_binary_path,
    is_geckodriver_installed,
)
from aws_api_actions.logger import logger
from aws_api_actions.utilities import get_firefox_binary_path


if is_geckodriver_installed() is False:
    logger.warning(
        "Geckodriver is NOT installed. For 'aws_api_actions' to function properly, "
        "it must be installed. To install Geckodriver, run the 'gecko_install' "
        "command or import the 'aws_api_actions.geckodriver.install_geckodriver'"
        " function."
    )


def setup_webdriver(
    geckodriver_binary: str, firefox_binary: str, webdriver_options: List[str]
) -> webdriver.Firefox:
    """Generate a webdriver instance.

    Args:
        geckodriver_binary str: Path to Geckodriver binary.
        firefox_binarystr: Path to Firefox binary.
        webdriver_options List[str]: List of options to pass to the
            webdriver.

    Returns:
        webdriver.Firefox: A webdriver instance.
    """
    # Generate the webdriver
    service = Service(
        executable_path=geckodriver_binary,
        # log_path=gecko_logs,
    )
    options = webdriver.FirefoxOptions()
    for option in webdriver_options:
        options.add_argument(option)

    options.binary_location = firefox_binary
    driver = webdriver.Firefox(
        options=options,
        service=service,
    )
    return driver


def main() -> None:
    """Main function to setup the webdriver and load the target URL."""
    geckodriver_binary = get_geckodriver_binary_path()
    firefox_binary = get_firefox_binary_path()

    driver: webdriver.Firefox = setup_webdriver(
        geckodriver_binary,
        firefox_binary,
        webdriver_options=[
            "--headless",
            "--disable-gpu",
            "--disable-extensions",
        ],
    )

    full_url = (
        "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Welcome.html"
    )
    url_comps = urlparse(full_url)
    domain = url_comps.netloc

    driver.get(full_url)
    driver.fullscreen_window()
    driver.save_screenshot(
        os.path.join(
            os.path.dirname(
                os.path.abspath(
                    "abc" if "__file__" not in locals() else __file__
                )
            ),
            "screenshot.png",
        )
    )
    title = driver.title
    current_url = driver.current_url
    page_source = driver.page_source

    performance = driver.execute_script("return window.performance.timing")
    cookies = driver.get_cookies()
    downloadable_files = driver.get_downloadable_files()

    for request in driver.requests:
        if request.response:
            print(request.url, request.response.status_code)

    source = driver.page_source
    driver.quit()

    print(source)


if __name__ == "__main__":
    main()
