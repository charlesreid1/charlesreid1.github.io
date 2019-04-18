Title: The Git-Commit-Ectomy
Date: 2019-04-17 12:00
Category: Git
Tags: git, rebase, cherry-pick, branching, version control

TLDR: Visit the git-commit-ectomy guide: <http://pages.charlesreid1.com/git-commit-ectomy>

<br />

Consider the following _completely hypothetical_
scenario.

Suppose you've been working for a while on your latest
invention, a brand-new whiz-bang command line
tool that's fast and solves an important problem
and you're chugging your way to the finish line.

As part of preparing to release your software tool,
you add some tests, because that's what you do.

Those tests require some data, so you add a few test
data sets, a few hundred kilobytes each, nothing fancy.

Then one day, **the intern** (who is just trying to be 
helpful by adding a new test) slips in a 70 MB test
data set, and slips it in with a string of commits
that somehow get incorporated into the master branch.

(Side note: you turned on branch protection to prevent
this whole mess, didn't you? _Didn't you??_ 
'Course you did. This is all
just a hypothetical scenario.)

Now, the situation is complicated: there are several
open pull requests and active branches, and a non-trivial
amount of history that's been added since the time the
large test data set was accidentally added.

**The intern** apologizes profusely and promises to 
bring in donuts every day next week. But the damage 
is done.

**The intern**, a git novice, pulls out a laptop
and runs a `git rm` on the files, pushing to the
remote and happily, ignorantly believing the problem
has been solved.

But **the intern** does not understand how git works.
It has a perfect memory, and remembers every file in
every commit. Since the problematic first commit that
added the large files, git has remembered and will always
remember that large file. It's in git's blood. 
It's what git was designed to do.

Once the intern has been, ahem, moved along,
and branch protection has been turned on,
it's time to find a git surgeon to perform a 
git-commit-ectomy to remove the problematic
large files from the repository entirely.


## Dr. Reid's Patented Git-Commit-Ectomy

If it's a git-commit-ectomy you need,
try Dr. Reid's Patented Git-Commit-Ectomy
to ease your git commit pains.

Whether you want to keep thing simple
and remove a git commit from a single branch,
or if you've got multiple branches, Dr. Reid's
Patented Git-Commit-Ectomy will get you back
on your feet.

Dr. Reid's Patented Git-Commit-Ectomy can handle
even the most messy, confused, and tangled git 
commit history - with a bit of work and a gifted
surgeon the git-commit-ectomy can smooth things 
out and get you feeling right as rain.

Visit the git-commit-ectomy guide: <http://pages.charlesreid1.com/git-commit-ectomy>

