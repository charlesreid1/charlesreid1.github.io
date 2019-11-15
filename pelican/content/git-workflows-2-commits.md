Title: Git Workflows, Part 2: Crafting Commits
Date: 2019-11-14 20:00
Category: Git
Tags: git, rebase, cherry-pick, branching, version control
Status: draft

# Table of Contents

* [Summary](#summary)
* [What is a commit](#what-is-a-commit)
    * [git add](#git-add)
    * [git commit](#git-commit)
    * [git rebase](#git-rebase)
    * [git fetch and git pull](#git-fetch-and-git-pull)
        * [rebase, merge, branch, pass](#rebase-merge-branch-pass)
    * [git push](#git-push)
    * [force pushing](#force-pushing)
* [Commit Workflow](#commit-workflow)
    * [Principles](#principles)
    * [Making Small Commits](#making-small-commits)
        * [git add patch mode](#git-add-patch-mode)
        * [git add editor mode](#git-add-editor-mode)
    * [Modifying Commits](#modifying-commits)
    * [Rearranging Commits](#rearranging-commits)
    * [Combining Commits](#combining-commits)

# Summary

* Make your commits small and atomic, and recombine them into
  larger commits later; it's easier to combine smaller commits
  than to split large commits.

* Make use of `git add -p` and `git add --interactive` to stage
  changes selectively and atomically.

* Make use of `git rebase` and `git cherry-pick` to edit your
  commits and assemble them in the order you want.

* Once commits have been combine and the history is satisfactory,
  push to a remote to share the work.

* Think about ordering your commits to "tell a story". (What that
  means will depend on the people you are collaborating with!)

# What is a commit

before we get into the good stuff, let's talk about the
anatomy of a git commit.

when you add files to your git repository, it's a two-step
process: `git add` and `git commit`. The first step _stages_
your changes, the second step memorializes those staged changes
into a commit that can now be shared with others by pushing it
to git remotes.

## git add

It is important to know that git does not keep track of changes at
the file level, it keeps track of changes at the character/line level.

What that means is, when you modify a line in a file that is in your
git repository, and run `git add` to stage your change, git has created
an object under the hood called a _blob_ to represent that one line change.

If you change two lines in two different parts of a file, and stage those
changes using `git add`, git will treat this as two separate changes, and
represent the changes with two different blobs.

## git commit

As you use `git add` to prepare your changes, the changes are added to
a _staging area_. Think of this staging area as a draft commit. Each change
being added to the staging area changes how the commit will look. When the
changes are complete and the user runs `git commit`, it turns the staging
area into a real commit, creates the metadata, and calculates hashes.

When a commit is created, it receives a name, which is the hash of the
contents of the commit. The hash is computed from the contents of the
blobs, plus the metadata about the commit, plus the hash of the prior
commits. Changing a commit changes its hash, and will change the hashes
of all subsequent commits.

Commits in your local repository can be easily rewritten and edited, and
their hashes changed. A common workflow is to make many small commits,
and recombine them later.

Because the commit hash is how the commit is named, modifying commits
after you've shared them is bad practice and will create extra work for
your collaborators. For that reason, don't `git push` until you're ready
to share your work.

## git rebase

The `git rebase` command allows you to edit your commit history. We will
cover some usage patterns in the sections below.

## git fetch and git pull

Before pushing changes to the remote, first check if there have been any
commits since you began your branch.

### rebase, merge, branch, pass

If a feature branch is created off of the master branch, and some time passes,
the feature branch base commit may grow far out of sync with the master branch.
(Note that `master` indicates the primary branch.)

This leaves the developer of the feature branch a few choices:

- **rebase** - continue to rebase all commits on the feature branch from the
  original feature branch base commit onto the head commit of the master branch.
  - Pros: clean history, easy for one-branch-one-developer workflow
  - Cons: requires continual force-pushes, requires coordination between developers
    to prevent squashing others' work, not scalable, some people hate this method

- **merge** - occasionally merge work from the master branch into the feature branch.
  - Pros: simple to understand, simple to carry out, low cognitive load
  - Cons: clutters PR review by mixing feature changes with merged changes, clutters the
    commit history

- **branch** - by making heavy use of throwaway branches and integration branches,
  it is easier to test out how the integration of a feature branch based on an old
  commit on `master` will do when merging it in with a newer version of `master`.
  Use throwaway integration branches to test out merging the two branches together,
  testing its functionality, etc. You can also rebase or cherry pick commits onto
  the throwaway integration branch, and figure out how to arrange the commits on a
  branch to "rebuild" it into a working, mergeable branch.

- **pass** - best combined with the branch approach mentioned above, the pass approach
  is to leave the branch history clean, avoid force-pushes, and rely on throwaway
  branches to test out merge strategies once the inevitable PR merge needs to happen.
  It can also be useful to wait for code reviews to finish, then create a merge commit
  to make the merge happen smoothly.

## git push

Once you run `git push`, all of the commits on the branch that you pushed
will end up on the remote, where others can access them. The purpose
of a `git push` is to share commits, so generally you don't push branches
until they are ready to share. This also allows more flexibility in crafting,
rewriting, and combining commits.

## force pushing

If you pushed a branch (which is a collection of commits) to a remote,
and then you have edited those commits, you will run into a problem when
you try and `git push` the new, edited versions of the commits to the same
remote. The remote will detect that there are conflicting versions of
the branch and will reject the changes.

That's where `git push --force` comes in. The `--force` flag tells the
remote to discard its version of the branch and use the version of the
branch that you are pushing.

We will cover more about force pushing - when to do it, when not to, and
why some people hate it - in part 3 of this post. For now, we will only say
that you should not force push often, since you can risk deleting others' work
and creating additional confusion and work for all of your collaborators.

# Commit Workflow

## Principles

Here are some principles for your `git commit` workflow:

* Commit small changes often.

* Don't sweat the commit messages - they can be fixed up later.

* Related - nobody will see your commits until you push your branch,
  so think of your branch as a scratch space. You have the ultimate
  freedom to use it however you want.

* Branches are easy to create, so make liberal use of branches!

* Be wary of force pushing, and of rewriting history.

## Making Small Commits

Two essential git commands to help with making small commits are
git add (patch mode) and git add (interactive mode).

### git add patch mode

How to use:

```plain
git add -p <name-of-file>
```

The `git add -p` command allows the user to interactively stage
individual changes made (in what is called patch mode). This means
users can stage certain changes for one commit, then stage other
changes for a different commit.

This solves the problem of making a long sequence of changes
to a single file that should be logically separated into
different steps. (For example, changing the `import` statements
versus changing the name of a variable throughout a file).

For example, suppose we have the following changes to a file named `doit.sh`:

```plain
$ git diff doit.sh
diff --git a/doit.sh b/doit.sh
index 3b938a1..6c1aec8 100644
--- a/doit.sh
+++ b/doit.sh
@@ -1,6 +1,6 @@
 #!/bin/bash
 #
-# This script lists the 40 largest files in the git repo history
+# This script lists the 50 largest files in the git repo history

 $ git rev-list --all --objects | \
      sed -n $(git rev-list --objects --all | \
@@ -9,9 +9,9 @@ $ git rev-list --all --objects | \
      grep blob | \
      sort -n -k 3 | \
      \
-     tail -n40 | \
+     tail -n50 | \
      \
      while read hash type size; do
           echo -n "-e s/$hash/$size/p ";
      done) | \
-     sort -n -r -k1
+     sort -nru -k1
```

There are two related changes and one unrelated change, respectively.
We can split these changes into two commits using `git add -p doit.sh`,
which will walk through each change in the file and ask if we want to
stage it:

```plain
$ git add -p doit.sh
diff --git a/doit.sh b/doit.sh
index 3b938a1..6c1aec8 100644
--- a/doit.sh
+++ b/doit.sh
@@ -1,6 +1,6 @@
 #!/bin/bash
 #
-# This script lists the 40 largest files in the git repo history
+# This script lists the 50 largest files in the git repo history

 $ git rev-list --all --objects | \
      sed -n $(git rev-list --objects --all | \
Stage this hunk [y,n,q,a,d,j,J,g,/,e,?]? y

@@ -9,9 +9,9 @@ $ git rev-list --all --objects | \
      grep blob | \
      sort -n -k 3 | \
      \
-     tail -n40 | \
+     tail -n50 | \
      \
      while read hash type size; do
Stage this hunk [y,n,q,a,d,j,J,g,/,e,?]? y

@@ -14,14 +14,14 @@        echo -n "-e s/$hash/$size/p ";
      done) | \
-     sort -n -r -k1
+     sort -nru -k1
Stage this hunk [y,n,q,a,d,j,J,g,/,e,?]? n
```

Now the two related changes are staged, and the unrelated change is not staged.
This is reflected in `git status`:

```plain
$ git status
On branch master
Your branch is ahead of 'gh/master' by 2 commits.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   doit.sh

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   doit.sh
```

Now `git commit` will commit only the staged portions.

Do not provide any filenames to `git commit`, so that git will only commit the staged changes.

To use this in your workflow, think about how you can group different changes together into
different commits. If you get a portion of a feature working, you can commit the changes in
groups so that related changes get committed together.

Also remember that if your commit history ends up being excessively long or overly detailed,
you can always examine what changes different commits made with `git diff`, and reorder them
with `git cherry-pick` or modify/combine them with `git rebase`.

### git add editor mode

How to use:

```
git add -e <name-of-file>
```

Like the interactive patch mode, `git add -e` allows you to selectively
stage certain changes in a file. But it's much better for keyboard jockeys
and those that love their text editor, because you can choose which changes
to stage or not using the text editor.

A sidebar:

If you have not yet set the text editor that git uses, you should
do that now. Modify your git configuration with this command:

```
git config --global core.editor vim
```

Alternatively, put the following in your `~/.gitconfig`:

```
[core]
    editor = vim
```

(Or, you know, whatever your text editor of choice is.)

End of sidebar.

When you pass the `-e` flag to git add, it will open a new editor window with the full diff:

```plain
diff --git a/doit.sh b/doit.sh
index 326273c..14e4059 100644
--- a/doit.sh
+++ b/doit.sh
@@ -1,17 +1,17 @@
 #!/bin/bash
 #
-# This script lists the 50 largest files in the git repo history
+# This script lists the 10 largest files in the git repo history

 $ git rev-list --all --objects | \
      sed -n $(git rev-list --objects --all | \
      cut -f1 -d' ' | \
      git cat-file --batch-check | \
      grep blob | \
      sort -n -k 3 | \
      \
-     tail -n50 | \
+     tail -n10 | \
      \
      while read hash type size; do
           echo -n "-e s/$hash/$size/p ";
      done) | \
-     sort -nru -k1
+     sort -nr -k1
```

**Editing this file requires some care!**

Fortunately there is a section in the documentation for
[git add](https://git-scm.com/docs/git-add) called
[Editing Patches](https://git-scm.com/docs/git-add#_editing_patches).

Two things to remember:

* Lines starting with `+` indicate new, added content. To prevent this
  content from being added, delete the line.

* Lines starting with `-` indicate removed content. To keep this content,
  replace `-` with a space (` `).

Once you are finished, make sure you review the changes that are staged,
particularly if this is the first time seeing patch files or the diff
syntax.

## Modifying Commits

There is always some reason or another to modify the commit history of a repository -
perhaps someone's work was lost, or the wrong issue or pull request number was referenced,
or a username was misspelled.

You can always modify a commit, but it will also modify every commit that came after it.
Think of it like replaying the changes recorded in each commit onto the new branch. The
contents of each commit changes slightly, so the hash (the name) of every commit changes.

### git rebase

To do a git rebase, an interactive rebase (the `-i` flag) is recommended.

The rebase action takes two commits, and will replay the commits.

**IMPORTANT:** The first commit given (the start commit) is _not_ included
in the rebase. To include it, add `~1` to the start commit. (For example,
`0a1b2c3d~1` refers to the commit before commit `0a1b2c3d`.

#### rebasing a range of commits

To rebase from the start commit hash to the end commit hash, and include the start commit
in the rebase, the rebase command is:

```
git rebase -i START_COMMIT_HASH~1 END_COMMIT_HASH
```

This does not indicate a destination branch. The default behavior is for the branch to move
and the new pile of commits to retain the same branch name.

#### rebasing onto another branch

To rebase a range of commits onto a different branch (for example, onto a `master` branch
that has the latest changes from the remote), use the `--onto` flag:

```
git rebase -i START_COMMIT_HASH END_COMMIT_HASH --onto TARGET_BRANCH
```

**IMPORTANT:** The above rebase commands will leave your repo in a headless state - unlike
the behavior of the prior command, the branch label will not move with you to the new pile
of commits.

Run `git checkout -b <branchname>` to give your new rebased branch a meaningful name.
This creates a branch wherever HEAD is, which is pointing to the top of the pile of rebased
commits.

If you want the old branch label to move to the new pile of commits, it requires a bit of branch
housekeeping - you have to delete the old branch, then create a new branch from where
HEAD is (the end of the rebase), then check out that branch.

```
git branch -D <branchname> && git checkout -b <branchname>
```

## Rearranging Commits

Where rebasing allows for editing commits en masse, cherry picking allows the changes made in
individual commits to be applied anywhere - including other branches. This makes the atomic
commit principle from the beginning of this post much easier - groups of related commits that
happened out of order can be rearranged by cherry picking them onto a new branch, and the new
branch is a better "story".

## Combining Commits

The cherry pick operation can also be combined with a rebase - once multiple small commits are
arranged together chronologically, a git rebase operation enables squashing those tiny commits
into a small number of larger commits, all carrying related changes.
