title: Automatically Generating Up-To-Date requirements.txt for Python Projects
Date: 2019-12-12 12:12
Category: Python
Tags: python, pip, version control, make, makefile

## Summary

In this post, we cover a pattern for automatically generating a `requirements.txt` file that has the latest
compatible versions of required software, and that specifies the full and exact version of each package to
make the Python environment reproducible.

This will turn a requirements input file (called `requirements.txt.in` for example) that looks like

```
numpy
```

into a requirements file that specifies the exact version of `numpy` and all dependencies, like

```
numpy==1.18.1
```

By the end of this post, you'll be able to do this to refresh and update the versions of all the software your
project depends on:

```
make requirements.txt
```

**All of this code comes from the Human Cell Atlas [data-store](https://github.com/HumanCellAtlas/data-store)
project!**

## What is requirements.txt?

When developing a Python project, the `requirements.txt` file is a plain text file that contains a list of
Python software packages that need to be installed for the current Python software package to work. The software
can be installed using the command

```
pip install -r requirements.txt
```

For example, if a package `foobar` has `import numpy` at the top of a Python file in the project, the `numpy` package
must be installed before importing `foobar`. In this case, the `requirements.txt` could just contain

```
numpy
```

or it could specify a particular version of numpy, or a minimum version of numpy:

```
numpy >= 1.10
```

Start by creating a `requirements.txt.in`, which should look like a normal `requirements.txt` file,
listing software packages for pip to install (and optionally version information - but version information
does not _need_ to be specified).

This file is a looser set of specifications of software versions.

Example `requirements.txt.in`:

```
numpy
pandas > 0.22
sphinx
```

## Converting requirements.txt.in to requirements.txt

Next, we use the `requirements.txt.in` file to install the latest versions of each software package (and all
dependent software packages) into a virtual environment.

From that virtual environment, we can use `pip freeze` to output the names of each software package installed in
the virtual environment, along with its exact version. This can be used to make a `requirements.txt` file.

The manual steps are

```
virtualenv -p $(which python3) venv
venv/bin/pip install -r requirements.txt
venv/bin/pip install -r requirements.txt.in
venv/bin/pip freeze >> requirements.txt
rm -fr venv
```

Using pip freeze means the resulting `results.txt` contains detailed version numbers:

```
alabaster==0.7.12
Babel==2.7.0
certifi==2019.11.28
chardet==3.0.4
docutils==0.15.2
idna==2.8
imagesize==1.1.0
Jinja2==2.10.3
MarkupSafe==1.1.1
numpy==1.17.4
packaging==19.2
pandas==0.25.3
Pygments==2.5.2
pyparsing==2.4.5
python-dateutil==2.8.1
pytz==2019.3
requests==2.22.0
six==1.13.0
snowballstemmer==2.0.0
Sphinx==2.2.2
sphinxcontrib-applehelp==1.0.1
sphinxcontrib-devhelp==1.0.1
sphinxcontrib-htmlhelp==1.0.2
sphinxcontrib-jsmath==1.0.1
sphinxcontrib-qthelp==1.0.2
sphinxcontrib-serializinghtml==1.1.3
urllib3==1.25.7
```

This is automated with a make rule next.

## Automating the step with a make rule

We have a nice Makefile rule that can be dropped into
any Makefile that allows users to run

```
make requirements.txt
```

and it will use `requirements.txt.in`, perform the above steps, and output an updated `requirements.txt` with the
latest compatible versions of software.

Here is the Makefile rule:

```make
requirements.txt: %.txt : %.txt.in
	[ ! -e .requirements-env ] || exit 1
	virtualenv -p $(shell which python3) .$<-env
	.$<-env/bin/pip install -r $@
	.$<-env/bin/pip install -r $<
	echo "# You should not edit this file directly.  Instead, you should edit $<." >| $@
	.$<-env/bin/pip freeze >> $@
	rm -rf .$<-env
```

Summary of the make rule:

* The first two lines create a virtual environment at `.requirements-env/`

* The next two lines run `pip install`, first on `requirements.txt` (the existing version), then
  `requirements.txt.in` (which installs/updates any software packages in `requirements.txt.in`)

* A comment is added to the top of the `requirements.txt` file to help give users a hint about
  where to update software requirements.

* The `pip freeze` command is used to create a `requirements.txt` file from the current virtual
  environment

## Refreshing requirements

To update the requirements, update the `requirements.txt` with these manual steps:

```
refresh_all_requirements:
    @cat /dev/null > requirements.txt
	@if [ $$(uname -s) == "Darwin" ]; then sleep 1; fi  # this is require because Darwin HFS+ only has second-resolution for timestamps.
	@touch requirements.txt.in
	@$(MAKE) requirements.txt
```

Now `requirements.txt` can be updated with

```
make refresh_all_requirements
```

This can be done periodically, and the new `requirements.txt` updated in the version control system.
