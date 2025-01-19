"""Functions to download, install, and manage the geckodriver binary."""

import os
import tarfile
import urllib.error
import urllib.request
import zipfile
from io import BytesIO

from aws_api_actions.logger import logger
from aws_api_actions.utilities import (
    get_compression_format,
    get_sys_arch,
    get_sys_platform,
    get_venv_path,
)


GECKODRIVER_REPOSITORY_URL = (
    "https://github.com/mozilla/geckodriver/releases/download/{version}"
    "/geckodriver-{version}-{platform}{architecture}.{compression}"
)
GECKODRIVER_REPOSITORY_LATEST_URL = (
    "https://github.com/mozilla/geckodriver/releases/latest"
)


def get_geckodriver_filename() -> str:
    """Returns the filename of the binary for the current platform.

    Args:
        None

    Returns:
        str: The filename of the binary for the current platform.
    """
    name = "geckodriver"
    if get_sys_platform() == "win":
        name += ".exe"

    return name


def get_geckodriver_binary_path() -> str:
    """Returns the path to the geckodriver binary.

    Returns:
        str: The path to the geckodriver binary.
    """
    venv_path = get_venv_path()
    geckodriver_filename = get_geckodriver_filename()
    geckodriver_path = os.path.join(venv_path, geckodriver_filename)
    return geckodriver_path


def get_latest_version_number() -> str:
    """Returns the latest version of the geckodriver binary.

    Args:
        None

    Returns:
        str: The latest version of the geckodriver binary.

    Raises:
        RuntimeError: If the download fails.
    """
    download_url = GECKODRIVER_REPOSITORY_LATEST_URL

    logger.info("Fetching latest geckodriver version from %s", download_url)

    try:
        req = urllib.request.urlopen(download_url)
        final_url = req.geturl()

    except urllib.error.HTTPError as err:
        logger.error("Failed to fetch latest geckodriver version: %s", err)
        raise RuntimeError("Failed to fetch latest geckodriver version") from err

    version: str = final_url.split("/")[-1]
    logger.info("Latest geckodriver version is %s", version)

    return version


def get_version_download_url(version: str) -> str:
    """Returns the download URL for the given version.

    Args:
        version (str): The version of the geckodriver binary.

    Returns:
        str: The download URL for the given version.
    """
    platform = get_sys_platform()
    architecture = get_sys_arch()
    compression = get_compression_format()

    return GECKODRIVER_REPOSITORY_URL.format(
        version=version,
        platform=platform,
        architecture=architecture,
        compression=compression,
    )


def is_geckodriver_installed() -> bool:
    """Checks whether the geckodriver binary is downloaded.

    Args:
        None

    Returns:
        bool: Whether the geckodriver binary is downloaded.
    """
    return os.path.exists(get_geckodriver_binary_path())


def uncompress_file(file: BytesIO, directory: str) -> None:
    """Uncompresses the given file to the given directory.

    Args:
        file (file): The file to uncompress.
        directory (str): The directory to uncompress the file to.

    Returns:
        None
    """
    platform = get_sys_platform()

    if platform == "win":
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(directory)
    else:
        tar = tarfile.open(fileobj=file, mode="r:gz")
        tar.extractall(directory)
        tar.close()


def make_executable(file_path: str) -> bool:
    """Makes the given file executable.

    Args:
        file_path (str): The path to the file to make executable.

    Returns:
        bool: Whether the file was successfully made executable.
    """
    try:
        os.chmod(file_path, 0o744)
    except OSError as err:
        logger.error("Failed to make binary executable: %s", err)
        return False

    return True


def install_geckodriver(force: bool = False) -> bool:
    """Downloads the latest geckodriver binary.

    Args:
        force (bool, optional): Whether to force the download. Defaults to False.

    Raises:
        urllib.error.URLError: If the download fails.
        RuntimeError: If the download fails.

    Returns:
        bool: Whether the download was successful.
    """
    geckodriver_binary_path = get_geckodriver_binary_path()
    binary_dir = os.path.dirname(geckodriver_binary_path)

    if is_geckodriver_installed() is True:
        logger.info("Geckodriver already installed %s", geckodriver_binary_path)

        if force is True:
            logger.debug(
                "Force flag specified, deleting existing geckodriver binary."
            )
            os.remove(geckodriver_binary_path)

        else:
            return True

    # Get the latest version number and download URL
    latest_version = get_latest_version_number()
    download_url = get_version_download_url(latest_version)

    # Download the latest geckodriver archive
    logger.info("Downloading latest geckodriver archive from %s", download_url)
    try:
        resp = urllib.request.urlopen(download_url)
        status_code = resp.getcode()
        if status_code != 200:
            raise urllib.error.URLError("Not Found")

    except urllib.error.URLError as err:
        raise RuntimeError(
            f"Failed to download geckodriver archive: {download_url}"
        ) from err

    # Read the downloaded file
    raw = resp.read()
    archive = BytesIO(raw)

    # Uncompress file to install dir
    logger.info("Decompressing downloaded archive to %s", binary_dir)
    try:
        uncompress_file(archive, binary_dir)
    except (tarfile.TarError, zipfile.BadZipFile) as err:
        logger.error("Failed to uncompress file: %s", err)
        return False

    # Create the install directory if it doesn't exist
    if os.path.exists(binary_dir) is False:
        logger.debug("Creating installation directory %s", binary_dir)
        os.makedirs(binary_dir)

    # Make the binary executable
    if make_executable(geckodriver_binary_path) is False:
        return False

    logger.info("Geckodriver installed successfully")

    return True
