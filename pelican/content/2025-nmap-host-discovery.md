Title: Nmap Host Discovery: All the Ways to Ask "Is Anyone There?"
Category: Security
Date: 2025-05-30 14:00
Tags: security, nmap, host discovery, ping, arp, networking, pentesting

This is a companion post to
[Building an Nmap Short Course from Scratch](building-an-nmap-short-course-from-scratch.html).
Where that post was about the meta - course design, lab
infrastructure - this one drills into the actual first-lecture
material: how Nmap decides whether a host is up.

Full lecture notes:
[Nmap/Short Course/Lecture 1](https://charlesreid1.com/wiki/Nmap/Short_Course/Lecture_1).

## Why Host Discovery Matters

Before you can scan ports, identify services, or check for
vulnerabilities, you have to figure out which IP addresses on the
target network actually have a machine behind them. Scanning IPs that
aren't responding is a waste of time, generates a lot of unnecessary
network noise, and can tip off defenders.

Think of it as making a map of active settlements before deciding
which ones to explore in detail.

## Ethics First

The obvious but necessary caveat: Nmap must only be used on networks
where you have explicit, written authorization to scan. Unauthorized
scanning can be interpreted as an attack, and in many jurisdictions is
illegal.

Everything in this post assumes an isolated lab environment - which is
exactly what we set up in
[the previous post](building-an-nmap-short-course-from-scratch.html).

## The Default: Nmap's Multi-Probe Approach

If you run Nmap as a privileged user (root or `sudo`) without
specifying any discovery options, it will fire *four* probes at each
target:

1. ICMP echo request (a classic ping)
2. TCP SYN packet to port 443
3. TCP ACK packet to port 80
4. ICMP timestamp request

If any of the four gets a response, Nmap considers the host up.

The multi-probe approach exists because different firewalls block
different things. ICMP is commonly blocked at the network edge. Port
443 might be allowed inbound because there is a web server behind it.
Port 80 might respond with a TCP RST because there is nothing
listening. Any one of these signals is enough.

Unprivileged users can't send raw packets, so Nmap falls back to
attempting TCP connect() calls to ports 80 and 443. Less accurate,
but works without root.

## `-sn`: Just Tell Me What's Alive

Nmap's default behavior is to do host discovery *and then* port scan
whatever comes back alive. If you only want the host discovery step,
use `-sn`:

```
nmap -sn 192.168.1.0/24
```

`-sn` means "scan, no port scan." (In older versions it was `-sP`,
"scan ping.") It runs the multi-probe discovery and prints just the
list of live hosts. Very fast, very quiet compared to a full port
scan, and often the first thing you run.

Everything else in this post uses `-sn` unless otherwise noted.

## The `-P` Family: Picking a Specific Probe

If you want to control exactly which probe Nmap sends, use one of the
`-P` flags.

### `-PE`: ICMP Echo (the plain ping)

```
sudo nmap -sn -PE 192.168.1.100
```

The most familiar probe. Sends an ICMP echo request, expects an ICMP
echo reply. Works when firewalls allow ICMP. Frequently blocked at
network perimeters.

### `-PP`: ICMP Timestamp

```
sudo nmap -sn -PP 192.168.1.101
```

Sends an ICMP timestamp request (type 13), expects a timestamp reply
(type 14). Useful when echo requests are blocked but timestamp
requests aren't - some firewall rules block ICMP type 8 (echo) but
forget about type 13.

### `-PM`: ICMP Address Mask

```
sudo nmap -sn -PM 192.168.1.102
```

Sends an ICMP address mask request. Very rarely used legitimately
these days, which is exactly why it sometimes gets through firewalls
that block the more common ICMP types.

The pattern: try the obvious probe, fall back to the less-obvious
ones if the obvious one fails.

### `-PS[ports]`: TCP SYN Ping

```
sudo nmap -sn -PS 192.168.1.0/24
sudo nmap -sn -PS22,80,443 192.168.1.50
```

Sends a TCP SYN packet to the given ports (default 80 if you don't
specify). A response - either SYN/ACK meaning "port open" or RST
meaning "port closed" - tells Nmap the host is alive.

This one is the workhorse against firewalled targets. Firewalls
typically allow inbound traffic to common service ports (80, 443, 22)
because there are legitimate reasons for outsiders to reach those
ports. TCP SYN pings ride on that permitted traffic.

### `-PA[ports]`: TCP ACK Ping

```
sudo nmap -sn -PA 192.168.1.0/24
sudo nmap -sn -PA21 192.168.1.55
```

Sends a TCP packet with the ACK flag set. This is a weird packet -
an ACK with no prior SYN - so most operating systems respond with a
TCP RST regardless of whether the port is open. If you see the RST,
the host is alive.

Useful against stateful firewalls that block unsolicited SYN packets
(because they aren't part of any tracked connection) but let ACKs
through (because ACKs look like the middle of an established
connection the firewall might have lost track of).

### `-PU[ports]`: UDP Ping

```
sudo nmap -sn -PU 192.168.1.0/24
sudo nmap -sn -PU53,161 192.168.1.60
```

Sends a UDP packet to the given ports (default 40125, chosen because
it's usually closed). If the port is closed, the host should respond
with ICMP port unreachable, telling you it's alive. If the port is
open, you might not get a response at all.

UDP ping is less reliable for host discovery on its own, but very
useful when the target runs UDP services (DNS on 53, SNMP on 161) and
when other probes are all blocked.

### `-PR`: ARP Ping

```
sudo nmap -sn -PR 192.168.1.0/24
```

The gold standard when you are on the same Ethernet segment as your
targets. ARP is the layer-2 protocol that resolves IP addresses to
MAC addresses, and hosts *cannot* refuse to answer ARP - if they did,
they would be unable to talk to anything on the local network.

Nmap automatically uses `-PR` for local-segment targets when run by
a privileged user, unless you tell it not to (`--send-ip`). It's
fast (no round trip past the switch) and 100% reliable for hosts
that are up.

## Target Specification

Independent of the probe type, you need to tell Nmap *which* IPs to
scan.

### Single addresses

```
nmap 192.168.1.1
nmap scanme.nmap.org
```

Hostnames get resolved via DNS. `scanme.nmap.org` is a target the
Nmap project maintains specifically for people to practice against.

### CIDR ranges

```
nmap -sn 192.168.1.0/24
nmap -sn 10.0.0.0/8
```

Standard CIDR notation. `/24` is 256 IPs, `/8` is 16.7 million (be
careful).

### Numeric ranges and lists

```
nmap -sn 192.168.1.1-100        # .1 through .100
nmap -sn 192.168.1.1,2,10,50    # specific IPs
nmap -sn 192.168.1,2,3.1-254    # cross product
```

That last one scans `.1-.254` for each of `192.168.1.x`,
`192.168.2.x`, and `192.168.3.x`. Useful for scanning a handful of
adjacent subnets.

### From a file

```
nmap -sn -iL targets.txt
```

One target per line in the file. Best option when you have a large
or irregular list of targets, or when the target list comes from
another tool.

### Excluding targets

```
nmap -sn 192.168.1.0/24 --exclude 192.168.1.1,192.168.1.100
nmap -sn 192.168.1.0/24 --exclude-file dontscan.txt
```

Critical for avoiding accidental scans on the CEO's laptop or the
production database when you're supposed to be scanning a specific
subnet.

## Timing: `-T0` through `-T5`

Nmap has six timing templates that control how aggressively it
sends packets:

* `-T0` (paranoid): Extremely slow. One probe every few minutes.
  Used for IDS evasion in serious red-team engagements.
* `-T1` (sneaky): Slow. IDS evasion, but not as extreme.
* `-T2` (polite): Slower than default. Reduces bandwidth and target
  load. Good for scanning production infrastructure.
* `-T3` (normal): The default. Reasonable timing for most networks.
* `-T4` (aggressive): Faster. Assumes a reliable network. Good
  balance for lab work.
* `-T5` (insane): Very fast. Sacrifices accuracy for speed. Can
  overwhelm slow networks or fragile targets.

```
sudo nmap -sn -T4 192.168.1.0/24
```

For host discovery specifically, `-T4` is usually the right choice
in a lab environment. On production, use `-T3` or `-T2` and be
patient.

## Reading the Output

A successful scan looks like this:

```
Starting Nmap 7.94 ( https://nmap.org ) at 2025-05-27 14:00 PDT
Host 192.168.1.1 is up (0.00050s latency).
MAC Address: AA:BB:CC:DD:EE:FF (Realtek Semiconductor)
Host 192.168.1.10 is up (0.00080s latency).
MAC Address: 11:22:33:44:55:66 (VMware)
Nmap done: 256 IP addresses (2 hosts up) scanned in 2.10 seconds
```

The MAC address only shows up when you're on the same Ethernet
segment. The vendor in parentheses comes from Nmap's built-in OUI
database - useful for spotting VMs, or figuring out which switch
port a device is behind.

## When Hosts Don't Appear

"Host is down" in Nmap's output really means "Nmap didn't get a
response from any of the probes it sent." That's not the same as
"the host is offline." Common reasons a live host doesn't appear:

* **Restrictive firewall.** The most common culprit. Dropping all
  probe types silently is a valid (if aggressive) defensive posture.
* **Host-based firewall.** Windows Firewall, iptables, and similar
  can block probes even when the network firewall is permissive.
* **Wrong scan for the environment.** ICMP-only discovery against a
  target that only accepts TCP-80 - the host won't appear even
  though a `-PS80` scan would find it in an instant.
* **Unprivileged Nmap.** Non-root Nmap has very limited discovery
  options. Always run as root (or via `sudo`) for real scanning.
* **Network layer issues.** Routing problems, wrong subnet mask on
  the scanner, VLAN mismatches - anything that prevents packets
  from reaching the target.

The right response to a "no hosts up" result on a network you know
is alive: try a different discovery method. If ICMP fails, try
`-PS22,80,443`. If TCP fails, try `-PA`. If nothing works, you're
probably up against a very well-configured firewall.

## From Discovery to Deeper Scans

Once you have a list of live hosts, the natural next step is port
scanning them to see what services are running. The clean way to
chain this is with grepable output:

```
nmap -sn -oG - 192.168.1.0/24 | awk '/Up$/{print $2}' > live_hosts.txt
nmap -sV -iL live_hosts.txt
```

The first command produces a machine-parseable list of live IPs.
The second feeds that list into a service-detection scan. This
two-phase approach is efficient (you don't waste time port-scanning
dead IPs) and organized (you have a saved list of live hosts to
work from later).

Service detection, port scanning, NSE scripting - all of that comes
in later lectures of the course. But it all starts with knowing
who's home.

## References

* Full lecture:
  [Nmap/Short Course/Lecture 1](https://charlesreid1.com/wiki/Nmap/Short_Course/Lecture_1)
* The rest of the course:
  [Nmap/Short Course](https://charlesreid1.com/wiki/Nmap/Short_Course)
* Nmap documentation: <https://nmap.org/book/man.html>
