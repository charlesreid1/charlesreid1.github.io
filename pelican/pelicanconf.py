#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import re, os

SITEURL = ''
AUTHOR = u'charlesreid1'
SITENAME = u'charlesreid1'

PATH = 'content'
THEME = 'cmr-theme'


# -------------------
# Plugins:
HOME = os.environ.get('HOME')
PLUGIN_PATHS = [HOME+'/codes/pelican-plugins/']
PLUGINS = ['render_math']

#MARKUP = ('md')

# Don't try to turn HTML files into pages
#READERS = {'html': None}


# --------------------
# Static content

STATIC_PATHS = ['images']



# --------------------
# Templates

# template stuff 
EXTRA_TEMPLATES_PATHS = []
TEMPLATE_PAGES = {}

### # index 
### EXTRA_TEMPLATES_PATHS.append('angular')

### # The index will become some kind of blog index.
### TEMPLATE_PAGES['index.html'] = 'index.html'

# No contact page on charlesreid1.github.io
#TEMPLATE_PAGES['contact.html'] = 'contact/index.html'

# No pgp page
#TEMPLATE_PAGES['pgp.html'] = 'pgp/index.html'



# writing
# a.k.a.
# blaaaaaaaaarg
### #EXTRA_TEMPLATES_PATHS.append('writing')
### #TEMPLATE_PAGES['writing.html'] = 'writing/index.html'
### 
# summary length
SUMMARY_MAX_LENGTH = 100

# time formats for blaaaarg
DATE_FORMATS = {'en': '%A %m/%d/%Y',}

# month formatting filter for blaaaaaaarg
from datetime import datetime
def int_to_month (m_int):
    """Turns an integer month into a long month."""
    d = datetime(year=1927, day=1, month=m_int)
    return d.strftime("%B")

JINJA_FILTERS = {'month_name':int_to_month}




### # projects
### EXTRA_TEMPLATES_PATHS.append('projects')
### TEMPLATE_PAGES['projects.html'] = 'projects/index.html'
### TEMPLATE_PAGES['projects.json'] = 'projects/projects.json'
### TEMPLATE_PAGES['projects.css']  = 'projects/projects.css'
### TEMPLATE_PAGES['projects_modcontrol.js'] = 'projects/projects_modcontrol.js'
###  
### # about
### EXTRA_TEMPLATES_PATHS.append('about')
### TEMPLATE_PAGES['about.html'] = 'about/index.html'
### TEMPLATE_PAGES['about.css']  = 'about/about.css'
### TEMPLATE_PAGES['about.json'] = 'about/about.json'
### TEMPLATE_PAGES['about_modcontrol.js'] = 'about/about_modcontrol.js'
### 
### TEMPLATE_PAGES['auto.html'] = 'about/auto.html'


DEFAULT_PAGINATION = 3

#ARTICLE_URL = 'blog/{slug}'
#ARTICLE_SAVE_AS = 'blog/{slug}/index.html'
#DIRECT_TEMPLATES = ['blog']
#PAGINATED_DIRECT_TEMPLATES = ['blog']













# --------------8<---------------------

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = u'en'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

