Title: Git Workflows, Part 3: Refactoring Large Commits
Date: 2019-12-08 16:00
Category: Git
Tags: git, rebase, cherry-pick, branching, version control
Status: draft

# Table of Contents

* Summary
* Refactoring Large COmmits
    * Rebase to edit
    * Selectively stage changes
    * Going deeper: recursively rebasing

# Summary

* If a commit gets too large, you can rebase your branch (`git rebase HASH_OF_COMMIT~1`):
    * Mark the commit to be modified 
    * The rebase will replay that commit, and stage the changes, but will not 
      commit them, allowing you to edit the commit.
    * Use `git add --patch` or `git add --edit` to selectively split out changes
    * Remember you can also perform the same procedure on the resulting commits,
      further splitting each commit into sub-commits.


