from typing import List

import requests
from bs4 import BeautifulSoup

from aws_api_actions.constants import USER_AGENT
from aws_api_actions.geckodriver import is_geckodriver_installed
from aws_api_actions.logger import logger


if is_geckodriver_installed() is False:
    logger.warning(
        "Geckodriver is NOT installed. For 'aws_api_actions' to function properly, "
        "it must be installed. To install Geckodriver, run the 'gecko_install' "
        "command or import the 'aws_api_actions.geckodriver.install_geckodriver'"
        " function."
    )

# req = get_page("https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Welcome.html")
# page = get_soup(req)

# services_list = page.find("h6", string="Services")


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from aws_api_actions.geckodriver import (
    get_firefox_binary_path,
    get_geckodriver_binary_path,
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
    geckodriver_binary = get_geckodriver_binary_path()
    firefox_binary = get_firefox_binary_path()

    # Generate the webdriver
    driver: webdriver.Firefox = setup_webdriver(
        geckodriver_binary,
        firefox_binary,
        webdriver_options=[
            "--headless",
            "--disable-gpu",
            "--disable-extensions",
        ],
    )

    target = (
        "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Welcome.html"
    )

    # Load the target URL
    driver.get(target)
    source = driver.page_source
    driver.quit()

    print(source)


if __name__ == "__main__":
    main()
