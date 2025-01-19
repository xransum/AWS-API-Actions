"""Module to export the scraped data to different formats.

The data is serialized and saved in the following formats:
    - Text
    - JSON
    - CSV
    - XML

Each export format is handled by a separate function that takes in the
processed data (dictionaries of services and their associated categories/values)
and outputs it to the desired format. This allows the program to save the scraped
information in a variety of formats for further use or analysis.

Functions in this module:
    - text_exporter(data): Exports the data as a plain text file, with services
      and their categories listed in a human-readable format.
    - json_exporter(data): Serializes the data into JSON format and writes it to
      a .json file.
    - csv_exporter(data): Converts the data into CSV format and saves it as a
      .csv file.
    - xml_exporter(data): Converts the data into XML format and writes it to an
      .xml file.

Example Usage:
    # Import the exporter module
    from exporter import output_to_text, output_to_json, output_to_csv,
        output_to_xml

    # Sample data structure
    data = {
        "service_name_1": {
            "category_1": "value_1",
            "category_2": "value_2",
        },
        "service_name_2": {
            "category_1": "value_1",
            "category_2": "value_2",
        }
    }

    # Export data to different formats
    output_to_text(data)
    output_to_json(data)
    output_to_csv(data)
    output_to_xml(data)
"""

from typing import Dict, List


def write_to_file(file_path: str, contents: str) -> None:
    """Write the contents to a file.

    Args:
        file_path (str): The path to the file to write to.
        contents (str): The contents to write to the file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(contents)


def output_to_text(
    file_path: str, data: Dict[str, Dict[str, List[str]]]
) -> None:
    """Export the data as an plain text file.

    Args:
        file_path (str): The path to the file to write to.
        data (Dict[str, Dict[str, List[str]]]): The data to export
    """


def output_to_json(
    file_path: str, data: Dict[str, Dict[str, List[str]]]
) -> None:
    """Export the data as an json file.

    Args:
        file_path (str): The path to the file to write to.
        data (Dict[str, Dict[str, List[str]]]): The data to export
    """


def output_to_csv(file_path: str, data: Dict[str, Dict[str, List[str]]]) -> None:
    """Export the data as an csv file.

    Args:
        file_path (str): The path to the file to write to.
        data (Dict[str, Dict[str, List[str]]]): The data to export
    """


def output_to_xml(file_path: str, data: Dict[str, Dict[str, List[str]]]) -> None:
    """Export the data as an xml file.

    Args:
        file_path (str): The path to the file to write to.
        data (Dict[str, Dict[str, List[str]]]): The data to export
    """
