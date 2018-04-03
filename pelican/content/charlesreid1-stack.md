Title: Charlesreid1.com Stack
Date: 2018-03-31 23:00
Category: Charlesreid1
Tags: web, git, pelican, nginx, ssl, apache, mediawiki, javascript, php, docker, security

This post is a preview of a series of posts to come, which will document
the process of containerizing the entire [charlesreid1.com](https://charlesreid1.com) website.

We will run through a lot of different moving parts and how to get them all working:

* Multiple domains and subdomains pointing to different services
* Docker pod for all services
* Nginx + SSL
* Reverse proxies via nginx
* Apache + MySQL + MediaWiki
* phpMyAdmin
* Gitea
* Configuration files under version control
* Data managed with backup/restore scripts and cron jobs
* Static content under version control
* Files server
* REST API
* Management LAN

All of the code for doing this is in [docker/pod-charlesreid1](https://git.charlesreid1.com/docker/pod-charlesreid1),
in particular in the `docker-compose.yml` file.

The big switchover took nearly a month, but it was relatively seamless, and only required one false start and a few minutes of downtime.

For now, check out the readme at [docker/pod-charlesreid1](https://git.charlesreid1.com/docker/pod-charlesreid1).
More details to come.

