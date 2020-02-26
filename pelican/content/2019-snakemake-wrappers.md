Title: Building Snakemake Command Line Wrappers for Workflows
Date: 2019-01-21 22:00
Category: Snakemake
Tags: python, bioinformatics, workflows, pipelines, snakemake, travis

**NOTE:** These ideas are implemented in the repository
[charlesreid1/2019-snakemake-cli](https://github.com/charlesreid/2019-snakemake-cli).

[TOC]

# Basic Idea: Wrapping Snakemake API Calls

## 2018-snakemake-cli

This blog post covers the implementation of an idea
that was originally explored in a blog post from 
Titus Brown, [Pydoit, snakemake, and workflows-as-applications](http://ivory.idyll.org/blog/2018-workflows-applications.html).

That blog post implemented a basic command line
wrapper around the Snakemake API to demonstrate
how a Snakemake workflow could be turned into
an executable.

Relevant code is in [ctb/2018-snakemake-cli](https://github.com/ctb/2018-snakemake-cli),
but the basic idea is to implement a command line
utility that takes two orthogonal sets of inputs:
a workflow configuration file, and a parameter set.

```text
./run <workflow-config> <workflow-params>
```

The [run script](https://github.com/ctb/2018-snakemake-cli/blob/master/run)
is a Python executable file that parses arguments
from the user.

Here is the main entrypoint of `run`:

```python
#! /usr/bin/env python
"""
Execution script for snakemake workflows.
"""
import argparse
import os.path
import snakemake
import sys
import pprint
import json

thisdir = os.path.abspath(os.path.dirname(__file__))

def main(args):
    # 
    # ...see below...
    #

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run snakemake workflows', usage='''run <workflow> <parameters> [<target>]
Run snakemake workflows, using the given workflow name & parameters file.
''')

    parser.add_argument('workflowfile')
    parser.add_argument('paramsfile')
    parser.add_argument('-n', '--dry-run', action='store_true')
    args = parser.parse_args()

    sys.exit(main(args))
```

The `main()` method uses the `os` module to look for
the Snakefile, the config file, and the params file,
then makes a call to the Snakemake API:

```python
def main(args):
    #
    # ...find the snakefile...
    # ...find the config file...
    # ...find the params file...
    # 

    target = workflow_info['workflow_target']
    config = dict()

    print('--------')
    print('details!')
    print('\tsnakefile: {}'.format(snakefile))
    print('\tconfig: {}'.format(workflowfile))
    print('\tparams: {}'.format(paramsfile))
    print('\ttarget: {}'.format(target))
    print('--------')

    # run!!
    status = snakemake.snakemake(snakefile, 
                                 configfile=paramsfile,
                                 targets=[target], 
                                 printshellcmds=True,
                                 dryrun=args.dry_run, 
                                 config=config)

    if status: # translate "success" into shell exit code of 0
       return 0
    return 1
```

This call uses the provided parameters file to set
the Snakemake configuration dictionary, but this can
be overridden with the `config` dictionary.
Additional argparser flags can be added, and the
`config` dictionary contents modified based on
the flags.

## 2019-snakemake-cli

We wanted to take this demo a step further, and add
a few things to it:

- Bundle the Snakefile and command line utility as an
  installable Python package with a `setup.py`

- Implement Travis CI tests of the Snakemake workflow.

We implemented a bundled Snakemake workflow as a 
command line tool called `bananas`.


# Turning Executables into Packages

We began with an executable script `run` and wished
to turn it into an installable command line utility
called `bananas`.

To do this, we moved the contents of `run` into 
a new file `command.py` in a new Python module 
called `cli`:

```text
cli/
├── Snakefile
├── __init__.py
└── command.py
```

The `Snakefile` will contain the workflow. Here is the
very simple workflow from [ctb/2018-snakemake-cli](https://github.com/ctb/2018-snakemake-cli).
The named rules are specified by the workflow configuration
file, while the parameters in `{}` are provided through
the parameters file (or via command line flags).

`cli/Snakefile`:

```text
name = config['name']

rule rulename1:
     input:
        "hello.txt"

rule target1:
     output:
        "hello.txt"
     shell:
        "echo hello {name} > {output}"

rule target2:
     output:
        "goodbye.txt"
     shell:
        "echo goodbye {name} > {output}"
```

**NOTE:** In this case we are bundling the Snakefile
with the command line wrapper, and writing the command
line wrapper to expect the Snakefile to be in the package.
But we can modify the command line wrapper function
(below) to look for the Snakefile in a local directory,
allowing the user to provide Snakefiles and workflows
to the command line wrapper.

The `__init__.py` file sets two important parameters:
the name of the command line utility, and the version
number:

`cli/__init__.py`:

```python
_program = "bananas"
__version__ = "0.1.0"
```

The contents of `command.py` are similar to `run` and
basically control how the command line utility runs:

`cli/command.py`:

```python
"""
Command line interface driver for snakemake workflows
"""
import argparse
import os.path
import snakemake
import sys
import pprint
import json

from . import _program


thisdir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.join(thisdir,'..')
cwd = os.getcwd()

def main(sysargs = sys.argv[1:]):

    parser = argparse.ArgumentParser(prog = _program, description='bananas: run snakemake workflows', usage='''bananas <workflow> <parameters> [<target>]

bananas: run snakemake workflows, using the given workflow name & parameters file.

''')

    parser.add_argument('workflowfile')
    parser.add_argument('paramsfile')
    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument('-f', '--force', action='store_true')
    args = parser.parse_args(sysargs)

    # ...find the Snakefile...
    # ...find the config file...
    # ...find the params file...

    target = workflow_info['workflow_target']
    config = dict()

    print('--------')
    print('details!')
    print('\tsnakefile: {}'.format(snakefile))
    print('\tconfig: {}'.format(workflowfile))
    print('\tparams: {}'.format(paramsfile))
    print('\ttarget: {}'.format(target))
    print('--------')

    # run bananas!!
    status = snakemake.snakemake(snakefile, configfile=paramsfile,
                                 targets=[target], printshellcmds=True,
                                 dryrun=args.dry_run, forceall=args.force,
                                 config=config)

    if status: # translate "success" into shell exit code of 0
       return 0
    return 1


if __name__ == '__main__':
    main()
```

The last component here is to make the function
in `cli/command.py` the entrypoint of a command line
utility called `bananas`, which can be done via
`setup.py`. This will put the executable `bananas`
in the Python binaries folder when the package is
installed.

`setup.py`:

```python
from setuptools import setup, find_packages
import glob
import os

with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if not x.startswith("#")]

# Note: the _program variable is set in __init__.py.
# it determines the name of the package/final command line tool.
from cli import __version__, _program

setup(name='bananas',
      version=__version__,
      packages=['cli'],
      test_suite='pytest.collector',
      tests_require=['pytest'],
      description='bananas command line interface',
      url='https://charlesreid1.github.io/2019-snakemake-cli',
      author='@charlesreid1',
      author_email='cmreid@ucdavis.edu',
      license='MIT',
      entry_points="""
      [console_scripts]
      {program} = cli.command:main
      """.format(program = _program),
      install_requires=required,
      include_package_data=True,
      keywords=[],
      zip_safe=False)
```

First, we grab the variables from `__init__.py`:

```python
from cli import __version__, _program
```

Next we specify where our package lives, the `cli` directory:

```python
setup(name='bananas',
        ...
        packages=['cli'],
```

and finally, we specify that we want to build a command line 
interface, with the entrypoint being the `main()` method of the
`cli/command.py` file using `entry_points`:

```python
setup(name='bananas',
        ...
        entry_points="""
[console_scripts]
{program} = cli.command:main
      """.format(program = _program),
``` 


# End Result: Using bananas

The end result is a command line utility that bundles a
Snakemake workflow. The repository contains some tests,
so let's run through the quick start installation and
run the tests.

## Quick Start: Installing

Start by setting up a virtual environment:

```bash
virtualenv vp
source vp/bin/activate
```

Install required components, then install the package:

```bash
pip install -r requirements.txt
python setup.py build install
```

Now you should see `bananas` on your path:

```text
which bananas
```

## Quick Start: Running Tests

```text
pytest
```

## Quick Start: Running Examples

Change to the `test/` directory and run tests with
the example config and param files.

```text
cd test
```

Run the hello workflow with Amy params:

```text
rm -f hello.txt
bananas workflow-hello params-amy
```

Run the hello workflow with Beth params:

```text
rm -f hello.txt
bananas workflow-hello params-beth
```

Run the goodbye workflow with Beth params:

```text
rm -f goodbye.txt
bananas workflow-goodbye params-beth
```


# Adding Travis CI Tests

To test or workflow, we break down the necessary tasks:

- Use a Python environment
- Install our requirements (snakemake)
- Install bananas with setup.py
- Run pytest

This is an easy Travis file to write, following the
[Travis docs](https://docs.travis-ci.com/user/languages/python/).

`.travis.yml`:

```yaml
language: python
python:
  - "3.5"
  - "3.6"
  #- "3.7-dev" # fails due to datrie build failure (snakemake dependency)

# command to install dependencies
install:
  - pip install -r requirements.txt
  - python setup.py build install

# command to run tests
script:
  - pytest
```

# Final Repository

All of the code for this repository is in
[charlesreid1/2019-snakemake-cli](https://github.com/charlesreid1/2019-snakemake-cli).

See the [v2.0 tag](https://github.com/charlesreid1/2019-snakemake-cli/releases/tag/v2.0)
in case there are changes to the code that are not reflected in
this blog post.

# Next Steps

This demo provides a starting point for creating executable Snakemake
workflows that are installable.

A few open question and directions:

- Bundling the Snakefile vs. user-provided Snakefles
    - There is obviously more utility and flexibility in letting the user provide Snakefiles.
    - User-provided Snakefiles provide more ways for workflows to go wrong.
    - Testing is either more difficult, or shifted to the workflow author.
    - Bundled Snakefiles take the burden of writing the workflow off of the user,
      so they can focus on param/config files.

- Kubernetes
    - Can we make the command line wrapper work with a Kubernetes cluster?
    - See [charlesreid1/2019-snakemake-byok8s](https://github.com/charlesreid1/2019-snakemake-byok8s)
      for proof of concept.

- Applications
    - How can we apply this concept?
    - [spacegraphcats](https://github.com/spacegraphcats/spacegraphcats)
    - [eelpond](https://github.com/dib-lab/eelpond)
    - [dahak](https://github.com/dahak-metagenomics/dahak) and 
      [dahak-taco](https://github.com/dahak-metagenomics/dahak-taco) 


