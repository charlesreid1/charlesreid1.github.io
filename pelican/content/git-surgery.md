Title: Performing a Git-Commit-Ectomy
Date: 2018-05-12 15:00
Category: Git
Tags: git, rebase, cherry-pick, branching, version control
Status: draft

scenario

## simple version walkthrough

High-level description/summary of steps

Link to repo

## multi-branch walkthrough 

Multiple branches cause complications

Patch branches, existing pull requests

How to handle multiple branches? 

- clear out the undergrowth (dead branches)
- identify and tag split point: where does existing branch diverge?
- identify and tag join point: where to join on new branch?
- git rebase join-here split-here patch-branch

## cherry pick walkthrough

blog repo problem:
    - originally forked from octopress repo with long history
    - lots of crap 
    - abandoned octopress and ruby in favor of python
    - git.charlesreid1.com wasting a gigabyte of space on crap

blog repo solution:
    - identify the zero/empty commit
    - rebase or cherry pick only the commits we want, toss out the rest

try to rebase first:
    - if successful, easiest solution
    - this may fail - need to apply commits to branches one at a time
    - usually happens if there is one particular set of commits that diverge and are merged
    - cherry pick all the commits up to a particular complicated point 
    - handle complicated situations by hand
    - cherry pick all the rest of the commits

to cherry pick lots of commits at once:
    - git log to a file
    - tail -r to reverse file
    - turn it into bash script
    - run git cherry-pick commit-hash

merge problems: 
    - conflicts may arise with split/merge commits
    - command to abort cherry pick: git cherry-pick --abort
    - command to undo one commit at a time: git 
    - these commands allow you to try different ways of cherry picking problematic commits
    - try these commits, try those commits

bypassing merge problems:
    - worst case scenario: stop at a particular point, hop over merge commits, use github or another copy of the repo 
    - copy the _exact_ state of the repo at a particular commit 
    - literally, exactly, trailing whitespaces and newlines and all
    - you can have extra files, but if a file was in the repo at that commit, it must match exactly
    - now begin the cherry-picking operation from the next commit

