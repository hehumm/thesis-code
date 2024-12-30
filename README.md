# About

This is the repository containing my thesis' code

## Environment setup
It's recommended to use a separate Python environment. For that I used [Miniconda](https://docs.anaconda.com/miniconda/).
Using Miniconda/Anaconda is not required but in that case some additional packages might have to be downloaded manually.

Running the scripts requires the installation of
* [Autogluon](https://auto.gluon.ai/stable/install.html)
* [MLForecast](https://nixtlaverse.nixtla.io/mlforecast/index.html)
* [SKForecast](https://skforecast.org/0.14.0/index.html)

Generating the results also requires
* [Matplotlib](https://matplotlib.org/stable/) for plotting (it gets installed already when installing Autogluon)
* [Openpyxl](https://anaconda.org/conda-forge/openpyxl) for generating Excel tables with accuracy metrics' scores

P.s: I downloaded Autogluon (version 1.2.0) and MLForecast (version 1.0.0) from [Conda-forge](https://conda-forge.org/) and SKForecast (version 0.14.0)
from [Pip](https://pypi.org/project/pip/). While it is generally not recommended to download packages from different sources, unfortunately SKForecast 
was not available in Conda-forge as of December 2024. But fortunately it seemed to work without any noticeable issues.

## IDE setup (optional)
I installed [Spyder](https://www.spyder-ide.org/). I configured Spyder to work with my Miniconda environment by following
the answer to '[How do I install Python packages to use withing Spyder if I downloaded Spyder from the standalon installers?](https://docs.spyder-ide.org/5/faq.html#using-spyder)'.
