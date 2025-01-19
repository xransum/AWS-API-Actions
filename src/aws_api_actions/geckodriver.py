import os
import sys
import tarfile
import urllib.error
import urllib.request
import zipfile
from glob import glob
from io import BytesIO
from typing import Optional

from aws_api_actions.logger import logger


GECKODRIVER_REPOSITORY_URL = (
    "https://github.com/mozilla/geckodriver/releases/download/{version}"
    "/geckodriver-{version}-{platform}{architecture}.{compression}"
)
GECKODRIVER_REPOSITORY_LATEST_URL = (
    "https://github.com/mozilla/geckodriver/releases/latest"
)


def get_sys_arch() -> str:
    """Returns the architecture of the current OS.

    Args:
        None

    Returns:
        str: The architecture of the current OS.
    """
    arch = "32"
    if sys.maxsize > 2**32:
        arch = "64"
    return arch


def get_sys_platform() -> str:
    """Returns the platform of the current OS.

    Args:
        None

    Returns:
        str: The platform of the current OS.
    """
    platform = "linux"

    if sys.platform.startswith("win"):
        platform = "win"

    elif sys.platform.startswith("darwin"):
        platform = "macos"

    return platform


def get_sys_name() -> str:
    """Returns the platform and architecture of the current OS.

    Args:
        None

    Returns:
        str: The platform and architecture of the current OS.
    """
    return "{platform}{architecture}".format(
        platform=get_sys_platform(), architecture=get_sys_arch()
    )


def get_compression_format() -> str:
    """Returns the compression format for the current platform.

    Args:
        None

    Returns:
        str: The compression format for the current platform.
    """
    comp = "tar.gz"
    if get_sys_platform() == "win":
        comp = "zip"

    return comp


def get_variable_separator() -> str:
    """Returns the separator for the PATH variable.

    Args:
        None

    Returns:
        str: The separator for the PATH variable.
    """
    sep = ":"
    if get_sys_platform() == "win":
        sep = ";"

    return sep


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


def get_venv_path() -> str:
    """Get the path to the virtual environment.

    Returns:
        str: The path to the virtual environment.
    """
    venv_path = os.path.dirname(sys.executable)
    return venv_path


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


# TODO: Add argument to specify the relative or absolute path to the binary.
def get_firefox_binary_path() -> str:
    """Returns the path to the firefox binary.

    Args:
        None

    Returns:
        str: The path to the firefox binary.
    """
    firefox_install_dir = ""
    if get_sys_platform() == "win":
        win_semi_paths = [
            "%s:\\Program Files\\Mozilla Firefox",
            "%s:\\Program Files (x86)\\Mozilla Firefox",
            "%s:\\Program Files\\Mozilla Thunderbird",
            "%s:\\Program Files\\mozilla.org\\Mozilla",
            "%s:\\Program Files\\mozilla.org\\SeaMonkey",
            "%s:\\Program Files\\SeaMonkey",
        ]
        # Add all letters of the alphabet to the paths
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            # Add all paths with the letter
            for semi_path in win_semi_paths:
                # If the drive exists, add the path
                if os.path.exists(f"{letter}:"):
                    path = os.path.join(semi_path % letter, "firefox*.exe")
                    for bins in glob(path):
                        if "firefox" in bins.lower():
                            firefox_install_dir = bins
                            break
                    if firefox_install_dir is not None:
                        break

    elif get_sys_platform() == "linux":
        linux_semi_paths = [
            "/usr/lib/",
            "/usr/lib64/",
            "/usr/lib/firefox/",
            "/usr/lib64/firefox/",
            "/usr/lib/firefox*/",
            "/usr/lib64/firefox*/",
        ]
        # Add all paths with the letter
        for semi_path in linux_semi_paths:
            # If the drive exists, add the path
            if os.path.exists(semi_path):
                path = os.path.join(semi_path, "firefox")
                for bins in glob(path):
                    if "firefox" in bins.lower():
                        firefox_install_dir = bins
                        break
                if firefox_install_dir is not None:
                    break

    elif get_sys_platform() == "macos":
        mac_semi_paths = [
            "/Applications/Firefox.app/Contents/MacOS/firefox",
        ]
        # Add all paths with the letter
        for semi_path in mac_semi_paths:
            # If the drive exists, add the path
            if os.path.exists(semi_path):
                path = os.path.join(semi_path, "firefox")
                for bins in glob(path):
                    if "firefox" in bins.lower():
                        firefox_install_dir = bins
                        break
                if firefox_install_dir is not None:
                    break

    return firefox_install_dir


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
    except Exception as err:
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
        logger.info("Geckodriver already installed %s" % geckodriver_binary_path)

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

    except urllib.error.URLError:
        raise RuntimeError(
            f"Failed to download geckodriver archive: {download_url}"
        )

    # Read the downloaded file
    raw = resp.read()
    archive = BytesIO(raw)

    # Uncompress file to install dir
    logger.info("Decompressing downloaded archive to %s" % binary_dir)
    try:
        uncompress_file(archive, binary_dir)
    except Exception as err:
        logger.error("Failed to uncompress file: %s", err)
        return False

    # Create the install directory if it doesn't exist
    if os.path.exists(binary_dir) is False:
        logger.debug("Creating installation directory %s" % binary_dir)
        os.makedirs(binary_dir)

    # Make the binary executable
    if make_executable(geckodriver_binary_path) is False:
        return False

    logger.info("Geckodriver installed successfully")

    return True
