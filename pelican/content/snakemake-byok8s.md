Title: Building Snakemake Command Line Wrappers for Kubernetes Workflows
Date: 2019-01-28 20:00
Category: Snakemake
Tags: python, bioinformatics, workflows, pipelines, snakemake, travis, kubernetes, minikube

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
    - [What is minikube?](#minikube)
    - [AWS](#aws)
    - [Fixing DNS issues with AWS](#dns-aws)
    - [Travis](#travis)
    - [`.travis.yml`](#travis-yml)
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

```plain
# Get byok8s
git clone https://github.com/charlesreid1/2019-snakemake-byok8s.git
cd ~/2019-snakemake-byok8s

# Create a virtual environment
virtualenv vp
vp/bin/actiavte

# Install byok8s
pip install -r requirements.txt
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

<br />
<br />

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

When using cloud computing platforms like GCP (Google 
Cloud Platform) or AWS (Amazon Web Services),
k8s is a simple and popular way to orchestrate
multiple compute nodes (support for Docker images
is also baked directly into k8s).


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

<br />
<br />

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
## Namespaces 

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

<br />
<br />

<a name="minikube"></a>
# Local Kubernetes Clusters with Minikube

<a name="minikube"></a>
## What is minikube?

Minikube is a Go program that allows users to simulate
a single-node kubernetes cluster using a virtual machine.
This is useful for local testing of Kubernetes workflows,
as it does not require setting up or tearing down cloud
infrastructure, or long waits for remote resources to
become ready.

We cover two ways to use it:

1. Installing and running a minikube virtual kubernetes cluster on
   AWS (for development and testing of Snakemake + kubernetes
   workflows)

2. Running a minikube cluster on a Travis CI worker node
   to enable us to _test_ Snakemake + kubernetes workflows.

<a name="aws"></a>
## AWS

Using Minikube from an AWS EC2 compute node comes 
with two hangups.

The first is that AWS nodes are virtual machines,
and you can't run virtual machines within virtual
machines, so it is not possible to use minikube's
normal VirtualBox mode, which creates a kubernetes
cluster using a virutal machine.

Instead, we must use minikube's native driver, meaning
minikube uses docker directly. This is tricky for several
reasons:

- we can't bind-mount a local directory into the
  kubernetes cluster
- the minikube cluster must be run with sudo
  privileges, which means permissions can be
  a problem

The second hangup with minikube on AWS nodes is that the
DNS settings of AWS nodes are copied into the Kubernetes
containers, including the kubernetes system's DNS service
container. Unfortunately, the AWS node's DNS settings are
not valid in the kubernetes cluster, so the DNS container
crashes, and no container in the kubernetes cluster can
reach the outside world.  This must be fixed with a
custom config file (provided with byok8s; details below).

### Installing Python Prerequisites

To use byok8s from a fresh Ubuntu AWS node
(tested with Ubuntu 16.04 (xenial) and 18.04
(bionic)), you will want to install a version
of conda; we recommend using pyenv and miniconda:

```plain
curl https://pyenv.run | bash
```

Restart your shell and install miniconda:

```plain
pyenv update
pyenv install miniconda3-4.3.30
pyenv global miniconda3-4.3.30
```

You will also need the virtualenv package to
set up a virtual environment:

```plain
pip install virtualenv
```


### Installing byok8s

Start by cloning the repo and installing byok8s:

```plain
cd 
git clone https://github.com/charlesreid1/2019-snakemake-byok8s.git
cd ~/2019-snakemake-byok8s
```

Next, you'll create a virtual environment:

```plain
virtualenv vp
source vp/bin/activate

pip install -r requirements.txt
python setup.py build install
```

Now you should be ready to rock:

```
which byok8s
```

### Starting a k8s cluster with minikube

Install minikube:

```plain
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Now you're ready to start a minikube k8s
cluster on your AWS node! Start a k8s cluster
as root with:

```plain
sudo minikube start
```

**NOTE:** The `minikube start` command will print
some commands for you to run to fix permissions -
it is importat you run them!

Tear down the cluster with:

```plain
sudo minikube stop
```

While the k8s cluster is running, you can control
it and interact with it like a normal k8s cluster
using `kubectl`.

However, as-is, the cluster's DNS settings are broken!
We need to fix them before running.


<a name="dns-aws"></a>
## Fixing DNS issues with AWS

We mentioned a second hangup with AWS was with the
DNS settings. 

The problem is with `/etc/resolv.conf` on the
AWS host node. It is set up for AWS's internal 
cloud network routing, but this is copied
into the CoreDNS container, which is the
kube-system container that manages DNS requests
from all k8s containers. The settings from the
AWS host confuse the DNS container, and it cannot
route any DNS requests.

### The Problem

If you're having the problem, you will see
something like this with `kubectl`, where the
coredns containers are in a `CrashLoopBackOff`:

```plain
$ kubectl get pods --namespace=kube-system

NAME                               READY   STATUS             RESTARTS   AGE
coredns-86c58d9df4-lvq8b           0/1     CrashLoopBackOff   5          5m17s
coredns-86c58d9df4-pr52t           0/1     CrashLoopBackOff   5          5m17s
etcd-minikube                      1/1     Running            15         4h43m
kube-addon-manager-minikube        1/1     Running            16         4h43m
kube-apiserver-minikube            1/1     Running            15         4h43m
kube-controller-manager-minikube   1/1     Running            15         4h43m
kube-proxy-sq77h                   1/1     Running            3          4h44m
kube-scheduler-minikube            1/1     Running            15         4h43m
storage-provisioner                1/1     Running            6          4h44m
```

This will cause all Snakemake jobs to fail with a name
resolution failure when it tries to write its output
files to the AWS S3 bucket:

```plain
$ kubectl logs snakejob-c71fba38-f64b-5803-915d-933ae273d7a4

Building DAG of jobs...
Using shell: /bin/bash
Provided cores: 4
Rules claiming more threads will be scaled down.
Job counts:
	count	jobs
	1	target1
	1

[Thu Jan 24 00:06:03 2019]
rule target1:
    output: cmr-smk-0123/alpha.txt
    jobid: 0

echo alpha blue > cmr-smk-0123/alpha.txt
Traceback (most recent call last):
  File "/opt/conda/lib/python3.7/site-packages/urllib3/connection.py", line 171, in _new_conn
    (self._dns_host, self.port), self.timeout, **extra_kw)
  File "/opt/conda/lib/python3.7/site-packages/urllib3/util/connection.py", line 56, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
  File "/opt/conda/lib/python3.7/socket.py", line 748, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
socket.gaierror: [Errno -3] Temporary failure in name resolution
```

and the kubernetes log for the CoreDNS container

```plain
$ kubectl logs --namespace=kube-system coredns-86c58d9df4-lvq8b

.:53
2019/01/25 14:54:48 [INFO] CoreDNS-1.2.2
2019/01/25 14:54:48 [INFO] linux/amd64, go1.11, fc62f9c
CoreDNS-1.2.2
linux/amd64, go1.11, eb51e8b
2019/01/25 14:54:48 [INFO] plugin/reload: Running configuration MD5 = 486384b491cef6cb69c1f57a02087373
2019/01/25 14:54:48 [FATAL] plugin/loop: Seen "HINFO IN 9273194449250285441.798654804648663468." more than twice, loop detected
```

Basically, the AWS node's DNS name server settings cause 
an infinite DNS loop to be set up.

### The Fix

Fixing this problem requires manually setting the DNS 
name servers inside the CoreDNS container to Google's
public DNS servers, `8.8.8.8` and `8.8.4.4`.

To apply this fix, we use a YAML configuration file to patch the
CoreDNS container image.

Hat tip to [this long Github issue](https://github.com/kubernetes/minikube/issues/2027)
in the minikube Github repo, and specifically 
[this comment](https://github.com/kubernetes/minikube/issues/2027#issuecomment-381574807)
by Github user [jgoclawski](https://github.com/jgoclawski).
and also [this comment](https://github.com/kubernetes/minikube/issues/2027#issuecomment-419733791)
by Github user [bw2](https://github.com/bw2).
(Note that neither of these quite solve the problem -
jgoclawski's solution is for kube-dns, not CoreDNS,
and bw2's YAML is not valid, but both got me most
of the way to a solution.)

Here is the YAML file (also in the 2019-snakemake-byok8s
repo here: <https://github.com/charlesreid1/2019-snakemake-byok8s/blob/master/test/fixcoredns.yml>):

**`fixcoredns.yml`:**

```yaml
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

(**NOTE:** There is also a `fixkubedns.yml` if you are using
an older Kubernetes version that uses kube-dns instead of
CoreDNS.)

To tell the k8s cluster to use this image
when it creates a CoreDNS container, run
this kubectl command *while the cluster is
running*:

```plain
kubectl apply -f fixcoredns.yml
```

Last but not least, delete all `kube-system` containers
and let Kubernetes regenerate them:

```plain
kubectl delete --all pods --namespace kube-system
```

The pods will regenerate quickly, and you can
check to confirm that the CoreDNS container
is no longer in the `CrashLoopBackOff` state
and is `Running` nicely:

```plain
kubectl get pods --namespace=kube-system
```

This is all documented in [this comment](https://github.com/kubernetes/minikube/issues/2027#issuecomment-457808462)
in the same Github issue in the minikube repo
that was linked to above, [kubernetes/minikube
issue \#2027: dnsmasq pod CrashLoopBackOff](https://github.com/kubernetes/minikube/issues/2027).


<a name="aws-byok8s"></a>
## AWS + byok8s Workflow

Now that the k8s cluster is running successfully,
run the example byok8s workflow in the `test/` 
directory of the byok8s repository (assuming
you cloned the repo to `~/byok8s`, and are in
the same virtual environment as before):

```plain
# Return to our virtual environment
cd ~/2019-snakemake-byok8s/test/
source vp/bin/activate

# Verify k8s is running
minikube status

# Export AWS keys for Snakemake
export AWS_ACCESS_KEY_ID="XXXXX"
export AWS_SECRET_ACCESS_KEY="XXXXX"

# Run byok8s
byok8s workflow-alpha params-blue --s3-bucket=mah-bukkit 
```

The bucket you specify must be created in advance
and be writable by the account whose credentials
you are passing in via environment variables.

When you do all of this, you should see the job
running, then exiting successfully:

```plain
$ byok8s --s3-bucket=cmr-0123 -f workflow-alpha params-blue
--------
details!
	snakefile: /home/ubuntu/2019-snakemake-byok8s/test/Snakefile
	config: /home/ubuntu/2019-snakemake-byok8s/test/workflow-alpha.json
	params: /home/ubuntu/2019-snakemake-byok8s/test/params-blue.json
	target: target1
	k8s namespace: default
--------
Building DAG of jobs...
Using shell: /bin/bash
Provided cores: 1
Rules claiming more threads will be scaled down.
Job counts:
	count	jobs
	1	target1
	1
Resources before job selection: {'_cores': 1, '_nodes': 9223372036854775807}
Ready jobs (1):
	target1
Selected jobs (1):
	target1
Resources after job selection: {'_cores': 0, '_nodes': 9223372036854775806}

[Mon Jan 28 18:06:08 2019]
rule target1:
    output: cmr-0123/alpha.txt
    jobid: 0

echo alpha blue > cmr-0123/alpha.txt
Get status with:
kubectl describe pod snakejob-e585b53f-f9d5-5142-ac50-af5a0d532e85
kubectl logs snakejob-e585b53f-f9d5-5142-ac50-af5a0d532e85
Checking status for pod snakejob-e585b53f-f9d5-5142-ac50-af5a0d532e85
[Mon Jan 28 18:06:18 2019]
Finished job 0.
1 of 1 steps (100%) done
Complete log: /home/ubuntu/2019-snakemake-byok8s/test/.snakemake/log/2019-01-28T180607.988313.snakemake.log
unlocking
removing lock
removing lock
removed all locks
```

Woo hoo! You've successfully run a Snakemake workflow 
on a virtual Kubernetes cluster!


<a name="travis"></a>
## Travis

Like running minikube on an AWS node, running minikube on Travis workers
also suffers from DNS issues. Fortunately, Github user 
[LiliC](https://github.com/LiliC) worked out how to run
minikube on Travis, and importantly, _did so for multiple versions_
of minikube and kubernetes.

The relevant `.travis.yml` file is available in the 
[LiliC/travis-minikube](https://github.com/LiliC/travis-minikube)
repo on Github.

We ended up using the [`minikube-30-kube-1.12`](https://github.com/LiliC/travis-minikube/tree/minikube-30-kube-1.12)
branch of LiliC/travis-minikube, which used the most up-to-date
version of minikube and kubernetes available in that repo. The `.travis.yml` file
provided by LiliC on that branch is 
[here](https://github.com/LiliC/travis-minikube/blob/minikube-30-kube-1.12/.travis.yml).

The example script by LiliC provided 90% of the legwork (thanks!!!),
and we only needed to modify a few lines of LiliC's Travis file
(which launches a redis container using kubectl)
to use Snakemake (launched via byok8s) instead.

<a name="travis-yml"></a>
## `.travis.yml`

Here is the final `.travis.yml` file, which has explanatory comments.

**`.travis.yml`:**

```yaml
# Modified from original:
# https://raw.githubusercontent.com/LiliC/travis-minikube/minikube-30-kube-1.12/.travis.yml

# byok8s and Snakemake both require Python,
# so we make this Travis CI test Python-based.
language: python
python:
- "3.6"

# Running minikube via travis requires sudo
sudo: required

# We need the systemd for the kubeadm and it's default from 16.04+
dist: xenial

# This moves Kubernetes specific config files.
env:
- CHANGE_MINIKUBE_NONE_USER=true

install:
# Install byok8s requirements (snakemake, python-kubernetes)
- pip install -r requirements.txt
# Install byok8s cli tool
- python setup.py build install

before_script:
# Do everything from test/
- cd test
# Make root mounted as rshared to fix kube-dns issues.
- sudo mount --make-rshared /
# Download kubectl, which is a requirement for using minikube.
- curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.12.0/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/
# Download minikube.
- curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.30.0/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
- sudo minikube start --vm-driver=none --bootstrapper=kubeadm --kubernetes-version=v1.12.0
# Fix the kubectl context, as it's often stale.
- minikube update-context
# Wait for Kubernetes to be up and ready.
- JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}'; until kubectl get nodes -o jsonpath="$JSONPATH" 2>&1 | grep -q "Ready=True"; do sleep 1; done

################
## easy test
script:
- kubectl cluster-info
# Verify kube-addon-manager.
# kube-addon-manager is responsible for managing other kubernetes components, such as kube-dns, dashboard, storage-provisioner..
- JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}'; until kubectl -n kube-system get pods -lcomponent=kube-addon-manager -o jsonpath="$JSONPATH" 2>&1 | grep -q "Ready=True"; do sleep 1;echo "waiting for kube-addon-manager to be available"; kubectl get pods --all-namespaces; done
# Wait for kube-dns to be ready.
- JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}'; until kubectl -n kube-system get pods -lk8s-app=kube-dns -o jsonpath="$JSONPATH" 2>&1 | grep -q "Ready=True"; do sleep 1;echo "waiting for kube-dns to be available"; kubectl get pods --all-namespaces; done

################ 
## hard test
# run byok8s workflow on the k8s cluster
- byok8s --s3-bucket=cmr-0123 -f workflow-alpha params-blue
```

<a name="byok8s3"></a>
# End Product: byok8s

The final byok8s package can be found in the
[charlesreid1/2019-snakemake-byok8s](https://github.com/charlesreid1/2019-snakemake-byok8s)
repository on Github.

You can find documentation for 2019-snakemake-byok8s 
here: <https://charlesreid1.github.io/2019-snakemake-byok8s/>

To return to our quick start, here is what running
byok8s end-to-end on a minikube kubernetes cluster 
on an AWS node looks like (slightly modified from
the intro of our post):

```plain
# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Get byok8s
git clone https://github.com/charlesreid1/2019-snakemake-byok8s.git
cd ~/2019-snakemake-byok8s

# Create a virtual environment
virtualenv vp
vp/bin/actiavte

# Install byok8s
pip install -r requirements.txt
python setup.py build install

# Create virtual k8s cluster
sudo minikube start

# Fix CoreDNS
kubectl apply -f fixcoredns.yml
kubectl delete --all pods --namespace kube-system

# Wait for kube-system to respawn
kubectl get pods --namespace=kube-system

# Run the workflow on the k8s cluster
cd test/
byok8s workflow-alpha params-blue --s3-bucket=mah-bukkit 

# Clean up the virtual k8s cluster
sudo minikube stop
```

<br />
<br />

<a name="docs"></a>
# Documentation

You can find documentation for 2019-snakemake-byok8s 
here: <https://charlesreid1.github.io/2019-snakemake-byok8s/>

The documentation covers a quick start on AWS nodes, 
similar to what is covered above, as well as more information
about running byok8s on other types of Kubernetes clusters
(e.g., AWS, Google Cloud, and Digital Ocean).

<br />
<br />

<a name="next"></a>
# Next Steps

Last year we were working on implementing metagenomic pipelines for
shotgun sequencing data as part of the [dahak-metagenomics](https://github.com/dahak-metagenomics)
project. We implemented several Snakemake workflows
in the [dahak](https://github.com/dahak-metagenomics/dahak)
repo, and began (but never completed) work on a command line utility
to run these workflows called [dahak-taco](https://github.com/dahak-metagenomics/dahak-taco).

Our next major goal is to reboot dahak-taco and redesign it to run metagenomic
workflows from dahak on Kubernetes clusters, similar to the way byok8s works.

Stay tuned for more!

