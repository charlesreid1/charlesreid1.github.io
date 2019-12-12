title: Automatically Generating requirements.txt for Python Projects
Date: 2019-12-12 12:12
Category: Python
Tags: python, pip, version control, make, makefile
status: draft


Quick post to demonstrate a way to automatically generate a `requirements.txt` file for your
Python project.

Start by creating a `requirements.txt.in`, which should look like a normal `requirements.txt` file,
listing software packages for pip to install (and optionally version information - but version information
does not _need_ to be specified).

Example `requirements.txt.in`:

```
numpy
pandas > 0.22
sphinx
```

Next, we use the `requirements.txt.in` file to install the latest versions of each software package (and all
dependent software packages) into a virtual environment.

From that virtual environment, we can use `pip freeze` to output the names of each software package installed in
the virtual environment, along with its exact version. This can be used to make a `requirements.txt` file.

Performing the above steps requires multiple steps, but we have a nice Makefile rule that can be dropped into
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

Summary:

* The first two lines create a virtual environment at `.requirements-env/`

* The next two lines run `pip install`, first on `requirements.txt` (the existing version), then
  `requirements.txt.in` (which installs/updates any software packages in `requirements.txt.in`)

* A comment is added to the top of the `requirements.txt` file to help give users a hint about
  where to update software requirements.

* The `pip freeze` command is used to create a `requirements.txt` file from the current virtual
  environment

Extending to requirements, requirements-dev, requirements-docs

What problem does this solve?
