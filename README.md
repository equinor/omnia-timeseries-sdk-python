# OMNIA Timeseries SDK for Python

Python software developer kit for the Omnia Timeseries API.

## General

### About

This is the Python SDK for developers and data scientists working with Omnia Timeseries. The package integrates with 
pandas to help you work easily and efficiently with the data.

### Getting started

Run the below command in a Python environment to install the latest release

```console
pip install omnia_timeseries_sdk
```

.. or upgrade existing installation

```console
pip install --upgrade omnia_timeseries_sdk
```

To access Omnia you have to set the following environmental variables. The values are provided by the Omnia administrators.
```console
set omniaResourceId="omnia-resource-id"
set omniaClientId="your-client-id"
set omniaClientSecret="very-very-secret-shared-key"
```

Import the Omnia client in your own scripts...

```python
from omnia_timeseries_sdk import OmniaClient
```

... and get to work. [Here](https://github.com/equinor/omnia-timeseries-sdk-python/blob/master/examples/introduction.ipynb) 
is an introduction. 

Take a look at the resources listed below to learn more.

### Resources

* [**Source**](https://github.com/equinor/omnia-timeseries-sdk-python)
* [**Issues**](https://github.com/equinor/omnia-timeseries-sdk-python/issues)
* [**Changelog**](https://github.com/equinor/omnia-timeseries-sdk-python/releases)
* [**Documentation**](https://github.com/equinor/omnia-timeseries-sdk-python/blob/master/README.md)
* [**Download**](https://pypi.org/project/omnia-timeseries-sdk/)
* [**Examples**](https://github.com/equinor/omnia-timeseries-sdk-python/blob/master/examples/)

## Contribute

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Install Python version 3.7 or later from either https://www.python.org or https://www.anaconda.com.

### Clone the source code repository

At the desired location, run:

```git clone https://github.com/equinor/omnia-timeseries-sdk-python.git```

### Installing

To get the development environment running:

... create an isolated Python environment and activate it,

```console
python -m venv /path/to/new/virtual/environment

/path/to/new/virtual/environment/Scripts/activate
```

... install the dev dependencies in [requirements.txt](requirements.txt),

```console
pip install -r requirements.txt
```

.. and install the package in development mode.

```console
python setup.py develop
```

You should now be able to import the package in the Python console,

```python
import omnia_timeseries_sdk
help(omnia_timeseries_sdk)
```

### Running the tests

We apply the [unittest](https://docs.python.org/3/library/unittest.html#module-unittest) and 
[pyteset](https://docs.pytest.org/en/latest/contents.html) frameworks.

Run the tests and check test coverage by
```console
pytest --cov=omnia_timeseries_sdk --cov-report term-missing tests/
```

### Building the package

Build tarball and wheel distributions by:

```console
python setup.py sdist bdist_wheel
```

The distribution file names adhere to the [PEP 0427](https://www.python.org/dev/peps/pep-0427/#file-name-convention)
convention `{distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl`.

<!---
### Building the documentation

The html documentation is build using [Sphinx](http://www.sphinx-doc.org/en/master)

```console
sphinx-build -b html docs\source docs\_build
```
--->

### Deployment

The package [releases](https://github.com/equinor/omnia-timeseries-sdk-python/releases) are deployed 
to [PyPi](https://pypi.org/project/omnia-timeseries-sdk/).

We use GitHub Actions to automate the build and deployment (CI-CD).

### Versioning

We apply the "major.minor.micro" versioning scheme defined in [PEP 440](https://www.python.org/dev/peps/pep-0440/).

We cut a new version by applying a Git tag like `0.1.0` at the desired commit and then
[setuptools_scm](https://github.com/pypa/setuptools_scm/#setup-py-usage) takes care of the rest at build time.
See the [tags on this repository](https://github.com/equinor/omnia-timeseries-sdk-python/tags).

## Authors

* **Per Voie** - [tovop](https://github.com/tovop)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
