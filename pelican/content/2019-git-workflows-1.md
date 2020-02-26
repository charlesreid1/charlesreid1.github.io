Title: Git Workflows, Part 1: Supercharging your Git Config
Date: 2019-10-07 20:00
Category: Git
Tags: git, rebase, cherry-pick, branching, version control

[TOC]

# Source

Most of the good stuff is from
<https://github.com/mathiasbynens/dotfiles>!

# User Section

Start off easy - here's how you set your email and name for commits:

```text
[user]
    email = foo@bar.com
    name = Foo Bar
```

# Bash Aliases

## The Best One Letter Alias Ever

Start supercharging how you use git by creating a one-letter alias.

Add this to your `~/.bashrc` file:

```text
alias g="git"
```

You're already saving yourself a bunch of keystrokes, and we're just getting started!

## Ending Bad Habits

This is a nice trick for getting yourself out of bad habits.
My first time using a "sophisticated" branch worklow in git
(i.e., not just committing and pushing to master all the time),
I got in trouble for committing directly to master with a
`git push origin master` (instead of making a feature branch
and opening a pull request).

To get myself out of the habit of typing `git push origin master`,
I wanted to map it to an alias that told me no. I did that by
defining `git` to be a bash function (this works because functions
take precedence over a binary named `git` on your path).

The git function checks the arguments that are passed to it.
If the arguments are `push origin master`, it means I'm typing
`git push origin master`, and I get a slap on the wrist.

Otherwise, it passes the arguments through to the `git` binary.

You can also put this in `~/.bashrc`.

```bash
git() {
    if [[ $@ == "push origin master" ]]; then
        echo "nope"
    else
        command git "$@"
    fi
}
```

# Alias section

In the `~/.gitconfig` file, aliases specific to git can be
defined in a section beginning with alias.

## Log Utils

Let's start with some utilities for viewing git logs.

(You can never have too many ways to look at a git log.)

Note that we'll assume the alias bit in the following git config excerpts.

```text
[alias]
    # courtesy of https://stackoverflow.com/a/34467298
    lg = !"git lg1"
    lg1 = !"git lg1-specific --all"
    lg2 = !"git lg2-specific --all"
    lg3 = !"git lg3-specific --all"

    lg1-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(auto)%d%C(reset)'
    lg2-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(auto)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)'
    lg3-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset) %C(bold cyan)(committed: %cD)%C(reset) %C(auto)%d%C(reset)%n''          %C(white)%s%C(reset)%n''          %C(dim white)- %an <%ae> %C(reset) %C(dim white)(committer: %cn <%ce>)%C(reset)'
```

The `git lgX` shortcuts give similar views of the log, but with increasing vertical spacing.
`git lg1` is the most compact, while `git lg3` is the most comfortable to read, as far as vertical whitespace.
Same with the `-specific` commands.

This is one more nice short log command:

```text
    # View abbreviated SHA, description, and history graph of the latest 20 commits
    l = log --pretty=oneline -n 20 --graph --abbrev-commit
```

Remember to use this with the `g` alias for super short log:

```text
$ g l
* 4357b28 (HEAD -> source) update mocking aws post
* 063ad78 (gh/source, gh/HEAD) add mocking post
* a5f1adc add init keras cnn post
* fb911ec add keras cnn draft
* 3549d35 add rosalind (euler paths) part 7 draft

$ g lg1
* 4357b28 - (67 minutes ago) update mocking aws post - Charles Reid (HEAD -> source)
* 063ad78 - (2 weeks ago) add mocking post - Charles Reid (gh/source, gh/HEAD)
* a5f1adc - (4 months ago) add init keras cnn post - C Reid
* fb911ec - (5 months ago) add keras cnn draft - C Reid
* 3549d35 - (5 months ago) add rosalind (euler paths) part 7 draft - C Reid
...
```

## Status Utils

The git status command is one of my most frequently used commands, so I made a few shortcuts:

```text
    # View the current working tree status using the short format
    s = status -s
    ss = status
```

This makes checking the short or long status of a git repo easy:

```text
$ g s
AM pelican/content/git-workflows-1-config.md
AM pelican/content/git-workflows-2-teams.md

$ g ss
On branch source
Your branch is ahead of 'gh/source' by 1 commit.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   pelican/content/git-workflows-1-config.md
	new file:   pelican/content/git-workflows-2-teams.md

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   pelican/content/git-workflows-1-config.md
	modified:   pelican/content/git-workflows-2-teams.md
```

## Fetching

Fetching is handy to do, since it just fetches changes from a remote and doesn't actually
change anything or try to merge anything (unlike a `git pull` command).

The most useful fetch command (`git fetch --all`) is aliased to `g f` with the following
bit in the aliases section of the `~/.gitconfig` file:

```text
    f = fetch --all
```

## Branch Utils

The only command I might use more than the status command are branch commands,
so here are several branch aliases:

```text
    b = branch -v
    bv = branch -v
    bb = branch -v

    ba = branch -a
    bb = branch -v -a
```

In a similar way, you can get a summary view using `g b`:

```text
$ g b
  master 4c828cd [behind 84] update with awsome day notes
* source b18adfd add two git workflow posts

$ g b
  master 940ee98 update mocking post
* source b18adfd add two git workflow posts
```

and a little bit more information with `g bb`:

```text
$ g bb
  master            940ee98 update mocking post
* source            b18adfd add two git workflow posts
  remotes/gh/HEAD   -> gh/source
  remotes/gh/master 940ee98 update mocking post
  remotes/gh/source b18adfd add two git workflow posts
```

### Branch and Checkout

Sometimes if you are creaing a branch with a long branch name, it can be
inconvenient to have to first create the branch with `git branch <branch-name>`
and then check it out with `git checkout <branch-name>`.

To resolve this you can define a `git go` alias that creates the branch and
then switches to that branch:

```text
    # Switch to a branch, creating it
    # from the current branch if necessary
    go = "!f() { git checkout -b \"$1\" 2> /dev/null || git checkout \"$1\"; }; f"
```

Careful you don't mistype the branch name.

## Remote Utils

Another useful git command is the remote command, so here are a few
remote aliases:

```text
    r = remote -v
    rv = remote -v
    ra = remote -v
```

## Commit Utils

Sometimes you have changes that you've staged using `git add`, but you
want to see the changes that you've staged, before you commit them.

Normally you'd have to use the inconvenient `git diff --cached <files>`,
but this can be aliased to `cdiff`, so that you can use `git diff` to see
unstaged changes and `git cdiff` to see staged changes.

Even better, you can define the alias `g cd` to run `git cdiff`...!

Here's the relevant bit in the aliases section:

```text
    cdiff = diff --cached
    cd = diff --cached
```

### Committing All Changes

```text
    # Commit all changes
    ca = !git add -A && git commit -av
```

### Fixing Commits

Some common operations for repairing commit history before pushing:

```text
    # Amend the currently staged files to the latest commit
    amend = commit --amend --reuse-message=HEAD

    # Oops
    fix = commit --amend --reuse-message=HEAD --edit
```

## Miscellaneous Utils

There are a few other actions that are useful to add to the aliases section
of the `~/.gitconfig`:

### Rebasing shortcuts

```text
    # Interactive rebase with the given number of latest commits
    reb = "!r() { git rebase -i HEAD~$1; }; r"
```

### Diff shortcuts

```text
    # Show the diff between the latest commit and the current state
    d = !"git diff-index --quiet HEAD -- || clear; git --no-pager diff --patch-with-stat"

    # `git di $number` shows the diff between the state `$number` revisions ago and the current state
    di = !"d() { git diff --patch-with-stat HEAD~$1; }; git diff-index --quiet HEAD -- || clear; d"
```

### Pull shortcuts

```text
    p = "!f() { git pull $1 $2; }; f"
```

### Clone shortcuts

```text
    # Clone a repository including all submodules
    c = clone --recursive
```

### Contributor shortcuts

This last one is convenient for getting a summary of contributors:

```text
    # List contributors with number of commits
    contributors = shortlog --summary --numbered
```

An example for <https://github.com/aws/chalice>:

```text
$ cd chalice/
$ g contributors
  1053  James Saryerwinnie
   120  John Carlyle
    94  stealthycoin
    42  kyleknap
    35  jcarlyl
    19  Kyle Knapp
    12  Atharva Chauthaiwale
```

# Core section

Because it's the best text editor:

```text
[core]
    editor = vim
```

I have some other stuff I've collected, many of them from
<https://github.com/mathiasbynens/dotfiles>:

```text
    # Use custom `.gitignore` and `.gitattributes`
    excludesfile = ~/.gitignore
    attributesfile = ~/.gitattributes

    # Treat spaces before tabs and all kinds of trailing whitespace as an error
    # [default] trailing-space: looks for spaces at the end of a line
    # [default] space-before-tab: looks for spaces before tabs at the beginning of a line
    whitespace = space-before-tab,-indent-with-non-tab,trailing-space

    # Make `git rebase` safer on macOS
    # More info: <http://www.git-tower.com/blog/make-git-rebase-safe-on-osx/>
    ###trustctime = false

    # Prevent showing files whose names contain non-ASCII symbols as unversioned.
    # http://michael-kuehnel.de/git/2014/11/21/git-mac-osx-and-german-umlaute.html
    precomposeunicode = false

    # Speed up commands involving untracked files such as `git status`.
    # https://git-scm.com/docs/git-update-index#_untracked_cache
    untrackedCache = true
```

# Color section

Make some nice beautiful colors that are easy to understand:

```text
[color]

    # Use colors in Git commands that are capable of colored output when
    # outputting to the terminal. (This is the default setting in Git ≥ 1.8.4.)
    ui = auto

[color "branch"]

    current = yellow reverse
    local = yellow
    remote = green

[color "diff"]

    meta = yellow bold
    frag = magenta bold # line info
    old = red # deletions
    new = green # additions

[color "status"]

    added = yellow
    changed = green
    untracked = cyan
```

# Url section

This makes some Github-related URLs easier and shorter to type:

```text
[url "git@github.com:"]

    insteadOf = "gh:"
    pushInsteadOf = "github:"
    pushInsteadOf = "git://github.com/"

[url "git@gist.github.com:"]

    insteadOf = "gst:"
    pushInsteadOf = "gist:"
    pushInsteadOf = "git://gist.github.com/"

[url "git://gist.github.com/"]

    insteadOf = "gist:"
```

Now, instead of

```text
$ git clone git@github.com:org-name/repo-name
```

you can do the much simpler

```text
$ g c gh://org-name/repo-name
```

Voila! Start integrating these alises into your daily workflow,
and you'll find yourself using a lot fewer keystrokes!
