# AWS-API-Actions

Compiles and generates datasets for the AWS API actions for all services.

## Installation

Clone the repository:

```bash
git clone https://github.com/xransum/AWS-API-Actions.git
```

Install the dependencies:

```bash
poetry install
```

Install the GeckoDriver for Selenium, currently the only method to do so is to
run the packages installer command:

```bash
poetry run gecko_install
```

or you can install by running the function directly:

```bash
poetry run python
```

```python
>>> from aws_api_actions import gecko_installer
>>> gecko_installer()
```

## Contributing

Contributions are very welcome. To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license], _AWS-API-Actions_ is
free and open source software.

## Issues

If you encounter any problems, please [file an issue] along with a detailed
description.

## Credits

This project was built off of the sweat and tears of the the bad actors it was
built to fight.

<!-- github-only -->

[contributor guide]:
    https://github.com/xransum/AWS-API-Actions/blob/main/CONTRIBUTING.md
[file an issue]: https://github.com/xransum/AWS-API-Actions/issues
[license]: https://github.com/xransum/AWS-API-Actions/blob/main/LICENSE
