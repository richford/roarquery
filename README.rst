Roarquery
=========

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/roarquery.svg
   :target: https://pypi.org/project/roarquery/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/roarquery.svg
   :target: https://pypi.org/project/roarquery/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/roarquery
   :target: https://pypi.org/project/roarquery
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/roarquery
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/roarquery/latest.svg?label=Read%20the%20Docs
   :target: https://roarquery.readthedocs.io/
   :alt: Read the documentation at https://roarquery.readthedocs.io/
.. |Tests| image:: https://github.com/richford/roarquery/workflows/Tests/badge.svg
   :target: https://github.com/richford/roarquery/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/richford/roarquery/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/richford/roarquery
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features
--------

* Query ROAR runs
* Download ROAR runs and trials
* List ROAR Firestore collections


Requirements
------------

* Python 3.8+
* `fuego`_


Installation
------------

You can install *Roarquery* via pip_ from PyPI_:

.. code:: console

   $ pip install roarquery

*Roarquery* also requires you to install *fuego*, a command line firestore client.
Please see the `fuego documentation`_ for installation instructions.


Usage
-----

Authentication
~~~~~~~~~~~~~~

Before you can use *Roarquery*, you need to provide authentication details:

1. Retrieve or generate a Service Account key file.

   a. go to your `Firebase project console`_,
   b. go to "Project settings" (in the little gear menu next to "Project Overview"),
   c. click on the "Service accounts" tab,
   d. click on the "Generate new private key" button.

2. Save this file to somewhere on your computer. For example, presuming the previous commands downloaded a file to "$HOME/downloads/private_key.json"

   .. code:: bash

      mv "$HOME/downloads/private_key.json" "$HOME/.firebaseconfig/private_key.json"

3. Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to point to this file.

   .. code:: bash

      export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.firebaseconfig/private_key.json"

   or better yet, set this environment variable permanently in your shell configuration file.

   .. code:: bash

      echo "export GOOGLE_APPLICATION_CREDENTIALS=\"$HOME/.firebaseconfig/private_key.json\"" >> ~/.zshrc


Command-line Usage
~~~~~~~~~~~~~~~~~~

Please see the `Command-line Reference <Usage_>`_ for details.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*Roarquery* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _authentication_instructions:
.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/richford/roarquery/issues
.. _Firebase project console: https://console.firebase.google.com
.. _fuego: https://sgarciac.github.io/fuego/
.. _fuego documentation: https://sgarciac.github.io/fuego/#installation
.. _service account credentials: https://sgarciac.github.io/fuego/#authentication
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://roarquery.readthedocs.io/en/latest/usage.html
