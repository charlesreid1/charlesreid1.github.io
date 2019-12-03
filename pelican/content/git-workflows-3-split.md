Title: Git Workflows, Part 3: Refactoring Large Pull Requests and Commits
Date: 2019-11-21 20:00
Category: Git
Tags: git, rebase, cherry-pick, branching, version control
Status: draft

# Table of Contents

* Summary
* Managing Complexity
* Refactoring Large Branches
* Refactoring Large Pull Requests
* Refactoring Large Commits

# Summary

* If a feature branch or pull request gets too complicated and should be refactored
  into simpler pieces:
    * Squash a set of commits together into a patch
    * Create a new feature branch from the original destination branch
    * Apply the patch to the new branch
    * Use `git add --patch` or `git add --edit` to selectively split out changes

* If a commit gets too large, you can rebase your branch, and mark that particular commit
  to be edited (`git rebase HASH_OF_COMMIT~1`). 
    * The rebase will replay that commit, and stage the changes, but will not 
      commit them, allowing you to edit the commit.
    * Use `git add --patch` or `git add --edit` to selectively split out changes
    * Remember you can also perform the same procedure on the resulting commits,
      further splitting each commit into sub-commits.

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

```plain
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

```plain
A - B - C (master)
    \
     D1 - E1 - D2 - F1 - E2 - F2 - D3 - F3 - E3 (feature)
```

to this:

```plain
A - B - C (master)
    \
     D - E - F
```

so that the changes in commits D, E, and F are simpler, more limited in scope, and easier to review.

### git format-patch

```
git format-patch
```

### squash and unstage






