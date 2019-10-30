# DCLUTTER

Data cleaning.

## General

### About

Data cleansing or data cleaning is the process of detecting and correcting (or removing) corrupt or inaccurate 
data from a data set and refers to identifying incomplete, incorrect, inaccurate or irrelevant parts of the data
and then replacing, modifying, or deleting the dirty or coarse data. The inconsistencies detected and modified or 
removed may have been originally caused by user entry errors, by corruption in transmission or storage.

High-quality data needs to pass a set of quality criteria including:
- Validity
    - type constraints
    - range constraints
    - regular expresion patterns
    - cross field validation (like this and that cannot happen occur at the same time)
- Accuracy
- Completeness
- Consistency (like duplicated data points)
- Uniformity (the degree to which a data set is measured using the same units)

`dclutter` ensures *validity* and *uniformity*, removes duplicates (*consistency*) and can to some extent remedy
lack of *completeness*. However accuracy is very hard to achieve through data-cleansing in the
general case, because it requires having access to "the truth". The same goes for completeness as it is not
generally possible to back and capture data that was not initially recorded.     

### Getting started

Run the below command in a Python environment to install the latest release

```console
pip install dclutter
```

.. or upgrade existing installation

```console
pip install --upgrade dclutter
```

You can now import dclutter in your own scripts to create custom workflows etc.

```python
import dclutter
```

Take a look at the resources listed below to learn more.

### Resources

* [**Source**](https://github.com/equinor/simpos/data-cleansing)
* [**Issues**](https://github.com/equinor/simpos/issues)
* [**Changelog**](https://github.com/equinor/simpos/releases)
* [**Documentation**](https://github.com/equinor/simpos/blob/master/README.md)
<!---* [**Download**](https://app.packagr.app/packages/951d77bf-73e0-40dc-8d4a-e01a22916460/)--->

## Contribute

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Install Python version 3.6 or later from either https://www.python.org or https://www.anaconda.com.

### Clone the source code repository

At the desired location, run:

```git clone https://github.com/equinor/simpos.git```

Navigate to the 'data-cleansing' directory.

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
import dclutter
help(dclutter)
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