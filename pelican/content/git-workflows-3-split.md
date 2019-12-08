Title: Git Workflows, Part 3: Refactoring Large Pull Requests and Commits
Date: 2019-12-08 15:00
Category: Git
Tags: git, rebase, cherry-pick, branching, version control

# Table of Contents

* [Summary](#summary)
* [Managing Complexity](#managing-complexity)
* [Refactoring Large Branches](#refactoring-large-branches)
  * [Converting Set of Commits to Unstaged Changes](#converting-set-of-commits-to-unstaged-changes)
    * [git format\-patch](#git-format-patch)
    * [cherry\-pick and unstage](#cherry-pick-and-unstage)
    * [soft reset and commit](#soft-reset-and-commit)
* [Refactoring Large Pull Requests](#refactoring-large-pull-requests)
  * [Chaining Pull Requests](#chaining-pull-requests)
  * [Preparing to Merge a Large Pull Request](#preparing-to-merge-a-large-pull-request)
  * [Rinse and Repeat](#rinse-and-repeat)
  * [Final Merge into Master](#final-merge-into-master)

# Summary

* If a feature branch or pull request gets too complicated and should be refactored
  into simpler pieces:
    * Create a new feature branch from the original destination branch
    * Turn commits into patches, or cherry-pick commits (leaving changes unstaged)
    * Apply patches or cherry-picks to the feature branch
    * Use `git add --patch` or `git add --edit` to selectively split out changes into separate commits

* If a commit gets too large, you can rebase your branch, and mark that particular commit
  to be edited (`git rebase HASH_OF_COMMIT~1`). 
    * The rebase will replay that commit, and stage the changes, but will not 
      commit them, allowing you to edit the commit.
    * Use `git add --patch` or `git add --edit` to selectively split out changes
    * Remember you can also perform the same procedure on the resulting commits,
      further splitting each commit into sub-commits.

This post contains many common patterns applied to different workflows.

# Managing Complexity

When collaborating on software, especially large software with people who are not the
primary developers, it is important to limit the complexity of features and proposed
changes. Why is it bad practice to propose large, complex changes?

* It is harder to review the proposed changes
* Bugs increase in likelihood, and increase in likelihood far faster than the amount of code.
* More complex changes usually combine 

# Refactoring Large Branches

Consider the case of a large feature branch that is suffering from feature creep (trying to
cram too many changes into one branch.) For example, in the process of implementing a feature,
you may also implement significant fixups, refactoring of functions, and code cleanup that is
in the same file but not entirely related. While writing tests for the new feature, you may also
refactor tests to be cleaner, or to use context manager foobar, or etc.

To illustrate: suppose you are on a branch called `feature` (created off of `master`) that consists of
three sets of changes, DEF:

```text
A - B - C (master)
    \
     D1 - E1 - D2 - F1 - E2 - F2 - D3 - F3 - E3 (feature)
```

* D corresponds to implementing the new feature and writing tests for it
* E corresponds to fixups to the same file that was changed to implement the feature
* F corresponds to fixups to tests unrelated to the new feature

Now, in reality, if things were really so clean, if you had a time machine or the patience to
to rebase commits one at a time and split them into atomic changes only to the features in their
scope (which would be super easy because of course your git logs are filled with helpful, concise
commit messages) you could use `git cherry-pick` to replay commits D1, D2, D3 onto a new D
branch, and so on. 

But in reality, commit F1 contains a little bit of E1, and D2, and vice versa, and so on.
It's much easier to navigate a diff and select pieces from it.  That's were `git add -e`
(or `--edit`) will help.

We also have to turn a set of commits into a single set of unstaged changes (meaning, replay
the changes each commit made but not replay the commits themselves). There are a few ways
to do this, we'll cover two ways: squashing and rolling back a set of commits, and converting
a set of commits into a set of patch files.

Once the commits have been rolled back and unstaged, particular changes can be staged for each
split commit using `git add -e` and using the editor to select which changes to include or exclude
from the commit. As each commit is created, branches can be created that are linked to the group
of changes in each new commit.

## Converting Set of Commits to Unstaged Changes

We are trying to untangle a set of unrelated changes into separate commits that group related
changes together. For the example, we want to convert this:

```text
A - B - C (master)
    \
     D1 - E1 - D2 - F1 - E2 - F2 - D3 - F3 - E3 (feature)
```

to this:

```text
A - B - C (master)
    \
     D - E - F (feature)
```

so that the changes in commits D, E, and F are simpler, more limited in scope, and easier to review.

### git format-patch

To create a set of patches, one per commit, to edit them or apply them in various orders,
you can use `git format-patch` with a commit range:

```text
git format-patch D1..E3
```

This will create a series of patches like 

```text
patches/0001-the-D1-commit-message.patch
patches/0001-the-E1-commit-message.patch
patches/0001-the-D2-commit-message.patch
patches/0001-the-F1-commit-message.patch
patches/0001-the-E2-commit-message.patch
patches/0001-the-F2-commit-message.patch
patches/0001-the-D3-commit-message.patch
patches/0001-the-F3-commit-message.patch
patches/0001-the-E3-commit-message.patch
```

Patches can be further split or modified, and can be applied in the desired order (although
changes in line numbers happening out of order may confuse the program applying the patch).

Start by creating a branch from the desired commit (commit `B` in the diagram above):

```text
git checkout B
```

(where `B` should be either the commit hash for commit B, or a tag or branch that is associated
with commit B). Now create a branch that will start from that commit (we'll start with our branch
for feature D here):

```text
git checkout -b feature-d
```

Now apply patches to the new branch, which will start from commit `B`.

To apply a patch, use `patch -p1`:

```text
patch -p1 < 0001-the-D1-commit-message.patch
```

The `-p1` strips the prefix by 1 directory level, which is necessary with patches created
by git. We use `patch` rather than `git am` to apply the patch, because we want to apply
the changes independent of git, and only stage the changes we want into our next commit.

If you have a series of commits that you want to squash, that's also easy to do by applying
each patch for those commits, then staging all the changes from those patches into a new
commit.

As patches are applied, particular changes can be staged and commits can be crafted. Use 
the `--edit` or `--patch` flags of `git add`:

```text
git add --edit <filename>
git add --patch <filename>
```

This allows selective filtering of particular edits into the next commit, so that one patch
(or any number of patches) can be applied, and selective changes can be staged into a commit.

Once you are ready, just run

```text
git commit
```

without specifying the filename. (If you specify the filename, it will stage all changes,
and ignore the crafting you've done.)

As you create a commit or a set of commits specific to changeset D, you can work on a D branch.
When you finish all commits related to D, you can start a new branch with

```text
git checkout feature-e
```

that will start a new branch from where the d-branch left off. Chaining your
changes together into several small branches that build on each other will 
help keep pull requests simpler too.

The advantages of this approach include:

* Commits can be split by applying the patch and staging particular edits
* The ability to split single commits into more commits, or combine/squash commits together, means
  this approach has a lot of flexibility
* Best for some situations where, e.g., a long series of commits with many small commits that should
  be squashed and some large commits that should be split 

The disadvantages of this approach include:

* Patches applied out of order can confuse the program applying the patches

### cherry-pick and unstage

An alternative to the above workflow is to use `git cherry-pick` to apply the changes from particular
commits, but to leave those changes unstaged using the `--no-commit` or `-n` flag:

```text
git cherry-pick --no-commit <commit-hash>
git cherry-pick -n <commit-hash>
```

Alternatively, a range of commits can be used instead:

```text
git cherry-pick -n <commit-hash-start>..<commit-hash-end>
```

This can help achieve a similar level of flexibility to the patch approach.

### soft reset and commit

Suppose the commit history is simple enough that you can squash all of the commits together
into a single diff set, and pick the changes to split into commits D, E, and F.

In that case, the easiest way might be to roll back all of the commits made, but preserve
the changes that each commit made. This is precisely what a _soft reset_ will do.

For the git commit history

```text
A - B - C (master)
    \
     D1 - E1 - D2 - F1 - E2 - F2 - D3 - F3 - E3 (feature)
```

Run the command

```text
git reset --soft B
```

to move the HEAD pointer to commit B, while also _preserving_ all changes made from the
start of the feature branch `D1` to the tip of the feature branch `E3`, all added as
staged changes (as though they had been `git add`-ed).

The changes will be staged, but changes to files can be unstaged using

```text
git restore --staged <filename>
```

Now add changes selectively using the `--edit` or `--patch` flags

```text
git add --edit <filename>
git add --patch <filename>
```

If desired, those changes can be unstaged, and then re-staged using `git add --edit` or
`git add --patch` to selectively add changes to particular commits.

When done, run 

```text
git commit
```

with no arguments to commit the changes you made.

# Refactoring Large Pull Requests

The approaches above can be useful for refactoring branches. The end result will look something like this:

```text
A - B - C (master)
    \
     D (feature-d)
      \ 
       E (feature-e)
        \
         F (feature-f)
```

Now 3 pull requests can be made, one for each feature. Thanks to the refactoring above, each branch
should be a more isolated set of changes that are all related, and therefore easier to review.

## Chaining Pull Requests

The three D E F branches should be merged in together, since they are all related. But their changes should
be kept separate to make reviewing each branch easier. To accomplish this, chain the pull requests together
like so:

Pull Request 1: merge `feature-d` into `master`

Pull Request 2: merge `feature-e` into `feature-d`

Pull Request 3: merge `feature-f` into `feature-e`

In this way, each pull request only shows the changes specific to that branch.

(If each pull request were made against `master`, then later branches (F) would also incorporate changes
from prior branches (D), resulting in messy and hard-to-review pull requests.)

Pull requests are reviewed and discussed, and new commits will probably be added to fix things or incorporate
feedback:

```text
A - B - C (master)
    \
     D - DA - DB (feature-d)
      \ 
       E - EA - EB (feature-e)
        \
         F - FA - FB (feature-f)
```

## Preparing to Merge a Large Pull Request

All of your pull requests are approved and ready to merge. Now what?

Pull requests will need to be merged in reverse order (last PR is merged first - f into e, e into d, d into
master).  To test that things go smoothly with the first pull request (`feature-f` into `feature-e`), we should
create a local E-F integration branch.

The local integration branch will have new commits if changes are needed to resolve merge conflicts or fix
broken tests. Any changes made can be added to the `feature-f` branch and pushed to the remote, so that
they are part of the pull request, making the merge into `feature-e` go smoothly.

To create a throwaway E-F integration branch, we start by creating a test integration branch from the tip of the
`feature-f` branch, and we will merge branch `feature-e` into branch `feature-f`.

```text
git checkout feature-f
```

Now we create a local E-F integration branch:

```text
git checkout -b integration-e-f
```

Now we merge `feature-e` into `integration-e-f`, which is the same as `feature-f`:

```text
git merge --no-ff feature-e
```

The `--no-ff` flag creates a separate merge commit, which is useful here to keep our commit history clean.

If merge conflicts are encountered, those can be resolved in the usual manner, and the (conflict-free) new
versions of each file, reflecting changes from `feature-f` and `feature-e`, will all be present after the
merge commit.

Further commits can also be made to make tests pass, with a resulting git diagram:

```text
A - B - C (master)
    \
     D - DA - DB (feature-d)
      \ 
       E - EA - EB ----
        \              \
         F - FA - FB - EF1 - EF2 (integration-e-f)
                              ^
                             HEAD
```

Once the `integration-e-f` branch is polished and passing tests, we can re-label it as `feature-f` and push
the new commits to the remote. To re-label `integration-e-f` as `feature-f`, assuming we're at the tip of
the `integration-e-f` branch (where we left off above):

```text
git branch -D feature-f
git checkout -b feature-f
```

and push the new commits to the remote's `feature-f` branch, before you merge in the pull request (`feature-f`
into `feature-e`):

```text
git push origin feature-f
```

Now you are ready to merge pull request 3 (F into E).

## Rinse and Repeat

Rinse and repeat for pull requests 2 and 1.

For Pull Request 2, we start by creating a new `integration-d-e-f` branch from the tip of the
`integration-e-f` branch, like so:

```text
git checkout integration-d-e
git checkout -b integration-d-e-f
```

and use the same approach of merging in the `feature-d` branch with an explicit merge commit:

```text
git merge --no-ff feature-d
```

Work out any merge conflicts that result, and add any additional changes needed to get tests passing,
and you should now have a git commit history like this:


```text
A - B - C (master)
    \
     D - DA - DB ----------------
      \                          \
       E - EA - EB ----           \
        \              \           \
         F - FA - FB - EF1 - EF2 - DEF1 - DEF2 (integration-d-e-f)
                                            ^
                                           HEAD
```

Now re-label the `integration-d-e-f` branch as `feature-e`:

```text
git branch -D feature-e && git checkout -b feature-e
```

Finally, push all new commits to the remote, including the new merge
commit, which will make sure the pull request can be merged without
any conflicts:

```text
git push origin feature-e
```

Now PR 2 (E into D) can be merged.

## Final Merge into Master

The last and final PR, D into master, will merge all combined feature
branches into the master branch. We start with a `feature-d` branch
that has several commits related to feature D, then several commits
from merging the `feature-e` branch in (pull request 2, E into D),
and the `feature-e` branch also had `feature-f` merged into it.

```text
A - B - C (master)
     \
      D - D2 - DEF1 - DEF2 (feature-d)
```

Now we will create one more commit on the `feature-d` branch that is
merging `master` into `feature-d`, which will help the merge happen
smoothly for pull request 1 (D into master).

But first we switch to an integration branch, in case things don't go
smoothly and we want to throw away the merge commit:

```text
git branch integration-def-master
```

Create an explicit merge commit to merge `master` into `integration-def-master`:

```text
git merge --no-ff master
```

Work out any merge conflicts that result, and add any additional changes needed to get tests passing,
and you should now have a git commit history like this:

```text
A - B - C (master)
     \   \---------------------
      \                        \
       D - D2 - DEF1 - DEF2 - DEF3 (integration-def-master)
```

where commit `DEF3` is the merge commit created with the `--no-ff` command.

The merge commit will resolve any conflicts. When you're satisfied with the
merge commit, you can switch out the `integration-def-master` branch with the
`feature-d` branch like so:

```text
git branch -D feature-d
git checkout -b feature-d
```

Now you can push the merge commit to the remote:

```text
git push origin feature-d
```

and you're now ready to merge your (conflict-free) pull request!
