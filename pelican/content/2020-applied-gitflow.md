Title: Applied Gitflow
Date: 2020-07-01 12:00
Category: Git
Tags: git, github, programming, gitflow, hubflow, patterns

[TOC]

**This is a retroactive blog post. This post was authored in February 2022,
using material authored in July 2020.**

The most up-to-date version of this content is here: <https://charlesreid1.com/wiki/Applied_Gitflow>

## How We Apply Gitflow

In some prior blog posts, we've covered a few patterns that we use for software development,
including:

* [Automatically generating requirements.txt files with pinned versions for Python
  projects](https://charlesreid1.github.io/automatically-generating-up-to-date-requirementstxt-for-python-projects.html),
  which covered a Makefile rule that would programmatically generate a fresh, up-to-date requirements.txt file
  for a Python project

* [Incorporating Terraform commands into
  Makefiles](https://charlesreid1.github.io/incorporating-terraform-commands-into-makefiles.html) to make it easy
  to use `make` and terraform to manage multiple cloud deployments

* [Git workflows: supercharging your git
  config](https://charlesreid1.github.io/git-workflows-part-1-supercharging-your-git-config.html), which covers
  some tricks and aliases for the git configuration file that makes some git operations a lot easier

* [Git workflows: refactoring large branches and pull
  requests](https://charlesreid1.github.io/git-workflows-part-3-refactoring-large-branches-and-pull-requests.html),
  which covered strategies and techniques for refactoring a large set of changes
  or pull request into smaller chunks that are simpler and easier to review,
  without having to start from scratch

In this post, we'll get into some details about how we manage software in git repositories.

Specifically, we want to provide some details about how gitflow looks
when it's being used to manage software with different versions,
and when that software is being deployed in multiple environments.

The original gitflow pattern doesn't talk much about how software
deployments in multiple environments fits in with the gitflow model,
or even *if* it fits in the gitflow model.

With a few adjustments and patterns, gitflow can easily handle both.
In this post we'll share patterns we have found useful when using
gitflow to manage both deployments and releases.

## The Tools

The main tool for this writeup is git, used for version control of the repository. GitHub and Gitea provide an
interface to manage the git repository and to collaborate/review code. We use the gitflow model for managing
branches and code, so we'll summarize it, and provide a link with the details. 

We are also using a cloud provider where we upload the code to the cloud, and the code is run there. 
(Think AWS lambda function.) That code is separate from the git repository, so we need a way to track
what code is in what environment. We'll cover how we do that, too. 

## Recap of Gitflow

Since this post is talking about how to apply [Gitflow](https://nvie.com/posts/a-successful-git-branching-model/),
let's go through a quick recap of how it works.

Gitflow requires that a few branches be created, but
let's assume you're working in a repo already set up with Gitflow.
In that case, regular development work looks like thi:

* The `develop` branch is where the newest version is being worked on
* Specific fixes or features go into their own feature branch
* Feature branches are reviewed/tested before being merged into `develop`
* When it is time for a new version, the accumulated features on `develop` are
  put into a new branch for the new version.
* When the new version is ready, the `main` branch is updated to point to the new version branch.
  A new release is made from the main branch.

There is also a workflow for bug fixes for versions that have already been released:

* A new hotfix branch is created from the version branch (which is also what the `main` branch is pointing to)
* The changes are added to the hotfix branch
* The hotfix branch is merged back into the version branch, the version number is bumped, and a new release is cut.
* The hotfix branch is also merged into the `develop` branch, so that it will make it into future releases.

## Deploying and Releasing

As the original author himself says on the page describing Gitflow,
this model doesn't say much about how to handle deployments into
multiple cloud environments.

There are two main actions that an operator can take, using the system we have devised:

* deploy code (upload the code to a cloud stage, and have that version of the code running in the cloud)
* release code (update which version of the code is considered the "latest version")

Additionally, the actions the operator can take will require certain variables to be defined - the location of the
source code, and which cloud environment (development, integration, production) we're deploying to, for example. Those
variables are defined using environment variables, so that we can use scripts to do deploy or release actions.

## Environment File

Before covering the deploy and release scripts, here is an example environment file. The example release script
below refers to these variables. The deploy script (no example provided, since it will inevitably be case-specific)
also uses these environment variables. More environment variables can be added as needed, to grow with the
complexity of the software and deployment process.

```plain
#!/bin/bash

export PROJECTNAME_PACKAGENAME_HOME="${HOME}/path/to/package"
export PROJECTNAME_PACKAGENAME_STAGE="dev"
```

## Deploy Action

The deploy action is the action that takes the code in its current state and uploads it to the cloud. That can take
many forms depending on the cloud service being used, but for example deploying an AWS lambda function would mean
creating a new .zip file from the lambda function code, and uploading that zip file to the corresponding lambda
function using the AWS CLI.

The deploy action is a script that is run. It deploys the code in its current state in the repository. Environment
variables are used to parameterize the script. There are environment variables to specify the repository location
on disk, to specify the deployment stage, and any others that are needed.

The deploy script is also the place to assert certain conditions are true before the deploy action is taken. We
keep it simple, but these can be expanded on:

* Check various environment variables are set
* Check environment variable values

These can be done in the deploy script directly, if the checks are simple, or they can be moved to an entire
separate script like a hypothetical `check_env.sh`, which would be run before the deploy script (using a make rule
dependency).

(Note that if checks are TOO strict, they can interfere with deployment, so they should be adjusted accordingly.) 

Another step the deployment action might have before the actual deployment is to assemble any deployment
configuration files. For example, if the deployment process requires a JSON file that is dynamically assembled from
other bits of information, that could go in its own script that would be run before the deploy script (using a make
rule dependency).

For this writeup, we keep things simple and do all the checks in the deploy script.

## Release Action

The release action can be thought of as a git repository operation.

**When does a release happen?**

When using gitflow, features and bugfixes will accumulate in the develop branch. Eventually the time for a new
release will come (scheduled, or because enough changes have accumulated). A new branch will be created that will
"freeze" the code in whatever state the develop branch is in. (Freeze is in quotes, because there are small changes
that need to be made to that "frozen" code before a release happens, but those are changes like bumping the version
number - no core changes.)

**Where does the release script come in?**

Once the code in the release branch is ready to go, the release script is run. The script will create a git tag, reset the head of the branch corresponding to the release (the "stable release" branch, usually main) to the head of the pre-release branch - whatever branch you're on when the release script is being run. Using our convention, we name this branch release/v1 (prefixed with release/ and a v plus the major version number only). 

**What does the release script do?**

The release script starts by running some checks to make sure the code is in a state that's ready to release. There
must be no uncommitted files in the repo, there must be no changes to tracked files, and there must be no unpushed
changes in the repository (local commits that haven't been pushed to the remote).

If those conditions are met, then the release script proceeds. The release script will start by creating a git tag,
which records the date, time, and branch being released to. Next, the head of the branch to release to (usually
main) will be reset to the head of the branch to release from (the "frozen" code that's all fixed up for the
release). Finally, the release script will push the results of the reset operation, and the new tag, to the remote.

To keep it more general, the release script uses the concept of a "source" and "destination" branch - the source is
the branch to release from, the destination is the branch to release to. The destination branch is the one whose
head is reset to the source branch's head. (That should help clarify the script below a bit more.) 

Also, the Makefile (which we cover below) will take care of providing the right destination and source branch
names.

## Release Script

Here is an example release script, which we would add to our repository at `scripts/release.sh`:

```bash
#!/bin/bash
set -euo pipefail
set -x

REMOTE="origin"

# Check that environment file has been sourced
if [ -z "${PROJECTNAME_PACKAGENAME_HOME}" ]; then
	echo 'You must set the $PROJECTNAME_PACKAGENAME_HOME environment variable to proceed.'
	exit 1
fi

# Check the script is being called correctly
if [[ $# != 2 ]]; then
    echo "Given a source (pre-release) branch and a destination (release) branch,"
	echo "this script does the following:"
	echo " - create a git tag"
	echo " - reset head of destination branch to head of source branch"
	echo " - push result to git repo"
    echo
    echo "Usage: $(basename $0) source_branch dest_branch"
    echo "Example: $(basename $0) release/v2 main"
    exit 1
fi

# Check that all changes are committed
if ! git diff-index --quiet HEAD --; then
    echo "You have uncommitted files in your Git repository. Please commit or stash them."
    exit 1
fi

export PROMOTE_FROM_BRANCH=$1 PROMOTE_DEST_BRANCH=$2

# Check that there are no local commits that haven't been pushed yet
if [[ "$(git log ${REMOTE}/${PROMOTE_FROM_BRANCH}..${PROMOTE_FROM_BRANCH})" ]]; then
    echo "You have unpushed changes on your promote from branch ${PROMOTE_FROM_BRANCH}! Aborting."
    exit 1
fi

RELEASE_TAG=$(date -u +"%Y-%m-%d-%H-%M-%S")-${PROMOTE_DEST_BRANCH}.release

# Check whether there are commits on the destination branch that aren't on the source branch (changes would be thrown away)
if [[ "$(git --no-pager log --graph --abbrev-commit --pretty=oneline --no-merges -- $PROMOTE_DEST_BRANCH ^$PROMOTE_FROM_BRANCH)" != "" ]]; then
    echo "Warning: The following commits are present on $PROMOTE_DEST_BRANCH but not on $PROMOTE_FROM_BRANCH"
    git --no-pager log --graph --abbrev-commit --pretty=oneline --no-merges $PROMOTE_DEST_BRANCH ^$PROMOTE_FROM_BRANCH
    echo -e "\nYou must transfer them, or overwrite and discard them, from branch $PROMOTE_DEST_BRANCH."
    exit 1
fi

# Check that untracked files are not present
if ! git --no-pager diff --ignore-submodules=untracked --exit-code; then
    echo "Working tree contains changes to tracked files. Please commit or discard your changes and try again."
    exit 1
fi

# Perform the actual release operations
git fetch --all
git -c advice.detachedHead=false checkout ${REMOTE}/$PROMOTE_FROM_BRANCH
git checkout -B $PROMOTE_DEST_BRANCH
git tag $RELEASE_TAG
git push --force $REMOTE $PROMOTE_DEST_BRANCH
git push --tags $REMOTE
```

### Breaking It Down

Let's break down the essential commands, starting with the checks: 

`git diff-index --quiet HEAD --`

* Checks that all changes are committed
* git diff-index is basically the same as git diff, but restricted to the working tree or index only
* See <https://stackoverflow.com/q/24197606>

`git log ${REMOTE}/${PROMOTE_FROM_BRANCH}..${PROMOTE_FROM_BRANCH}`

* Checks the difference between the remote and local versions of the promote from branch
* If this command turns up any commits, those are all local, unpushed commits

`RELEASE_TAG=$(date -u +"%Y-%m-%d-%H-%M-%S")-${PROMOTE_DEST_BRANCH}.release`

* Creates a name for the git tag with the date and time, and branch being released to
* This stores the release history in git tags

`git --no-pager log --graph --abbrev-commit --pretty=oneline --no-merges -- $PROMOTE_DEST_BRANCH ^$PROMOTE_FROM_BRANCH)`

* This command checks for any commits that are on the destination branch and not on the source branch
* Because the destination branch's head will be reset, commits on the destination branch but not on the source branch would be lost
* (This script could optionally add a --force flag, to power through the release even if this check fails)

`git --no-pager diff --ignore-submodules=untracked --exit-code`

* Checks if there are any untracked changes in the working tree
* If there are, the release can't proceed

Now here's a breakdown of the release process commands:

`git fetch --all`

* Ensures we have an up-to-date picture of where the remotes are at

`git -c advice.detachedHead=false checkout ${REMOTE}/$PROMOTE_FROM_BRANCH`

* Checks out the source branch from the remote
* This command is the reason why we have to make sure all local commits are pushed to the remote
* The release process uses the remote version of the source/destination branches

`git checkout -B $PROMOTE_DEST_BRANCH`

* This step forces the destination branch to be the same as the source branch.

`git tag $RELEASE_TAG`

* Creates a record of what was released and when via a git tag

`git push --force $REMOTE $PROMOTE_DEST_BRANCH`

`git push --tags $REMOTE`

* Pushes the results of the operations to the remote

## Makefile

Now we add a Makefile with rules for releasing and deploying.

The first rule is the release rule - run this when the current branch is release/vX and it's ready for it's final release.

```make
CB := $(shell git branch --show-current)

release_mainx:
	@echo "Releasing current branch $(CB) to mainx"
	scripts/release.sh $(CB) mainx
```

The `$(CB)` is short for current branch.

Now on to the deploy rule.

Because we might want to deploy the code in an arbitrary state (temporarily deploying a feature branch to the development stage, for example), the deploy script and deploy rule are intended to deploy the code in its current state, and don't have the same kinds of checks as the release script. 

```make
deploy:
	scripts/deploy.sh
```
As mentioned above, the deploy script will be case-specific so we don't provide an example.

How does the deploy script know which environment to deploy to? It depends on the environment file that was
sourced, and the value of the `PROJECTNAME_PACKAGENAME_STAGE` variable. The deploy script should be checking that
that environment variable is set to a valid value before proceeding with the deploy.

## More Details

For more details, see the full writeup on our wiki here:
<https://charlesreid1.com/wiki/Applied_Gitflow>
