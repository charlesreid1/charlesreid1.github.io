Title: Charlesreid1.com Technology Stack
Date: 2018-02-21 14:00
Category: Charlesreid1
Tags: web, git, pelican, nginx, apache, mediawiki, javascript, php, docker, security
Status: draft

# Web

Several components:
* Main site - pelican
* Wiki - MediaWiki (PHP), Old Reliable, same software running Wikipedia
* Javascript playground - pelican, life, calendar, maps, Leaflet, D3, etc.
* Blog - hosted on Github, made with Pelican

## Main Pelican Site: Charlesreid1.com

### Design and Layout

Consistent look and feel of site belies underlying heterogeneous elements:
* HTML/JS for main page and Javascript sub-pages (Pelican)
* Wiki with a skin and style files for wiki page layouts defined in PHP (MediaWiki)
* Static content hosted on Github pages (also Pelican)

The way these are kept consistent is by encapsulating all content for the Charlesreid1.com 
look and feel into standalone HTML files that can be copied into MediaWiki's skin folder,
Pelican's theme folder, and shared across Pelican themes to create a suite of 
sites with the same style.

### Pelican Workflow

Manage content of the main site with Pelican, version control with git.

Edit workflow:

* Organize website repo into source branch and htdocs branch
* Clone a local copy of the site, edit source of site to add content
* Commit changes, push to central server

Update htdocs after edit workflow:

* Generate pelican content into output/
* Move to output directory
* Add, commit, and push changes to the htdocs branch

Deploy workflow:

* Clone (or pull) a local copy of the htdocs branch of the site 
* Web server uses this directory asa live htdocs directory

Alternative deploy workflow:

* Clone (or pull) a local copy of the source brnach of the site
* Generate pelian content for site
* Copy htdocs files over to appropriate location on webserver

## Wiki Site: Charlesreid1.com/wiki

MediaWiki

Highly customized skin limits amount of clutter

chose mediawiki nearly a decade ago, and am still going strong with it. Important reasons:
* The content features: simple as hell to create new pages, upload images, transclude content from one page in another, develop page templates, quickly create a sense of "there"-ness
* The markdown: using a MW wiki every day means you are learning MW syntax, which translates directly to Wikipedia. This means you'll have a much deeper understanding of Wikipedia than the average bear.
* The community: MW is a robust tool whose fate is forever tied to the fate of Wikipedia. It's a good bet Wikipedia will be around for a long time, and so will MW.
* The bots: MW has an amazing API that allows you to create sophisticated wiki bots in Python. Again, this is knowledge that translates directly to Wikipedia.

Alternatives: 

* Git-based plain text repos rendered into markdown - this has the problem of mainly consisting of ruby tools,
    most of which were hopelessly mired in ruby versions, gem libraries, and Rakefiles. Ugh. 
    Furthermore, it's diffiult to incorporate rich text, media, HTML, Javascript, or plugins,
    and it's difficult to visualize history (impossible in the browser).

* Other wiki software - none are as full featured as MediaWiki. Trac Wiki came the closest in terms of features and maturity,
    but it was extremely complicated to build and set up, and the syntax is completely different from MediaWiki, and in my opinion
    completely and utterly senseless. MediaWiki offers a better wiki than Trac, and Gitea offers a better version control web interface than Trac.

* Drupal - similar in scope and complexity to MW (and also written in PHP), and designed for a large enough site that 
    you could handle thousands of pages. (For example, The Economist uses Drupal to manage their website.)
    However, I found Drupal's source difficult to understand and nearly impossible to customize, 
    and the barrier to creating pages and linking content was just too high.

* WordPress - yeah right. WP matches MediaWiki in terms of features and ease of use (and is also written in PHP), 
    but WP is also riddled with security flaws and would make the task of managing a decade of notes and information impossible. 

MediaWiki is a clear winner.

## Javascript Playground: Charlesreid1.com/*

Keeping Javascript pages standalone, lightweight, and modular

Pattern for Javascript apps: all files related to the app in a single directory

Static content (css, js libraries, images, common components) in static directory

## Server

Running VPS

Nginx server frontend:

* Listens for requests 
* Forwards requests for wiki on to local instance of Apache
* Pros: fast, secure, good for static content, handling high loads
* Cons: no PHP (mitigated by Apache)

Apache server backend:

* Listens for requests from local address only (Nginx)
* Pros: handles PHP (and many other things)
* Cons: constant patching (mitigated by Docker, building from source, not exposing Apache directly)


# Git

Gitea service - Go binary that runs continuously.

https://charlesreid1.github.io/setting-up-a-self-hosted-github-clone-with-gitea.html

Workflow to build from source, so able to constantly use the latest version.

Goenv to keep my Go version up to date.

# Docker

Use Docker to run services, and to maintain patched, up-to-date software:
* Rsync
* Stunnel
* Netdata
* Grafana
* Nginx
* Apache
* Zmq
* Jupyter Notebook

# Security

Encryption 
* Private keys, SSH connection, ECSA fingerprint over trusted connection
* SSH endpoint first time will ask you to verify fingerprint
* Linode provides root web shell

VPN - management LAN
* Concept of management LAN
* Tinc for lightweight mesh VPN
* OpenVPN is more complicated, server architecture
* How it works: creates virtual network device, private IP 
* Use this to bind services to maangement LAN
* Example: netdata server monitoring dashboard can be bound to VPN IP, and only accessible via LAN

