# About

This is the repository containing my thesis' code

The files containing my experiments come with the `script_` prefix. Each one contains a brief summary of the experiment
together with accuracy metrics of the trained model(s).


## IDE setup
I installed [Spyder](https://www.spyder-ide.org/). Then I used [PyEnv](https://github.com/pyenv/pyenv) to install [Miniconda](https://docs.anaconda.com/miniconda/).
I created a new Miniconda environment, installed [AutoGluon](https://auto.gluon.ai/stable/index.html) and configured Spyder to work with my Miniconda environment by following
the answer to '[How do I install Python packages to use withing Spyder if I downloaded Spyder from the standalon installers?](https://docs.spyder-ide.org/5/faq.html#using-spyder)'.

## Tests
I have covered data preprocessing with tests. To execute them, run the command `python ./utils/preprocessingtest.py`