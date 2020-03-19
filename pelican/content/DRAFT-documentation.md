Title: Writing Better Documentation: Part 1: The Software
Date: 2020-03-10 22:00
Category: Documentation
Tags: programming, computer science, documentation, technical writing, sphinx, mkdocs, pelican
Status: draft

[TOC]

# Writing Better Documentation: A Series

This is the first in a series of posts about writing better documentation.

**Why the name?**

The series is named "better documentation" and not "good documentation" because documentation
is always being improved, rarely reaching a "finished state". So we use the word "better" to
signal that the emphasis is on things you can do to make your documentation better, one iteration
at a time.

**What does it cover?**

In Part 1, we cover some useful software packages for writing documentation. We cover the use case
of each software, since they each serve different purposes, and give some examples.

In Part 2, we cover how to use Github Pages to host your documentation (for free!). Bonus: this integrates
well with all of the documentation systems covered in Part 1.

In Part 3, we cover some tips for getting started writing and organizing documentation, and creating
a structure that you can build out as your software and documentation mature.

# The Software Packages

In this post we'll cover three software packages useful for writing documentation:

* [**mkdocs**](https://www.mkdocs.org/) - a reliable, simple, markdown-based documentation solution.
* [**sphinx**](https://www.sphinx-doc.org/en/master/) - a highly-configurable, code-friendly documentation framework.
* [**pelican**](https://blog.getpelican.com/) - a sophisticated static site generator.

Our personal favorite is mkdocs, since it is so minimal and straightforward. But sphinx and pelican are both
capable of creating really fantastic documentation pages.

## mkdocs

mkdocs is the first on the list because of how simple and minimal it is. To use mkdocs, you need an mkdocs configuration
file, and some markdown files. The documentation site is configured using a YAML file specifying a few options, and
the content consists of a pile of Markdown files. That's it!

### when to use mkdocs

mkdocs is a good option when you don't have any documentation, but you're accumulating notes/Readmes/markdown files
and you want to turn those into a decent-looking documentation site.

mkdocs can also easily handle larger and more complicated sites. 

**When _not_ to use mkdocs?** mkdocs is _not_ a good option if you find markdown too simple for your needs,
or if you are using documentation in multiple formats, or if you need to extract information from comments in code.

### how to install mkdocs

Use pip, it's the recommended method:

```text
pip install mkdocs
```

### how to use mkdocs

You can initialize an mkdocs site with the command:

```text
mkdocs new .
```

This creates an `mkdocs.yml` config file and a `docs/` directory containing an initial `index.md`. The config file
is an absolutely barebones config file:

```text
site_name: My Docs
```

This can get more complicated, as covered by the guide on the [mkdocs homepage](https://www.mkdocs.org/).
As a more complicated example, here is the config file for the centillion search engine, which includes
additional variables, plus a navigation section and theme info:

```text
site_name: centillion search engine
site_url: http://dcppc.github.io/centillion
repo_name: dcppc/centillion
repo_url: https://github.com/dcppc/centillion

docs_dir: docs
site_dir: site
strict: true

nav:
- Index: index.md
- Configuring Centillion: config.md
- Submodules: submodules.md
- Backend Search: backend.md
- Frontend Web Interface: frontend.md
- Github Authentication: auth.md
- APIs: apis_all.md

extra_css:
- css/custom.css

theme:
  name: null
  custom_dir: mkdocs-material-dib/material
  palette:
    primary: blue
    accent: blue
  logo:
    icon: search
  font:
    text: Roboto Slab
    code: Roboto Mono
```

When you're ready to generate your documentation, use the `build` command:

```text
mkdocs build
```

and to start a simple HTTP server to serve up the documentation, use the `serve` command:

```text
mkdocs serve
```

### pros and cons of mkdocs

Pros:

* Provides a simple and comprehensive solution to the problem of wanting easy, beautiful documentation
* Markdown file format is universal and simple, keeps documentation from getting too complicated
* Only requires 1 configuration file and a pile of Markdown files
* Can be version-controlled

Cons:

* Simplicity of Markdown format can be constricting
* Markdown files must be maintained by hand (goes against principle of laziness)
* Integrating with other (non-markdown) sources of documentation can be challenging

## sphinx

The next documentation package we cover is sphinx. This is a more complex documentation system,
and has many plugins to extend its functionality to make documentation from many sources in many
formats. Sphinx is also written in Python, so if you are developing in Python, that's a big plus.

### when to use sphinx

One of the most important capabilities of sphinx is its autodoc extension. This enables the
automatic generation of documentation for the Python API, and annotates the documentation with
docstrings. When it comes to making lazy, effort-free documentation, it doesn't get much better
than that!

(As an example of this, see the [Github objects](https://pygithub.readthedocs.io/en/latest/github_objects.html)
page of the [PyGithub documentation](https://pygithub.readthedocs.io). The documentation for
PyGithub shows that automatically-generated documentation can be useful, even without any supplementary
pages.)

Use sphinx when you need the autodocs capability, or when you need to extend the functionality of the
documentation generator to handle custom document formats or documentation sources.

**When _not_ to use sphinx?** One of the downsides of sphinx is it doesn't have seamless integration
with Markdown (it works, but not well); sphinx likes ReST (restructured text) better. This is less
universal than markdown and can create additional barriers to writing documentation. If all you want
is to turn a pile of markdown files into documentation, mkdocs is the better bet.

Likewise, formatting sphinx documentation can be frustrating and time-consuming, since the default settings
make documentation hard to read and navigate. Themes allow you to customize the display of content, but
only to an extent. Not everything about the documentation layout can be changed.

### how to install sphinx

Use pip to install sphinx:

```text
pip install sphinx
```

### how to use sphinx

To initialize a sphinx documentation site, use the quick-start function:

```text
sphinx-quickstart
```

This will run through a series of questions about your project, and will use that to create the
sphinx configuration file, `conf.py`. This configuration file is a bit more complicated than the
mkdocs YAML file, but the fact that the configuration file is a Python script means you have all
the power of Python at your command in the configuration file. (That means you can, for example,
use `glob` instead of manually listing every file.)

To enable the autodoc extension, start by adding the root location of the source code to the Python path:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
```

Now specify autodocs in the `extensions` list:

```python
extensions = ['sphinx.ext.autodoc']
```

There are many instructions and guides online on [using
sphinx](https://medium.com/@richdayandnight/a-simple-tutorial-on-how-to-document-your-python-project-using-sphinx-and-rinohtype-177c22a15b5b)
or [using sphinx with 
autodocs](https://medium.com/@eikonomega/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365),
so we will not cover that here.

### pros and cons of sphinx

Pros:

* Can handle documentation from multiple sources in multiple formats
* Written in Python, and supports plugins written in Python
* Provides `autodoc` capabilities to automatically generate documentation from code

Cons:

* Uses ReST (Restructured Text), a more complicated version of Markdown; ReST has a steep learning curve,
  is much less universal, and looks terrible.
* Has poor support for Markdown; you can render Markdown files into documentation pages, but they don't look great.
* Can be overkill for simple projects or if starting new documentation for a project

## pelican

pelican is the last on the list because, while it can be used for documentation pages, it's actually
a static site generator intended for blogging. However, with enough customization, pelican can be
coerced into creating static sites from ReST or Markdown content, or other files.

### when to use pelican

You should think of Pelican as a last resort for documentation, since it is not intended primarily for that
use case, but it also has the capability and flexibility needed to make a static site look and feel however
you'd like. Additionally, pelican, like sphinx, has a configuration file that is a Python script, so that
allows the configuration files to be really powerful.

Pelican also has the ability to include static files, including CSS and Javascript, so pelican can also handle
documentation pages with complex Javascript apps (e.g., visualizations). There are also many plugins available
for pelican, so you can include LaTeX or Jupyter Notebooks in your site too.

**When _not_ to use pelican?** If all you want is to turn a pile of markdown files into a static site,
mkdocs is the more appropriate tool. However, pelican can certainly handle this use case.
If you need documentation generated directly from the code (like Sphinx's autodocs), this is not something
that pelican is capable of providing.

### how to install pelican

```text
pip install pelican
pip install Markdown
```

### how to use pelican



