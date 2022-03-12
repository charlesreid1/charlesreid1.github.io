Title: Copying LetsEncrypt Certs Between Machines
Date: 2020-08-11 17:00
Category: Security
Tags: letsencrypt, ssl, https, certificates, letsencrypt

[TOC]

A quick post that details a useful operation: copying LetsEncrypt certificates
from one machine to another.

(We also cover our use case: setting up certificates for private VPN networks
that use public DNS entries.)

## HTTPS, SSL Certificates, and LetsEncrypt

As a bit of background, the whole reason this is necessary, the whole reason we are dealing with
the hassle of setting up SSL certificates, is to enable end-to-end encrypted connections to
a server.

For example, we might have a web application that we want to make available over a VPN network.
The web application would have a private IP address on the VPN network, say `10.0.0.101`.

Now, what we want is for clients connected to the VPN to be able to visit a domain, say
`foobar.limo`, and be able to make encrypted connections to the web service at `10.0.0.101`.

We can do this (assuming we control the foobar.limo domain) by creating a public DNS entry
for `foobar.limo` to point to `10.0.0.101`. Then when visitors type `foobar.limo` into their
browser, if they are connected to the VPN they will reach the web service at `10.0.0.101`.

To make connections encrypted, however, so that users can type `https://foobar.limo` and make an
encrypted connection to the server at `10.0.0.101`, the server must have an SSL certificate
for the `foobar.limo` domain.

Assuming the web service at `10.0.0.101` cannot be reached from the outside world,
it becomes necessary to perform several extra steps to enable SSL on the `10.0.0.101` server:

* First, the DNS entry for `foobar.limo` must be temporarily updated to point to a server that:
    * has a publicly-accessible IP address,
    * has LetsEncrypt and certbot installed,
    * is connected to or can connect to the VPN or private `10.0.0.101` server,
    * has no services running on port 80

* Second, the certbot utility must be run on the publicly-accessible server to request a new or renewed
  certificate `foobar.limo`. This will put the new or renewed `foobar.limo` cert files into
  `/etc/letsencrypt/live`.

* Third, the LetsEncrypt certificates are owned by the root user, they must be owned by the root user on the
  remote machine they are copied to, and SSH/SCP via the root user is (or should be!) prohibited,
  the certificate files must be compressed using tar, so they can be copied as a non-root user;
  and on the remote machine, they must be uncompressed to the appropriate location.

(Yes, there is always a [relevant XKCD](https://xkcd.com/1168/).)

In this post, we cover how this works, and why you might want to do this.

## Create Certificates

The first time you create a private VPN certificate on a machine:

* Log into the DNS provider
* Create a DNS record - type A, pointing to the IP address of the public server.
* Run the certbot command to create a certificate on the public server (see below).
* Copy the certificates to the private VPN node using scp (see below).
* Update the DNS record - type A, to point to the private VPN IP address of the private server.

### Certbot Command

Command to create a certbot certificate (must be run as sudo):

```plain
#!/bin/bash
if [ "$(id -u)" != "0" ]; then
    echo ""
    echo ""
    echo "This script should be run as root."
    echo ""
    echo ""
    exit 1;
fi

set -x

DOM="foobar.limo"

certbot certonly \
    --standalone \
    --non-interactive \
    --agree-tos \
    --email test@example.com \
    -d ${DOM}
```

This command requires port 80 be available (the `--standalone` flag starts a standalone web server
that binds to port 80). If port 80 is being used this command will fail to run and the cert will not be created.

### Tar Compress Certs Command

Archive on the public server:

```plain
DOM="foobar.limo"
sudo tar -chvzf foobar_certs.tar.gz \
    /etc/letsencrypt/archive/${DOM} \
    /etc/letsencrypt/renewal/${DOM}.conf \
    /etc/letsencrypt/live/${DOM}
```

### Secure Copy Certs Command

Use scp to copy certs to private remote machine:

```plain
scp foobar_certs.tar.gz user@10.0.0.101:~/
```

### Untar Certs Command

On the private remote machine, untar the certs file copied over:

```plain
cd /
sudo tar -xvf ~/foobar_certs.tar.gz
```

Last, fix permissions for cert directories:

```
sudo chmod 700 /etc/letsencrypt/archive
sudo chmod -R 755 /etc/letsencrypt/archive/*
sudo chmod 700 /etc/letsencrypt/live
sudo chmod -R 755 /etc/letsencrypt/live/*
sudo chmod 700 /etc/letsencrypt/archive
```

## Renew Certificates

When you renew a private VPN certificate on a machine:

* Log into the DNS provider
* Update the DNS record to a type A, pointing to the IP adress of the public server.
* Run the certbot command to renew a certificate on the public server (see above).
* Copy the certificates to the private VPN node (see above).
* Untar the certificates into place on the private VPN node (see above).
* Restore the DNS record - type A, to point to the private VPN IP address of private server again.

