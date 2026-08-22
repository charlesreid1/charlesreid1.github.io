Title: Building an Nmap Short Course from Scratch
Date: 2025-05-27 12:00
Category: Security
Tags: security, nmap, teaching, curriculum, aws, vagrant, docker, ansible, pentesting

We spent a good chunk of late May 2025 building a short course on Nmap
from scratch - 12 lectures, 12 companion labs, plus the entire virtual
lab infrastructure the students would use to run the labs. The whole
thing lives on our wiki under
[Nmap/Short Course](https://charlesreid1.com/wiki/Nmap/Short_Course).

This post is not about the Nmap material itself (that comes in the next
post). It is about the design decisions behind the course - why 12
lectures, why a fully isolated cloud lab, why Vagrant + Docker +
Ansible instead of picking one, and what we would do differently if
we started over.

## Course Shape

The course is organized into three modules:

* **Module 1: Nmap Mastery - Beyond the Basics.** The core Nmap
  material: host discovery, port scanning, service and OS detection,
  the scripting engine (NSE), and output formats.
* **Module 2: Red Team Nmap - Offensive Recon & Vuln Identification.**
  Using Nmap for reconnaissance in an authorized engagement:
  fingerprinting, vulnerability enumeration via NSE, and integrating
  results into a broader recon workflow.
* **Module 3: Blue Team Nmap - Auditing, Defense & Network Monitoring.**
  The other side: using Nmap for asset inventory, compliance checks,
  detecting unauthorized services, and pairing Nmap output with IDS
  rules.

Twelve lectures split across those three modules. Every lecture has a
companion lab. The labs share a single virtual environment that gets
richer over the course - by the time students are in Module 3 they are
scanning the same infrastructure they attacked in Module 2.

## Why Twelve Lectures

We picked 12 because it maps cleanly to a compressed summer session (a
lecture + lab per week for a 12-week course, or two per week for a
6-week intensive). It also gave us enough room to introduce Nmap
options in the order they build on each other, without cramming.

Twelve is a round number, each lecture is a coherent unit, and the
whole thing still fits in a summer course.

## The Lab Environment: The Big Boy

The lab infrastructure is the part we spent the most time on. Our
requirements:

* Students should be able to scan without touching any network they
  don't have explicit permission to scan
* The lab should have a variety of realistic services and
  vulnerabilities, not just one target
* Adding a new lab scenario should be a few lines of code, not a
  reinstall
* The instructor should be able to reset the whole environment to a
  known-good state before every class

The design we landed on:

**A single large EC2 instance as the lab host.** We call it "the big
boy" in our notes. Something like an `m5.xlarge` if the budget allows.
Ubuntu Server LTS on the host, because Vagrant/libvirt/KVM has the
smoothest experience there. Storage is EBS `gp3`, 80-100 GB.

**Nested virtualization on that host.** The EC2 instance runs KVM
(via libvirt), which runs full VMs for the more heavyweight targets
(and one attacker VM per student), plus Docker for lightweight
containerized services. Vagrant orchestrates the VMs, Docker Compose
orchestrates the containers, and both live on the same private virtual
network (`192.168.50.0/24` in our example).

**Ansible for configuration management.** Every target service, every
firewall rule, every open port is defined in an Ansible playbook.
Changing the lab is editing YAML, not clicking around in Docker or
SSHing into VMs and running commands.

**Students SSH into an attacker VM.** They do not SSH into the EC2
host directly, and they do not connect via VPN. Each student (or
shared pair of students) gets a preconfigured attacker VM with Nmap
and the other course tools installed. That VM sits inside the lab
network and can reach all the targets.

The recommendation we did not take: a VPN-based approach where students
connect to the EC2 host and run Nmap from their own laptops. We ruled
it out because it puts environment consistency on the student's
shoulders - their local Nmap version, their local firewall, their
local OS. The attacker-VM approach guarantees everyone is running the
same tool from the same place.

## Why This Stack

The "why Vagrant + Docker + Ansible instead of picking one" question
comes up a lot. Short version:

* **Vagrant** is the right tool for full VMs that need to look and
  behave like real hosts (a Windows target, an outdated Linux with a
  vulnerable SSH). Vagrant plays well with libvirt/KVM on Linux.
* **Docker Compose** is the right tool for lightweight service
  targets: a vulnerable web app, an FTP server, a Samba share. One
  container, one service, one IP.
* **Ansible** is the right tool for configuration - install this
  software, open this port, run this service - and it works
  identically on Vagrant VMs and Docker containers.

Each tool does waht it is best at. Trying to make
Docker do full-VM work is possible but painful. Trying to make Vagrant
manage 30 tiny services is possible but slow. Ansible glues them
together with the same configuration language.

## Cost Model

The EC2 instance is the main cost driver. Some things we do to keep
it reasonable:

* **Stop the instance when not in use.** Evenings, weekends, and
  between class sessions. We only pay for the EBS storage during
  those times, not the compute.
* **Start small on the instance size.** If it is not enough, we
  upgrade.
* **Use Elastic IP or a cheap domain.** Use an easy to remember
  domain like `nmap-lab.our-course.net`.

Spot Instances would save a lot more, but we ruled them out because
they can be terminated with little notice, and getting evicted 15
minutes into a lab session is not the experience we want to give
students.

## Notes for the Instructor

A few things we would tell anyone building a course like this from
scratch:

**Version everything.** The whole lab is a Git repo:
Vagrantfile, `docker-compose.yml`, Ansible playbooks, and the Ansible
inventory. Every branch is a different lab scenario. Rolling back is
`git checkout`.

**Test the lab reset every time.** Before every session, tear the
whole environment down (`docker-compose down -v && vagrant destroy
-f`) and bring it back up from scratch. This catches "works on my machine"
bugs.

**Write the lab handout after you build the lab.** The lab handout is
the source of truth for what students see and do. If you write the
handout first and then build the lab to match it, you will end up
writing two things that don't quite line up.

**Instrument the attacker VM.** We put a shell history file that
survives resets, plus a script that logs every Nmap command run
during the session, so students can review what they did. Also
useful when a student says "I typed the command exactly and it
didn't work."

## What This Cost Us

The course took roughly two solid weeks to build end-to-end - one week
on the lab infrastructure, one week on the lecture content and lab
exercises. 

expected to run more than once. If we were doing it as a one-off, we
would have skipped the Ansible layer and hard-coded the target
configurations, saving maybe two or three days at the cost of a much
worse experience if we ever wanted to change anything.

If you are considering doing this: yes, do it. The single biggest
teaching lever is being able to show students a live network with
real services responding to their scans, and this setup does that
without ever putting them or you in legal jeopardy.

## References

* Our full course notes:
  [Nmap/Short Course](https://charlesreid1.com/wiki/Nmap/Short_Course)
* Lab infrastructure design:
  [Nmap/Short Course/Running the Labs](https://charlesreid1.com/wiki/Nmap/Short_Course/Running_the_Labs)
* Nmap itself: <https://nmap.org/>
