Title: Stunnel 
Date: 2017-04-30 20:00
Category: Security
Tags: stunnel, SSL, encryption, SSH, networking, OpenVPN

* [Introduction](#stunnel-intro)
	* [What Does Stunnel Do?](#stunnel-what)
	* [How Does Stunnel Work?](#stunnel-work) 

* [Setting Up an Stunnel Server](#stunnel-server)
	* [Charlesreid1.com Resources for Stunnel Servers](#stunnel-server-resoures)

* [Setting Up an Stunnel Client](#stunnel-client)

* [Example Protocols](#stunnel-protocols)

* [Stunnel with Docker](#stunnel-docker)

* [Troubleshooting Stunnel Connections](#stunnel-troubleshooting)

* [References](#stunnel-refs)



<a name="stunnel-intro"></a>
## Introduction

<a name="stunnel-what"></a>
### What Does Stunnel Do?

Stunnel is a tool for creating SSL tunnels between a client and a server.

Creating SSL connections is a general task that is very useful.
In particular, any packet of any protocol can always be wrapped in an
additional SSL layer, with packets embedded within packets, so this means 
you can wrap arbitrary traffic protocols in SSL using Stunnel.

Stunnel requires a client and a server on either end of the tunnel.

This writeup assumes access to both the server and the client.
If you don't have access to the client, the server certificate
needs to be signed by a certificate authority that the client trusts.
You can either:

* Shell out big bucks for a certificate signed by a certificate authority company, thereby contributing to the ongoing racketeering of said companies;

* Use a LetsEncrypt certificate, signed by a certificate authority for free; or

* Use a self-signed certificate and install the certificate authority onto the client computer.

(These are all difficult and confusing processes, 
compounded by OpenSSL's lack of documentation
and a proliferation of incorrect terminology.
Good luck.)

<a name="stunnel-work"></a>
### How Does Stunnel Work?

The client stunnel instance will encrypt traffic, 
and the server stunnel instance will decrypt traffic.

When encrypting traffic, stunnel accepts incoming traffic by listening on
a port (almost always a local port). It will wrap the traffic in an encrypted
SSL layer (TCP wrapping) using the SSL certificate/key that is shared between
the client and the server. The client then sends out the encrypted traffic 
over an external connection, and on to the stunnel server.

When decrypting traffic, stunnel will listen on an external connection for 
incoming, encrypted SSL traffic. It will use its SSL certificate/key to 
decrypt the traffic and unwrap the SSL layer. It will then forward this traffic
on to another (usually local) port.

![Stunnel flowchart schematic](/images/stunnel1.png)

<a name="stunnel-server"></a>
## Setting Up an Stunnel Server

Stunnel servers can listen on any port, and the port you choose depends on the application. 
The configuration we're showing here is intended to bypass a network that is tightly controlled
and locked down except for HTTP and HTTPS traffic (ports 80 and 443).

Consider an example of connecting a local service on local port 8443 (not open to the outside world)
to an stunnel server listening on port 443 (open to the outside world).

stunnel will listen on port 443, open to external traffic, for SSL-encrypted stunnel traffic. 
This means that only stunnel can listen on 443 (so this cannot be a server for an HTTPS web 
site - if a user points their browser to https://yourstunnelserver.com stunnel will not understand
the HTTPS request and will discard it). 
We can use stunnel on any port that we want, but communicating between stunnel clients 
and servers on port 443 allows us to disguise arbitrary traffic (HTTP, HTTPS, SSH, database, 
etc.) as legitimate HTTPS. 

This is very useful if we have a firewall that is actively inspecting
the type of traffic inside of packets, and dropping packets with particular protocols like 
SSH or OpenVPN. By wrapping that traffic in an SSL layer, there is no way for the 
firewall to inspect the contents of the packet, so it just looks like ordinary HTTPS traffic.
The firewall can't decrypt the packet contents, so it doesn't know if you are visiting 
your bank, checking your email, or sneaking SSH/OpenVPN traffic through the firewall. 

(Note that other services like Iodine allow you to do similar things with other protocols,
like disguising network connections using encrypted DNS on port 53.)

Typically, stunnel is forwarding that traffic on to a local port, something like 8443. 
(The common scenario is if you have a service only exposed to LOCAL traffic from localhost or 127.0.0.1 
and not bound to an EXTERNAL ip address like 0.0.0.0). 

<a name="stunnel-server-resources"></a>
### Charlesreid1.com Resources for Stunnel Servers

The charlesreid1.com wiki has an extensive guide to setting up an Stunnel server: 

* [charlesreid1.com/wiki/Stunnel/Server](https://charlesreid1.com/wiki/Stunnel/Server)

* [charlesreid1.com/wiki/Stunnel/Docker](https://charlesreid1.com/wiki/Stunnel/Docker) - wiki page detailing the use of Docker and Docker containers to run an stunnel server.

The charlesreid1.com git server has several repositories with configuration files for setting up an stunnel server: 

* [d-stunnel repository](https://charlesreid1.com:3000/docker/d-stunnel) - repo containing Docker configuration files, for creating a Docker container that runs an stunnel server.
	This repository contains example stunnel configuration files for running a number of different protocols over stunnel (ssh, http, and rsync).


<a name="stunnel-client"></a>
## Setting Up an Stunnel Client

Running an stunnel client requires installing stunnel and 
setting up a configuration file just like if you were setting up an Stunnel/Server, 
except swapping the accept and connect ports, since we want the client to accept local 
traffic (e.g., on port 8443) and send it on to the server that it connects to with SSL 
(e.g., on port 443).

<a name="stunnel-client-resources"></a>
## Charlesreid1.com Resources for Stunnel Clients

The charlesreid1.com wiki has an extensive guide to setting up an Stunnel client: 

* [charlesreid1.com/wiki/Stunnel/Client](https://charlesreid1.com/wiki/Stunnel/Client) - wiki page detailing the stunnel configuration process for stunnel servers.

The charlesreid1.com git server has several repositories with configuration files for setting up an stunnel client: 

* [m-stunnel repository](https://charlesreid1.com:3000/mac/m-stunnel) - stunnel configuration files for running an stunnel client on Mac OS X

* [pi-stunnel repository](https://charlesreid1.com:3000/rpi/pi-stunnel) - stunnel configuration files for running an stunnel client on Raspberry Pi


<a name="stunnel-protocols"></a>
## Example Protocols

One of the most beautiful aspects of networking is that packets can be wrapped within other packets - 
so theoretically it can be packets all the way down. This allows us to use stunnel's SSL TCP wrappers to wrap
just about any traffic we want. This means we can run various services (encrypted or not) through stunnel,
including but not limited to:

* SSH (secure shell)

* SCP (secure copy)

* OpenVPN (virtual network)

* Rsync (file transfer)

* MongoDB (NoSQL database)

* Redis (local-only NoSQL database)

While stunnel has a few pre-configured services that it can deal with, 
users can also define their own custom protocols, over whatever port they please.

The charlesreid1.com wiki details stunnel configuration for all of the above protocols,
excepting MongoDB and redis. Here are links to pages specifying how to configure stunnel
for each protocol:

* [SSH over stunnel](https://charlesreid1.com/wiki/Stunnel/SSH)

* [SCP over stunnel](https://charlesreid1.com/wiki/Stunnel/Scp)

* [HTTP over stunnel](https://charlesreid1.com/wiki/Stunnel/HTTP)

* [OpenVPN over stunnel](https://charlesreid1.com/wiki/Stunnel/OpenVPN)

* [Rsync over stunnel](https://charlesreid1.com/wiki/Stunnel/Rsync)

The [Rsync over stunnel](https://charlesreid1.com/wiki/Stunnel/Rsync) page, in particular,
details the steps needed to define your own custom protocol and have stunnel wrap it 
in an SSL layer *correctly*.


<a name="stunnel-docker"></a>
## Stunnel with Docker

Docker is a useful way of managing services in a self-contained and reproducible manner.
Running stunnel through a Docker container is surprisingly easy: 
once you've installed stunnel into the docker container, you just need to map 
the incoming port (containing incoming encrypted traffic from the client, linked to the external network interface)
to the outgoing port (containing decrypted traffic from stunnel, linked to a local-only service on a closed port).

The charlesreid1.com wiki details how to create set up SSH over stunnel at the following page:
* [charlesreid1.com/wiki/Stunnel/Docker](https://charlesreid1.com/wiki/Stunnel/Docker)

The charlesreid1.com git server has an stunnel docker repository with configuration files
for running a Docker stunnel server, along with several example stunnel server configuration files
for handling protocols like rsync, ssh, and http:
* [d-stunnel repository](https://charlesreid1.com:3000/docker/d-stunnel)


<a name="stunnel-troubleshooting"></a>
## Troubleshooting Stunnel Connections

In the [d-stunnel repository](https://charlesreid1.com:3000/docker/d-stunnel) is a document called `DEBUGGING.md` 
that contains a number of techniques for debugging an stunnel connection. 

[Here is the direct link to DEBUGGING.md](https://charlesreid1.com:3000/docker/d-stunnel/src/master/DEBUGGING.md).

The techniques covered include:

* Configuring stunnel to run in the foreground (print log messages to console instead of to log file)

* Configuring stunnel to output debugging information 

* Poking the stunnel server with telnet

* Inspecting open ports with nmap

* Watching `/var/log/syslog` for activity

See [DEBUGGING.md](https://charlesreid1.com:3000/docker/d-stunnel/src/master/DEBUGGING.md) for details.

<a name="stunnel-refs"></a>
## References

1. "Stunnel". Charlesreid1.com wiki. 30 April 2017. 
<[https://charlesreid1.com/wiki/Stunnel](https://charlesreid1.com/wiki/Stunnel)>

2. "Category: Stunnel". Charlesreid1.com wiki. 30 April 2017. 
<[https://charlesreid1.com/wiki/Category:Stunnel](https://charlesreid1.com/wiki/Category:Stunnel)>

3. "Stunnel/Server". Charlesreid1.com wiki. 30 April 2017. 
<[https://charlesreid1.com/wiki/Stunnel/Server](https://charlesreid1.com/wiki/Stunnel/Server)>

4. "Stunnel/Client". Charlesreid1.com wiki. 30 April 2017. 
<[https://charlesreid1.com/wiki/Stunnel/Client](https://charlesreid1.com/wiki/Stunnel/Client)>

5. "Stunnel/Docker". Charlesreid1.com wiki. 30 April 2017. 
<[https://charlesreid1.com/wiki/Stunnel/Docker](https://charlesreid1.com/wiki/Stunnel/Docker)>

6. "Stunnel/Certificates". Charlesreid1.com wiki. 30 April 2017. 
<[https://charlesreid1.com/wiki/Stunnel/Certificates](https://charlesreid1.com/wiki/Stunnel/Certificates)>

7. "Stunnel/Rsync". Charlesreid1.com wiki. 30 April 2017. 
<[https://charlesreid1.com/wiki/Stunnel/Rsync](https://charlesreid1.com/wiki/Stunnel/Rsync)>

8. "Stunnel/SSH". Charlesreid1.com wiki. 30 April 2017. 
<[https://charlesreid1.com/wiki/Stunnel/SSH](https://charlesreid1.com/wiki/Stunnel/SSH)>

9. "Stunnel/Scp". Charlesreid1.com wiki. 30 April 2017. 
<[https://charlesreid1.com/wiki/Stunnel/Scp](https://charlesreid1.com/wiki/Stunnel/Scp)>

10. "Stunnel/OpenVPN". Charlesreid1.com wiki. 30 April 2017. 
<[https://charlesreid1.com/wiki/Stunnel/OpenVPN](https://charlesreid1.com/wiki/Stunnel/OpenVPN)>

