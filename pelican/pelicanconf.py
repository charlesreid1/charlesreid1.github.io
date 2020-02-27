#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import re, os

SITEURL = 'https://charlesreid1.github.io'
#SITEURL = 'http://localhost:8000'
AUTHOR = u'charlesreid1'
SITENAME = u'charlesreid1'

PATH = 'content'
THEME = 'charlesreid1-githubio-theme'


# -------------------
# Plugins:
HOME = os.environ.get('HOME')
PLUGIN_PATHS = [HOME+'/codes/pelican-plugins/']
PLUGINS = ['render_math']

#MARKUP = ('md')

# Don't try to turn HTML files into pages
#READERS = {'html': None}


MARKDOWN = {
    'extension_configs': {
        # See options here:
        # https://python-markdown.github.io/extensions/toc/
        'markdown.extensions.toc': {
            'title': 'Table of Contents'
        },

        # The rest of this dictionary is the default value
        # http://docs.getpelican.com/en/stable/settings.html
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5'
}


# --------------------
# Static content

STATIC_PATHS = ['images']



# --------------------
# Templates

# template stuff 
THEME_TEMPLATES_OVERRIDES = []
TEMPLATE_PAGES = {}


######################
# To add paths:
#EXTRA_TEMPLATES_PATHS.append('mydir')

# To add template pages in those directories:
### TEMPLATE_PAGES['mydirpage.html'] = 'mydirpage.html'




# ----------------------------
# Blog stuff

# Pagination: posts per page
DEFAULT_PAGINATION = 3

# Length of summary:
SUMMARY_MAX_LENGTH = 100

# Time formats 
DATE_FORMATS = {'en': '%A %m/%d/%Y',}

# Month formatting filter 
from datetime import datetime
def int_to_month (m_int):
    """Turns an integer month into a long month."""
    d = datetime(year=1927, day=1, month=m_int)
    return d.strftime("%B")

JINJA_FILTERS = {'month_name':int_to_month}

## Not sure if these are necessary, or... what.
#ARTICLE_URL = 'blog/{slug}'
#ARTICLE_SAVE_AS = 'blog/{slug}/index.html'
#DIRECT_TEMPLATES = ['blog']
#PAGINATED_DIRECT_TEMPLATES = ['blog']






# --------------8<---------------------

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'atom.xml'
FEED_ALL_RSS = 'feed.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = u'en'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

