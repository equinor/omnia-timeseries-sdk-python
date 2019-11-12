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

... and get to work. [Here](https://github.com/equinor/omnia-timeseries-sdk-python/examples/introduction.ipynb) 
is an introduction. 

Take a look at the resources listed below to learn more.

### Resources

* [**Source**](https://github.com/equinor/omnia-timeseries-sdk-python)
* [**Issues**](https://github.com/equinor/omnia-timeseries-sdk-python/issues)
* [**Changelog**](https://github.com/equinor/omnia-timeseries-sdk-python/releases)
* [**Documentation**](https://github.com/equinor/omnia-timeseries-sdk-python/blob/master/README.md)
* [**Download**]()
* [**Examples**](https://github.com/equinor/omnia-timeseries-sdk-python/examples)

## Contribute

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Install Python version 3.7 or later from either https://www.python.org or https://www.anaconda.com.

### Clone the source code repository

At the desired location, run:

```git clone https://github.com/equinor/simpos.git```

Navigate to the 'omnia-timeseries-sdk-python' directory.

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

The automated tests are run using [Tox](https://tox.readthedocs.io/en/latest/).

```console
tox
```

The test automation is configured in [tox.ini](tox.ini).

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
Wait for it...
<!---
Packaging, unit testing and deployment to [Packagr](https://app.packagr.app) is automated using
[Travis-CI](https://travis-ci.com).
--->
### Versioning

We apply the "major.minor.micro" versioning scheme defined in [PEP 440](https://www.python.org/dev/peps/pep-0440/).

<!---
We cut a new version by applying a Git tag like `3.0.1` at the desired commit and then
[setuptools_scm](https://github.com/pypa/setuptools_scm/#setup-py-usage) takes care of the rest. For the versions
available, see the [tags on this repository](https://github.com/equinor/simpos/tags).
--->

## Authors

* **Per Voie** - [tovop](https://github.com/tovop)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.