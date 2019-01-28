Title: Building Snakemake Command Line Wrappers for Kubernetes Workflows
Date: 2019-01-23 22:00
Category: Snakemake
Tags: python, bioinformatics, workflows, pipelines, snakemake, travis, kubernetes, minikube
Status: draft

**NOTE:** These ideas are implemented in the repository
[charlesreid1/2019-snakemake-byok8s](https://github.com/charlesreid/2019-snakemake-byok8s).

<br />
<br />

## Table of Contents:

- [Recap: Workflows as Executables](#exe)
    - [2018-snakemake-cli](#2018)
    - [2019-snakemake-cli](#2019)
    - [2019-snakemake-byok8s](#byok8s)
- [Overview of 2019-snakemake-byok8s](#byok8s2)
    - [Cloud + Scale = Kubernetes](#k8s)
    - [Snakemake k8s support](#smkk8s)
- [Modifying the CLI](#cli)
    - [Namespaces](#ns)
    - [Adding flags](#flags)
- [Local Kubernetes Clusters with Minikube](#minikube)
    - [AWS](#aws)
    - [Fixing DNS issues with AWS](#dns-aws)
    - [Travis](#travis)
    - [Fixing DNS issues with Travis](#dns-travis)
- [End Product: byok8s](#byok8s3)
- [Documentation](#docs)
- [Next Steps](#next)


<br />
<br />

<a name="exe"></a>
# Recap: Workflows as Executables

In our previous blog post, [Building Snakemake Command Line Wrappers](https://charlesreid1.github.io/building-snakemake-command-line-wrappers.html),
we covered some approaches to making Snakemake
workflows into executables that can be run as
command line utilities.

In this post, we extend those ideas to Snakemake workflows
that run on Kubernetes clusters.

<a name="2018"></a>
## 2018-snakemake-cli

To recap, back in March 2018 Titus Brown wrote a blog post titled
[Pydoit, snakemake, and workflows-as-applications](http://ivory.idyll.org/blog/2018-workflows-applications.html)
in which he implemented a proof-of-concept command
line utility wrapping the Snakemake API to create
an executable Snakemake workflow.

The end result was a command line utility that could
be run like so:

```plain
./run <workflow-config> <workflow-params>
```

Relevant code is in [ctb/2018-snakemake-cli](https://github.com/ctb/2018-snakemake-cli).


<a name="2019"></a>
## 2019-snakemake-cli

In our previous blog post, [Building Snakemake Command Line Wrappers](https://charlesreid1.github.io/building-snakemake-command-line-wrappers.html),
we extended this idea to create a bundled executable
command line utility that could be installed with
`setup.py` and run from a working directory. We also
demonstrated a method of writing tests for the 
Snakemake workflow and running those tests with
Travis CI.

We packaged the Snakefile with the command line utility,
but the approach is flexible and can be modified to
use a user-provided Snakemake workflow or Snakefile.

The end result was a command line utility called
`bananas` that could be installed and run like
the `run` wrapper above:

```plain
bananas <workflow-config> <workflow-params>
```

Relevant code is in [charlesreid1/2019-snakemake-cli](https://github.com/charlesreid1/2019-snakemake-cli).


<a name="byok8s"></a>
## 2019-snakemake-byok8s

The next logical step in bundling workflows was to take
advantage of Snakemake's ability to run workflows across
distributed systems.

Specifically, we wanted to modify the command line utility
above to run the workflow on a user-provided Kubernetes
cluster, instead of running the workflow locally.

The result is [2019-snakemake-byok8s](https://github.com/charlesreid1/2019-snakemake-byok8s),
a command line utility that can be installed with
a `setup.py` and that launches a Snakemake workflow 
on a user-provided Kubernetes cluster. Furthermore,
we demonstrate how to use minikube to run a local
Kubernetes cluster to test Snakemake workflows on
Kubernetes clusters.

Here's what it looks like in practice:

```
# Install byok8s
python setup.py build install

# Create virtual k8s cluster
minikube start

# Run the workflow on the k8s cluster
cd /path/to/workflow/
byok8s my-workflowfile my-paramsfile --s3-bucket=my-bucket

# Clean up the virtual k8s cluster
minikube stop
```

We cover the details below.


<a name="byok8s2"></a>
# Overview of 2019-snakemake-byok8s

<a name="k8s"></a>
## Cloud + Scale = Kubernetes (k8s)

First, why kubernetes (k8s)?

To scale Snakemake workflows to multiple compute nodes,
it is not enough to just give Snakemake a pile of
compute nodes and a way to remotely connect to each.
Snakemake requires the compute nodes to have a 
controller and a job submission system.

When using cloud computing platforms like GCP or AWS,
k8s is a simple and popular way to orchestrate
multiple compute nodes (support for Docker images
is also baked into k8s).


<a name="smkk8s"></a>
## Snakemake k8s Support

Snakemake has built-in support for k8s, making
the combination a logical choice for running 
Snakemake workflows at scale in the cloud. 

The `minikube` tool, which we will cover later
in this blog post, makes it easy to run a local
virtual k8s cluster for testing purposes, and
even makes it possible to run k8s tests using
Travis CI.

Snakemake only requires the `--kubernetes` flag,
and an optional namespace, to connect to
the k8s cluster. (Under the hood, Snakemake
uses the Kubernetes Python API to connect
to the cluster and launch jobs.)

If you can run `kubectl` from a computer
to control the Kubernetes cluster, you can
run a Snakemake workflow on that cluster.

Let's get into the changes required in the Python code.

<a name="cli"></a>
# Modifying the CLI

In our [prior post](https://charlesreid1.github.io/building-snakemake-command-line-wrappers.html)
covering [charlesreid1/2019-snakemake-cli](https://github.com/charlesreid1/2019-snakemake-cli),
we showed how to create a command line utility
using the `cli/` directory for the command line
interface package, and specifying it is a cli
entrypoint in `setup.py`:

```plain
cli/
├── Snakefile
├── __init__.py
└── command.py
```

and the relevant bit from `setup.py`:

```python
setup(name='bananas',
        ...
        entry_points="""
[console_scripts]
{program} = cli.command:main
      """.format(program = _program),
``` 

We want our new command line utility, `byok8s`, to work
the same way, so we can do a `s/byok8s/bananas/g`
across the package.

The only change required happens in the file
`command.py`, where the Snakemake API call 
happens.


<a name="ns"></a>
## Nmespaces 

Checking the [Snakemake API documentation](https://snakemake.readthedocs.io/en/stable/api_reference/snakemake.html),
we can see that the API has a `kubernetes` option:

> **kubernetes** *(str)* – submit jobs to kubernetes,
> using the given namespace.

so `command.py` should modify the Snakmake API call
accordingly, adding a kubernetes namespace.
This is a parameter the user usually won't need
to provide (`default` is the typical namespace
we want to use) but we added a `-k` argument
to the ArgParser to allow the user to specify
the Kubernetes namespace name. By default
the Kubernetes namespace used is `default`.

<a name="flags"></a>
## Adding flags

We add and modify some flags to make the workflow
more flexible:

* The user now provides the Snakefile, which is
  called `Snakefile` in the current working directory
  by default but can be specified with the `--snakefile`
  or `-s` flag

* The user provides the k8s namespace using the
  `--k8s-namespace` or `-k` flag

* The user provides the name of an S3 bucket for
  Snakemake worker nodes to use for I/O using the
  `--s3-bucket` flag

Finally, the user is also required to provide their
AWS credentials to access the S3 bucket, via two
environment variables that Snakemake passes through
to the Kubernetes worker nodes:

```plain
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

For Travis CI testing, these environment variables
can be set in the repository settings on the Travis
website once Travis CI has been enabled.

See <https://charlesreid1.github.io/2019-snakemake-byok8s/travis_tests/>
for details.

<a name="minikube"><a>
# Local Kubernetes Clusters with Minikube

<a name="aws"></a>
## AWS

Using Minikube from AWS comes with two hangups.

The first is that AWS nodes are virtual machines,
and you can't run virtual machines within virtual
machines, so it is not possible to use minikube's
normal VirtualBox mode, which creates k8s nodes
with VirtualBox machines. Instead, we must use 
minikube's native driver, meaning minikube uses
docker directly. This is tricky for several 
reasons:

- we can't bind-mount a local directory into the
  kubernetes cluster
- the minikube cluster must be run with sudo
  privileges, which means permissions can be
  a problem

The second is that the DNS settings of AWS nodes
are copied into the Kubernetes containers,
including the DNS service container, which
breaks DNS for the entire Kubernetes cluster.
This must be fixed with a custom config file
(provided with byok8s; details below).

### Installing Python Prerequisites

To use byok8s from a fresh Ubuntu AWS node
(should work with both 18.04 bionic and 16.04
xenial), you will want to install a version of
conda; we recommend using pyenv and miniconda:

```
curl https://pyenv.run | bash
```

Restart your shell and install miniconda:

```
pyenv update
pyenv install miniconda3-4.3.30
pyenv global miniconda3-4.3.30
```

You will also need the virtualenv package to
set up a virtual environment:

```
pip install virtualenv
```


### Installing byok8s

Start by cloning the repo and installing byok8s:

```
git clone https://github.com/charlesreid1/2019-snakemake-byok8s.git byok8s
cd byok8s
```

Next, you'll create a virtual environment:

```
virtualenv vp
source vp/bin/activate

pip install -r requirements.txt
```

### Starting a k8s cluster with minikube

Install minikube:

```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Now you're ready to start a minikube k8s
cluster on your AWS node! Start a k8s cluster
as root with:

```
sudo minikube start
```

**NOTE:** The `minikube start` command will print
some commands for you to run to fix permissions -
it is importat you run them!

Tear down the cluster with:

```
sudo minikube stop
```

While the k8s cluster is running, you can control
it and interact with it like a normal k8s cluster
using `kubectl`.

However, as-is, the cluster's DNS settings are broken!
We need to fix them before running 


<a name="dns-aws"></a>
## Fixing DNS issues with AWS

We mentioned a second hangup with AWS was with the
DNS settings. 

The problem is with `/etc/resolv.conf` on the
AWS node. It is set up for AWS's internal 
cloud network routing, but this is copied
into the CoreDNS container, which is the
kube-system container that manages DNS requests
from all k8s containers.

The fix requires setting the DNS nameservers 
inside the CoreDNS container to Google's public
DNS, `8.8.8.8` and `8.8.4.4`.

Here is the YAML file, for completeness:

```
kind: ConfigMap
apiVersion: v1
data:
  Corefile: |
    .:53 {
        errors
        health
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           upstream 8.8.8.8 8.8.4.4
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
        }
        proxy .  8.8.8.8 8.8.4.4
        cache 30
        reload
    }
metadata:
  creationTimestamp: 2019-01-25T22:55:15Z
  name: coredns
  namespace: kube-system
```



<a name="aws-byok8s"></a>
## AWS + byok8s Workflow


<a name="travis"></a>
## Travis

<a name="dns-travis"></a>
## Fixing DNS issues with Travis


<a name="byok8s3"></a>
# End Product: byok8s

<a name="docs"></a>
# Documentation

<a name="next"></a>
# Next Steps




-------






Relevant portion of `cli/command.py` for
2019-snakemake cli and `bananas`:

```python
    
    ...

    print('--------')
    print('details!')
    print('\tsnakefile: {}'.format(snakefile))
    print('\tconfig: {}'.format(workflowfile))
    print('\tparams: {}'.format(paramsfile))
    print('\ttarget: {}'.format(target))
    print('--------')

    # run bananas!!
    status = snakemake.snakemake(snakefile, 
                                 configfile=paramsfile,
                                 targets=[target], 
                                 printshellcmds=True,
                                 dryrun=args.dry_run, 
                                 forceall=args.force,
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


<a name="using"></a>
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

```
which bananas
```

## Quick Start: Running Tests

```
pytest
```

## Quick Start: Running Examples

Change to the `test/` directory and run tests with
the example config and param files.

```
cd test
```

Run the hello workflow with Amy params:

```
rm -f hello.txt
bananas workflow-hello params-amy
```

Run the hello workflow with Beth params:

```
rm -f hello.txt
bananas workflow-hello params-beth
```

Run the goodbye workflow with Beth params:

```
rm -f goodbye.txt
bananas workflow-goodbye params-beth
```


<a name="travis"></a>
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

<a name="repo"></a>
# Final Repository

All of the code for this repository is in
[charlesreid1/2019-snakemake-cli](https://github.com/charlesreid1/2019-snakemake-cli).

See the [v2.0 tag](https://github.com/charlesreid1/2019-snakemake-cli/releases/tag/v2.0)
in case there are changes to the code that are not reflected in
this blog post.

<a name="next"></a>
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


