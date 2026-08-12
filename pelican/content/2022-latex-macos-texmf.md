Title: Installing LaTeX Packages on macOS: The `~/Library/texmf` Layout
Date: 2022-06-19 20:00
Category: LaTeX
Tags: latex, mac, tex, texmf, packages

Every few years, we find ourselves installing a new LaTeX package on a Mac,
and every few years, we find ourselves searching for the same set of directory
paths, the same `texhash` invocation, and the same reminders that the LaTeX
package installer is not, in fact, going to create any directories for us.

So this post is here mostly as a note to our future selves.

## Where TeX Looks First

We use MacTeX (<http://www.tug.org/mactex/>), and MacTeX installs its files
under `/usr/local/texlive/`. That is the system-wide `texmf` tree.

Personal TeX files should not go there. They should go under
`~/Library/texmf`, which is your user-level `texmf` tree. When TeX needs to
find a file, it looks in `~/Library/texmf/` first, and the system-wide `texmf`
second. So if you drop a modified version of a system file into your user
tree, the modified version wins.

## The Directory Layout

The folder structure inside `~/Library/texmf` should mirror the structure
of the system `texmf` tree. Here is where different kinds of files go:

* TeX files: `~/Library/texmf/tex` (or any subfolder of it)
* LaTeX files: `~/Library/texmf/tex/latex`
* LyX files: `~/Library/texmf/tex/latex/lyx`
* BibTeX .bib files: `~/Library/texmf/bibtex/bib`
* BibTeX .bst (bib style) files: `~/Library/texmf/bibtex/bst`

**If any of these directories don't exist, you have to create them.** Most
TeX or LaTeX installers will not create them for you. Just run

```
mkdir -p ~/Library/texmf/tex/latex
```

and you are on your way.

## Rehashing After You Add Files

When you drop a new file or folder into the `texmf` tree, TeX will not
find it until you rehash the TeX database. The command is:

```
texhash ~/Library/texmf
```

If you don't know where your `texmf` directories are in the first place,
running `texhash` on its own will update the database and print the paths
it found, which is a nice way to discover the layout on any given machine.

## Example: The `cancel` Package

The [`cancel` package](https://charlesreid1.com/wiki/Cancel_Package) is a
small package for drawing slashing arrows through terms in equations (nice
for "goes to zero" or "goes to infinity" annotations in engineering
equations).

Installing it on a Mac is one of the easier cases:

* Download the package zip
* Unzip it
* Drop the `.sty` file into `~/Library/texmf/tex/latex`
* Run `texhash ~/Library/texmf`

That's it - no `sudo`, no system-wide install, no touching `/usr/local`.

## What About Windows?

Use MikTeX: <http://miktex.org/>. MikTeX has its own package manager and
handles most of this automatically. Consider yourself lucky.

## When Things Go Wrong: Conflicts With Fink

One historical footgun that we hit years ago, and mention here in case
someone else runs into it: if you have [Fink](https://finkproject.org)
installed, Fink may install its own copy of `pdftex`, and Fink may be putting
`/sw` (or whatever your Fink prefix is) at the *front* of your `$PATH`.

If that happens, `pdftex` from the command line resolves to the Fink version,
not the MacTeX version, and things get confusing quickly.

Two fixes:

1. Stop sourcing `/sw/bin/init.sh` (or `pathsetup.sh`) from your dotfiles,
   and add `/sw` to your `$PATH` manually so MacTeX wins.

2. Call `pdftex` with the full path when you mean the MacTeX version:
   `/usr/texbin/pdftex ...`

Both are annoying. Option 1 is less annoying long-term.

## Related

More notes on our LaTeX page: <https://charlesreid1.com/wiki/LaTeX>
