Title: centillion: a document search engine
Date: 2019-03-10 9:00
Category: Python
Tags: python, centillion, search, search engine, google drive, github, flask

We're excited to announce the public release of [centillion](https://github.com/dcppc/centillion),
a document search engine. 

centillion is a search tool that can be used by any individual or organization
to index Github repositories (including the content of markdown files),
Google Drive folders (including the content of .docx files), and Disqus
comment threads.

centillion is [tested using Travis CI](travis-ci.org/dcppc/centillion).

centillion was originally written for the [NIH Data Commons](https://public.nihdatacommons.us)
effort (which recently concluded).  centillion was built to facilitate information-finding
in a project with hundreds of people at dozens of institutions generating a sea of email threads,
Google Drive folders, markdown files, websites, and Github repositories.

centillion provided a single comprehensive way of searching across All The Things 
and earned the author many thanks from members across the Data Commons. It is the
author's hope that centillion can prove equally useful for other organizations.

Under the hood centillion uses [Flask](http://flask.pocoo.org/) (a web server
microframework) and [Whoosh](https://whoosh.readthedocs.io/en/latest/) (a Python-based
search engine tool).

You can get a copy of the latest centillion release here: <https://github.com/dcppc/centillion>

You can find the latest centillion documentation here: <http://nih-data-commons.us/centillion/>

