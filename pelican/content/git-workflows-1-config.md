Title: Git Workflows, Part 1: Supercharging your Git Config
Date: 2019-10-07 20:00
Category: Git
Tags: git, rebase, cherry-pick, branching, version control
Status: draft

# `[user]` section

Start off easy - here's how you set your email and name for commits:

```plain
[user]
    email = foo@bar.com
    name = Foo Bar
```

# Bash Aliases

## The Best One Letter Alias Ever

Start supercharging how you use git by creating a one-letter alias.

Add this to your `~/.bashrc` file:

```plain
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

# `[alias]` section

In the ~/.gitconfig` file, aliases specific to git can be 
defined in a section beginning with `[alias]`.

## Log Utils

Let's start with some utilities for viewing git logs.

(You can never have too many ways to look at a git log.)

Note that we'll assume the `[alias]` bit in the following git config excerpts.

```plain
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

```plain
    # View abbreviated SHA, description, and history graph of the latest 20 commits
    l = log --pretty=oneline -n 20 --graph --abbrev-commit
```

Remember to use this with the `g` alias for super short log:

```plain
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

```plain
    # View the current working tree status using the short format
    s = status -s
    ss = status
```

This makes checking the short or long status of a git repo easy:

```plain
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

## Branch Utils

## Commit Utils

# `[core]` section

# `[color]` section

# `[url]` section

