Title: Undergraduate Research Project: Wireless Sensor Networks for Internet of Things Applications (Part 2: The Technologies)
Date: 2017-05-14 12:00
Status: draft
Category: Wireless
Tags: wireless, security, undergraduate research project, stunnel, SSH, aircrack, mongodb, python, jupyter, linux, raspberry pi

* [Undergraduate Research (UGR) Project: The Technologies](#ugr2-tech)
	* [Overview of the UGR Project](#ugr2-overview)
	* [Student-Led Components](#ugr2-student)
		* [Raspberry Pi](#ugr2-pi)
		* [Pi Networking Issues](#ugr2-network-issues)
		* [NoSQL Database](#ugr2-db)
	* [Backend Components](#ugr2-backend)
	* [Technologies Flowchart](#ugr2-flowchart)

# Undergraduate Research Project (UGR): The Technologies

In this post we'll cover some of the technologies that were used in our
South Seatte College undergraduate research project.
The project involved an ensemble of different technologies
to complete each component of the data analysis pipeline.
Some components were planned for, but other components 
were implemented due to "surprise" challenges that cropped up 
during the course of the project, while yet more technologies
were integrated into the pipeline to avoid extra costs. 

<a name="ugr2-tech"></a>
## Overview of the UGR Project

Before we go further, let's recap what the project was all about.
As the research project mentor, I was leading a group of five undergraduate 
students in a project entitled "Wireless Sensor Networks for Internet of Things
Applications." This invovled guiding students through the construction of a data analysis
pipeline that would utilize a set of sensors, each collecting data about wireless networks 
in the vicinity, and collect the data into a central database. We then impemented
data analysis and visualization tools to analyze the sensor data that was collected
and extract meaningful information from it.

There were three major sets of tools used - those used onboard the Raspberry Pi sensors
(to extract and transfer wireless data), those used to store and organize 
the wireless sensor data (NoSQL database tools), and those used to process,
analyze, and visualize the data colleted (Python data analysis tools).

The technologies used can be classified two ways:
* ***Student-Led Components*** - the software components of the pipeline 
	that students learned about, and whose implementation was student-led. 
* ***Backend Components*** - the software components of the pipeline
	that were too complicated, too hairy, and/or too extraneous to the project
	objectives to have students try and handle. These were the components of the project
	that "just worked" for the students. 

<a name="ugr2-student"></a>
## Student-Led Components

<a name="ugr2-pi"></a>
### Raspberry Pi

The Raspberry Pi component presented some unique challenges, with the chief being,
enabling the students to actually remotely connect via SSH to a headless Raspberry Pi. 

This deceptively simple task requires an intermediate knowledge of computer networking,
and coupled with finnicky Raspberry Pi hardware, an overly-restrictive school network,
the fact that network connections to the Pis were being made via Linux virtual machines, 
and the awful way that the Windows operating system (which **all** of the students were using)
takes away your control of your own system and hardware, it took more than a month 
for students to consistently boot up the Pi, remotely SSH to the Pi, and get a command line. 

(Coupled with unfamiliarity with SSH and Linux in general, this left students with a skewed first impression
of SSH and Linux. Despite my many assurances that connecting to remote Linux machines is rarely 
that challenging, the students did not really believe me.) 

Once the students had reached the Raspberry Pi command line, we moved on to our next major tool - 
the [aircrack-ng](https://aircrack-ng.org) suite. This was a relatively easy tool to get working,
as it was already available through a package manager (yet another new concept for the students), 
so we did not waste much time getting aircrack operational and gathering our first sensor data. 
However, to interpret the output of the tool required spending substantial time covering 
many aspects of networking - not just wireless networks, but general concepts like packets,
MAC addresses, IP addresses, DHCP, ARP, encryption, and the 802.11 protocol specification.

Initially I had thought to use a Python library called [Scapy](http://secdev.org/projects/scapy/),
which provides functionality for interacting with wireless cards and wireless packets directly from Python.
My bright idea was to use aircrack to show students what kind of information about wireless networks
can be extracted, and to write a custom Python script that would extract only the information we were
interested in.

Unfortuantely, the complexity of Scapy, and the advanced level of knoweldge of the 802.11 protocol 
required of users (even to read the documentation), meant the students were dead in the water with Scapy.
Rather than write a magic tool that did everything for them, I dumped (the more flexible) Scapy 
in favor of (the simpler) Aircrack.

The approach we adopted was to collect wireless network data using aircrack, 
and to dump the network data at short intervals (15 seconds) to a CSV file. 
These CSV files were then post-processed with Python to extract information 
and populate the database. 

By the time students were able to utilize aircrack to collect wireless network data
into CSV files, we were nearly at the end of the first quarter of the project. 

<a name="ugr2-network-issues"></a>
### Pi Networking Issues

Further complicating the process of collecting wireless network data from 
Raspberry Pis was the fact that we were gathering data from the Pis in a
variety of different environments - most of which were unfamiliar, 
and would not reliably have open wireless networks or networks that the Pi
was authorized to connect to. 
Even on the South Seattle campus, the network was locked down, with only
HTTP, HTTPS, and DNS traffic allowed on ports 80, 443, and 53, respectively.

This meant we couldn't rely on the Pis making a direct connection to the 
remote server holding the central database. 

Instead, we utilized rsync to synchronize the CSV files gathered by the Pi
with the remote server, and we offloaded the process of extracting and analyzing 
data from the CSV files to a script on the remote server.

That way, the Pis gather the raw data and shuttle the raw data to the remote server
(whenever it is available), and the data extraction and analysis process can be performed
on the raw data in the CSV files as many times as necessary. If the analysis 
required different data, or needed to be re-run, the process could simply be updated
and re-run on the databae server, with the Raspberry Pi removed from the loop.

<a name="ugr2-db"></a>
### NoSQL Database

We needed a warehouse to store the data that the Raspberry Pis were gathering.
The aircrack script was dumping CSV files to disk every 15 seconds. 
Rather than process the data on-board the Raspberry Pi, 
the script to extract and process data from the CSV files 
was run on the computer running the database.

This is a good general principle - put off the actual extraction and processing 
of sensor data until it is absolutely needed; keep the original, raw data 
whenever possible; assume that each component of your pipeline is unreliable and 
will break at some point (build the pipeline to be asynchronous).

We used a cheap, $5/month virtual private server from Linode
to run the database. The database technology we chose was MongoDB,
mainly because it is a ubiquitous, open-source, network-capable 
NoSQL database. The NoSQL option was chosen to give students
flexibility in structuring the database, and avoid the pain and suffering
of making a weakly-typed language like Python talk to a strongly-typed 
database system like SQLite or PostgreSQL.

We ran the database on the server, but students had a hard time 
really *grokking* what was going on with the SQL server. So  we also had
a Mongo Express instance set up, to help students interact visually with 
the MongoDB documents and collections. This proved to be a magic ingredient 
that allowed students to make much faster progress with the database portion.

Using MongoDB and its Python bindings (PyMongo) also meant that students could 
install it on a Linux virtual machine and practice with basic database operations
(running basic queries and populating Python data structures with the results)
on their own computers.

The students struggled primarily with the extraction process - figuring out what data
to load from the aircrack CSV files, and how to add it to the NoSQL database.
This was due again to the fact that students had trouble separating the 
principle of the data pipeline (building a system that extracts and stores data)
from the specific questions that the wireless data could answer 
(which was a secondary focus of the project).

<a name="ugr2-backend"></a>
## Backend components





