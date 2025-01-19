"""Module provides utility functions for system information and paths."""

import os
import sys
from glob import glob


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
    return f"{get_sys_platform()}{get_sys_arch()}"


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


def get_venv_path() -> str:
    """Get the path to the virtual environment.

    Returns:
        str: The path to the virtual environment.
    """
    venv_path = os.path.dirname(sys.executable)
    return venv_path


# TODO: Need to add a function for detecting the Chrome binary path.
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
