Title: Git Workflows, Part 2: Crafting Commits
Date: 2019-11-14 20:00
Category: Git
Tags: git, rebase, cherry-pick, branching, version control

[TOC]

# Summary

* Make your commits small and atomic, and recombine them into
  larger commits later; it's easier to combine smaller commits
  than to split large commits.

* Make use of `git add -p` and `git add -e` to stage
  changes selectively and atomically.

* Make use of `git rebase` and `git cherry-pick` to edit your
  commits and assemble them in the order you want.

* Once commits have been combine and the history is satisfactory,
  push to a remote to share the work.

* Think about ordering your commits to "tell a story". (What that
  means will depend on the people you are collaborating with!)

# What is a commit

Before we get into the good stuff, let's talk about the
anatomy of a git commit.

When you add files to your git repository, it's a two-step
process: `git add` and `git commit`. The first step _stages_
your changes, the second step memorializes those staged changes
into a commit that can now be shared with others by pushing it
to git remotes.

## git add

Under the hood, git stores the full contents of each file at each snapshot
in an object called a _blob_. When you modify a file and run `git add`,
git writes a new blob containing the entire new contents of the file, and
updates the staging area (the index) to point at that new blob. The diff
between the old and new versions is not stored — it is computed on demand
by comparing the two blobs.

That said, when using tools like `git add -p`, `git diff`, and `git log -p`,
git presents changes at the line (hunk) level. This makes it useful to
think about staging in terms of individual line changes, even though the
underlying storage is snapshot-based. That line-level view is what makes
it possible to stage some hunks in a file but not others — the resulting
blob reflects only the hunks you accepted.

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

This leaves the developer of the feature branch (which is out of sync with master) with a few choices:

* **rebase** - continue to rebase all commits on the feature branch from the
  (old) original feature branch base commit onto the (new) head commit of the master 
  branch.
    * Pros: clean history, easy for one-branch-one-developer workflow
    * Cons: requires continual force-pushes, requires coordination between developers
      to prevent squashing others' work, not scalable, some people hate this method

* **merge** - occasionally merge work from the master branch into the feature branch.
    * Pros: simple to understand, simple to carry out, low cognitive load
    * Cons: any changes added to the branch via the merge commit will show up in the PR
      as new code, cluttering PR reviews by mixing features with merged changes; can also
      make the commit history messy and harder to understand.

* **branch** - by making heavy use of throwaway branches and integration branches,
  it is easier to test out how the integration of a feature branch based on an old
  commit on `master` will do when merging it in with a newer version of `master`.
  Use throwaway integration branches to test out merging the two branches together,
  testing its functionality, etc. You can also rebase or cherry pick commits onto
  the throwaway integration branch, and figure out how to arrange the commits on a
  branch to "rebuild" it into a working, mergeable branch.
    * Pros: easy to do, encourages local use of throwaway branches
    * Cons: clutters branches, integration process has to be repeated (can be mitigated
      with `git rerere`), merge commits must wait until PR is approved

- **pass** - best combined with the branch approach mentioned above, the pass approach
  is to leave the branch history clean, avoid force-pushes, and rely on throwaway
  branches to test out merge strategies once the inevitable PR merge needs to happen.
  It can also be useful to wait for code reviews to finish, then create a merge commit
  to make the merge happen smoothly.
    * Pros: easy to do
    * Cons: merge commits must wait until PR is approved

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
why some people hate it - in a later post. For now, we will only say
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

```text
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

```text
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

There are two related changes and one unrelated change, respectively:
the two related changes are the change to the comment and the change
to the `tail` command; the unrelated change is adding the `-u` flag
to the `sort` command.

We can split these changes into two commits using `git add -p doit.sh`,
which will walk through each change in the file and ask if we want to
stage it:

```text
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

```text
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

Run `git commit` with no filenames. If you pass a filename like
`git commit doit.sh`, git will commit the current working-tree contents
of that file directly, bypassing the index entirely — throwing away the
careful hunk-by-hunk staging you just did and committing the unstaged
changes too.

To use this in your workflow, think about how you can group different changes together into
different commits. If you get a portion of a feature working, you can commit the changes in
groups so that related changes get committed together.

Also remember that if your commit history ends up being excessively long or overly detailed,
you can always examine what changes different commits made with `git diff`, and reorder them
with `git cherry-pick` or modify/combine them with `git rebase`.

### git add editor mode

How to use:

```text
git add -e <name-of-file>
```

Like the interactive patch mode, `git add -e` allows you to selectively
stage certain changes in a file. But it's much better for keyboard jockeys
and those that love their text editor, because you can choose which changes
to stage or not using the text editor.

A sidebar:

If you have not yet set the text editor that git uses, you should
do that now. Modify your git configuration with this command:

```text
git config --global core.editor vim
```

Alternatively, put the following in your `~/.gitconfig`:

```text
[core]
    editor = vim
```

(Or, you know, whatever your text editor of choice is.)

End of sidebar.

When you pass the `-e` flag to git add, it will open a new editor window with the full diff:

```text
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

The general form of a rebase is:

```text
git rebase [-i] <upstream> [<branch>]
```

If `<branch>` is given, git checks it out first. Then it takes every commit
that is reachable from `<branch>` but not from `<upstream>` and replays them
on top of `<upstream>`.

**IMPORTANT:** The `<upstream>` commit itself is _not_ replayed - it is the
new base. If you want to include a specific commit in the rebase, use its
parent as `<upstream>`. For example, `0a1b2c3d~1` refers to the commit
before `0a1b2c3d`, so `git rebase -i 0a1b2c3d~1` will replay `0a1b2c3d`
and everything after it on the current branch.

#### rebasing the last N commits of a branch

The most common form of interactive rebase is "let me edit the last N commits
on my branch":

```text
git rebase -i HEAD~N
```

For example, `git rebase -i HEAD~5` replays the last 5 commits on top of
their existing base, giving you an editor where you can reorder, squash,
edit, or drop them.

#### rebasing onto another branch

To move a range of commits so they start on top of a different branch
(for example, on top of the latest `master`), use the `--onto` flag:

```text
git rebase --onto <newbase> <upstream> [<branch>]
```

`<newbase>` is where the commits will be replayed. `<upstream>` is the
commit whose descendants get replayed (and `<upstream>` itself is _not_
included). If `<branch>` is provided, git checks it out first before
starting the rebase.

For example, suppose you have a `feature` branch that was branched off an
old `master`, and you want to move its commits on top of the current
`master`:

```text
git rebase --onto master feature~3 feature
```

This replays the last 3 commits of `feature` on top of `master`, and
because `feature` was supplied as `<branch>`, the `feature` label moves
with the rebased commits — no headless state, no branch housekeeping
needed.

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
