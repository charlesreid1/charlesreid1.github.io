Title: AWSome Day Seattle Notes: Part 1: The Basics
Date: 2017-04-12 10:00
Category: Charlesreid1
Tags: aws, cloud, vpc, containers, data engineering

These notes are also available on [git.charlesreid1.com](https://git.charlesreid1.com/charlesreid1/aws/src/branch/master/awsome-day-sea-2018)

# AWSome Day Notes: Part 2: Networking, Security, and Miscellany

Following are some notes from Amazon's AWSome Day (Tuesday, February 27, 2018).

## Nomenclature

**Elastic:** You'll see the word "elastic" on a lot of Amazon's services. The "elastic" concept refers to a service that is able to handle huge increases in traffic (Pokemon Go - number of users grew orders of magnitude faster/larger than what they designed for).

**Virtual Private Cloud (VPC):** The AWS equivalent of a virtual private network (VPN). A VPC is a virtual network that allows a given set of nodes in the same region and zone to create a virtual network to communicate privately.

## Services

This document will give a brief summary of some of the popular cloud services. The model for most of these technologies is, the Apache Software Foundation will release an open-source big data project (can be installed/run by anyone). But since most people are using cloud providers anyway, the cloud providers offer their own ready-to-go implementation of these services. These run stable versions of the Apache software, wrapped by the cloud provider's API. This is a win-win because you don't have to fiddle with wrangling servers, and they can use their resources more wisely.

As an example, Apache Kafka is software for handling message streams. (Like a giant digital mail room - some services broadcast/publish messages, some services receive/subscribe to messages.) You can install Kafka locally or on a cluster, or rent cloud nodes and install it yourself. Or, you can use Kinesis on AWS, or PubSub on Google Cloud Platform (GCP), both of which are elastic (completely transparent to you) and charge for data throughput instead of compute time. Code written for Kafka can be uploaded and used without modification.

A few other important services, listing the Apache, AWS, and GCP equivalents:

| Apache   | AWS             |GCP       |Description
|----------|:----------------|----------|------------
|Hadoop    |Kinesis Analytics|Dataproc  |Running data-intensive parallel jobs
|Spark     |Kinesis Analytics|Dataproc  |Running data-intensive parallel jobs
|HDFS      |S3               |GC Storage|Object-based file storage
|Beam      |Kinesis Streams  |Dataflow  |Sream/batch data processing pipelines
|Impala    |Redshift/Athena  |BigQuery  |Handles SQL queries on massive (>1 PB) data sets
|Kafka     |Kinesis          |PubSub    |Message streaming

There are many other cloud services, some without a corresponding Apache project (e.g., Google's Machine Learning APIs or Amazon's text-to-speech API) but these five are common in big data ecosystems.

## Networking

Cloud networking is like the condiment bar of cloud providers - customers don't pay for it, but they can help themselves. 

Why set up a VPC? 
* Scaling - having the ability to connect nodes via network means you can scale up client-server services (e.g., databases/web servers)
* Security - VPC traffic is encrypted and not visible to outsiders, even when it occurs over public channels. Services can be set up to listen only for traffic from the VPC. You can also connect from an outside box (e.g., your laptop) to the VPC using a VPN client.
* Learning - you have to deal with some nitty gritty details, but learning how to set up virtual networks gives you a real education in network security and in how the internet works. 

You can still accomplish a lot even with simple networking patterns.

### Making a VPC: Plan

To create a VPC, you first define the entire VPC network, then define a subnet on the network. The subnet must have an internet gateway, a routing table, and DHCP/DNS added to it so that nodes on the subnet can access the outside internet and find each other.

Here is a visual depiction of the architecture:

```
         +--------------------------------------------------------------------------+
         | Whole Internet                                                           |
         |                                                                          |
         |                                                                          |
         |  +--------------------------------------------------------------------+  |
         |  |  Amazon                                                            |  |
         |  |                                                                    |  |
         |  |                                                                    |  |
         |  |                                                                    |  |
         |  |   +---------------------------------------------------+            |  |
         |  |   |   Virtual Private Cloud: WAN                      |            |  |
         |  |   |                                             +-----+-----+      |  |
         |  |   |   Network IP Block: 10.117.0.0/16           | Internet  |      |  |
         |  |   |                     10.117.*.*              | Gateway   |      |  |
         |  |   |                                             +-----+-----+      |  |
         |  |   |    +----------------------------------+           |            |  |
         |  |   |    |  VPC Subnet: LAN                 |           |            |  |
         |  |   |    |                                  |     +-----+-----+      |  |
         |  |   |    |  Subnet IP Block: 10.117.0.0/24  |     |  Routing  |      |  |
         |  |   |    |                   10.117.0.*     |     |  Table    |      |  |
         |  |   |    |                                  |     +-----+-----+      |  |
         |  |   |    |                                  |           |            |  |
         |  |   |    +----------------------------------+           |            |  |
         |  |   |                                             +-----+-----+      |  |
         |  |   |                                             |   DHCP    |      |  |
         |  |   |                                             +-----+-----+      |  |
         |  |   |                                                   |            |  |
         |  |   +---------------------------------------------------+            |  |
         |  |                                                                    |  |
         |  +--------------------------------------------------------------------+  |
         |                                                                          |
         +--------------------------------------------------------------------------+
```

### Making a VPC: Network and Subnet

To sepcify the network and subnet IP ranges, you use CIDR notation, which is an IP address
with zeroes in several blocks, and a suffix indicating which blocks are available for this 
network to assign. (For reference, `A.B.C.D/8` means "the last 3 blocks" or `B.C.D`;  `A.B.C.D/16` means "the last 2 blocks" or `C.D`; and `A.B.C.D/24` means "the last block" or `.D`).

The network IP address can be specified as:

```
10.X.0.0/16
```

where X is any number between 0 and 254 (when you include the reserved 255 value, that totals 256, since IP addresses are just 32 bit strings, 4 blocks of 8 bits each - `2^8 = 256`). The subnet can be specified with the CIDR IP range:

```
10.X.Y.0/24
```

where X and Y are integers between 0 and 254. This means any node joining this subnet will have an IP address of the form `10.X.Y.*`. Two IP addresses with the same `X` value are on the same VPC network; two IP addresses with the same `Y` value are on the same subnet.

In the example above, X = 117, and we have the VPC defined by:

```
10.117.0.0/16
```

and the subnet defined by:

```
10.117.0.0/24
```

### Making a VPC: The Essentials

Once you've added the VPC and the subnet, you'll also need to add three essential services to the VPC network:

* Internet gateway - this is something you create from the VPC section of the AWS console. It's like your home wifi router that's connected to the internet. actually, it _is_ the VPC network router, and it _is_ connected to the internet.
* Routing table - this tells computers on the network how to find each other and how to find the gateway.
* DHCP - domain host control protocol, this is the service that is used to hand out IP addresses
* (Bundled with DHCP) DNS - domain name service, this is used to turn web URLs into IP addresses

Now you should be good to go. (Scratch that - make a security group first.) 

### Making a VPC: Security Group

One last step, after you've constructed the network, is to create a security group to control outside access to the VPC. This is an AWS-level firewall that will only allow traffic on ports you specify. Here we specify a single security group for every node on the network, and the security policy opens the following ports from and to computers in the same VPC:

* 19999 - netdata
* 9090 - prometheus
* 3000 - grafana
* 27017 - mongodb
* 8080 - mongoexpress

### Adding Nodes to the VPC

Test out your network by creating a t2.micro node and specifying the subnet you created as the network the node should connect to. Check to ensure you can access the internet.

A good schema to use is:

```
10.X.0.1      gateway
10.X.0.100    node0
10.X.0.101    node1
10.X.0.102    node2
...
```

## Scaling Your Process

> If you're SSHing into a machine, your automation is broken.
> - Alex the AWS trainer

There are some tricks to getting your process to scale, but the essential part is figuring out how to remove SSH from the process. Cloud OS images (e.g. Ubuntu) have cloud-init, which runs an init script on boot. [More info in this Stack Overflow post](https://stackoverflow.com/a/10128171). This must be a bash script and size is limited to 16 KB. If it takes > 10 minutes, AWS will treat it as hanging and kill the node, so keep it (relatively) simple.

Example of what you can do:
* Check out a git repo with initailization scripts
* Install a hard-coded copy of your SSH _public_ (not private) key, so you can get passwordless access to the node later
* Spawn a server or process in the background
* Start a server or process in a screen so that later you can SSH into the machine and attach to the screen to monitor the progress of the job or the service

And so on.

## SSH and Identity Management

Identity access management (IAM) and access controls are the most confusing part of any cloud platform - don't feel frustrated if you don't pick it up easily. 

IAM is a way for you to provide limited, specified access to resources that you own/have created, without sharing your credentials.

IAM is useful for you to use yourself (e.g., if you are using Amazon Kinesis and you want it to access an Amazon Redshift database, you can create an IAM for your Amazon Kinesis script that gives it permission to access data in a particular Amazon Reshift database, and run your Kinesis script under that identity). 

IAM is also useful for sharing resources with other AWS users. You can create a VPC and create an IAM group that allows people to manage the network, and add any network administrators to the group. This gives them full control over the network. You can also create an IAM group that gives members the ability to see, but not modify, the network (e.g., billing manager).

[More info on IAM](https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_IAM.html)

## Tricks with Disks

AMI (Amazon Machine Images) provide operating system images that you can use to initialize a new node. But you can also create your own AMIs. Use the EC2 console to create an AMI (image) from any of your running nodes; wait for the snapshot to complete (may take a few minutes); and now you can spawn a new node from the exact state of the existing node.

This is useful for a couple of tasks:
* If you're doing a parameter study of an analysis technique and need to run a process in parallel on the same data set, you can download the data set and set up your code on a single node, create an image once you're finished, then spawn new nodes using that snapshot
* If you already have a node with a huge data set that took hours to download and process, and you realize your node needs another 32 GB of RAM, or a few extra CPUs, you won't be able to resize it on the fly. But you can create an AMI from the running node, shut it down, and create a new node from the image.
* If you created a node in region `us-west-1a` and another node in region `us-east-1c` and you want to connect them together on a VPC, you won't be able to create a VPC that spans regions. But you can create an AMI from one of the running nodes, shut it down, and spawn a new node in the correct region.
* If you have a particularly large data set, a complicated workflow setup, or a custom operating system, you can create a public AMI and share it with others. 
* You can also [privately share AMIs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/sharingamis-explicit.html)

## AWS CLI and Boto3

### AWS from the Command Line

If you've clicked the AWS web interface to death and are looking for a better way of interacting with AWS, you can use `aws-cli`, a command line interface to AWS. This is extremely convenient for scripting common tasks. 

[aws-cli](https://aws.amazon.com/cli/)

This is a really powerful way of interacting with S3 buckets, and makes copying files to/from S3 buckets as easy as copying files in local directories.

### Boto3

The CLI is much more powerful than the web interface, but is still missing some of the options available through the web. For the complicated stuff, use boto3, the Python API for AWS services.

[boto3 on github](https://github.com/boto/boto3)

[boto3 documentation](https://aws.amazon.com/sdk-for-python/)

The basic formula for boto scripts is, you create Python objects representing different consoles or resources (e.g., a VPC object or an EC2 object), and you call functions to perform actions on those resources or in those consoles. These functions can take complicated nested dictionaries as parameters and allow you to specify every option available in AWS.

### To Infinity... And Beyond!

Other libraries like [terraform](https://www.terraform.io/intro/) build on boto3 and simplify the routine tasks of juggling information and configuration details, providing a kubernetes-like dashboard to run and manage an AWS cluster.

## Instance Metadata

One last topic - how to get access to information about your EC2 node, from your EC2 node.

There are some special IP addresses - any IP address starting with 10 is reserved for private networks, as are networks starting with 192.168, and 127.0.0.1 is the IP address that points to yourself.

The IP address 169.254 is another reserved IP block, and is normally used for crossover connections (direct ethernet-to-ethernet connections). Given its uselessness in the cloud, AWS repurposed that IP address to store instance metadata.

This IP address exposes a restful API that you can call with curl. Information is organized hierarchically. For example:

```
$ curl http://169.254.169.254/latest/meta-data/

ami-id
ami-launch-index
ami-manifest-path
block-device-mapping/
hostname
iam/
instance-action
instance-id
instance-type
local-hostname
local-ipv4
mac
metrics/
network/
placement/
profile
public-hostname
public-ipv4
public-keys/
reservation-id
security-groups
services/
```

User data is also available:

```
http://169.254.169.254/latest/user-data
```

as are the IP addresses of network interfaces. The network interface can be specified if there are more than one. To get the private VPC IP, request the `local-ipv4` address:

```
http://169.254.169.254/local-ipv4
```

and to get the public IP address, use `public-ipv4`:

```
http://169.254.169.254/public-ipv4
```

by assigning these values to environment variables, you can write and run a single script across multiple machines, and control the execution behavior across those machines.

[Link to more info on instance data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html#instancedata-user-data-retrieval)

