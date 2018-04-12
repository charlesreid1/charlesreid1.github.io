Title: AWSome Day Seattle Notes: Part 1: The Basics
Date: 2017-04-11 10:00
Category: Charlesreid1
Tags: aws, cloud, vpc, containers, data engineering

These notes are also available on [git.charlesreid1.com](https://git.charlesreid1.com/charlesreid1/aws/src/branch/master/awsome-day-sea-2018)

# AWSome Day Notes: Part 1: The Basics

Following are some notes from Amazon's AWSome Day (Tuesday, February 27, 2018).

## EC2 Costs and Scheduling

Cost of a node:
* Important to understand Amazon's price model: users pay for *access*, not for *hardware*
* Cost of AWS node is cost for *on the spot access*

Scheduling:
* If you can anticipate your usage, you can schedule instances in advance, and get a discount
* Discount of 50% for one-year reservation (if you keep it busy for 6 months, you've made your money back)
* Spot instances also available - need to be robust to sudden starts/stops (good for embarrassingly parallel jobs)
* Cheaper to anticipate your usage and plan ahead

## EC2 Transfer Costs

EC2 Instances:
* See [EC2 Instance Pricing - Data Transfer](https://aws.amazon.com/ec2/pricing/on-demand/) section
* Network costs for AWS nodes are an important consideration for high-traffic nodes (>10 TB)

EC2-Internet:
* Traffic going from the internet *into* a node is always free
* Traffic going from the node *out* to the internet incurrs costs after 10 TB
* Outbound traffic costs ~$90/TB

AWS Regions:
* Traffic *within* a region does not incur costs (well... it's complicated)
* Traffic *between* regions will incur costs

EC2-S3:
* Transfer *into* an EC2 node from S3 bucket in same AWS region does not incur costs
* Transfer *out of* an EC2 node into S3 bucket in same AWS region does not incur costs
* (If they did charge you, they would be double-dipping...)

Note: the list of prices is like a legal document, so use the [AWS Monthly Calculator](https://calculator.s3.amazonaws.com/index.html) to estimate monthly costs with more detail.

## S3 Transfer Costs

* See [S3 Pricing - Data Transfer](https://aws.amazon.com/s3/pricing/)
* Price model for storage is simliar to price model for AWS nodes: you pay for *access*, not for *hardware*
* To give a sense of why, think about logistics of a large "disk farm": all the intensive operations are done by the head nodes, disks are just passive
* Busier disk farm needs sophisticated hardware for parallel read/write, high-bandwidth network lines, fast encryption

S3 storage pricing:
* Rule of thumb: ~$20/TB to store the data

S3-Internet:
* Transfer *into* an S3 bucket from the internet is always free (getting stuff into the bucket is the easy part - that's how they get ya)
* Transfer *out* of an S3 bucket to the internet costs ~$90/TB

S3-EC2:
* Transfer *out* of an S3 bucket to most other Amazon regions costs ~$20/TB
* Transfer *out* of an S3 bucket into an EC2 node in the same AWS region does not incur costs
* Transfer *into* an S3 bucket from an EC2 node in the same AWS region does not incur costs

As mentioned above, this means you won't be double-charged for transferring data from an S3 bucket to an EC2 node, then from the EC2 node out to the internet.

## S3 Storage Hierarchies

Continuing with the theme of planning ahead...

Storage hierarchies:
* Biggest cost of storage is not disk space, it's transfer
* Paying for speed, paying for timeliness, paying for *on the spot access* to your data
* Your data will be cheaper if you're willing to wait a few minutes or deal with a slow connection

Storage hierarchies:
* Standard (~$20/TB)
* Infrequent access (~$13/TB) - less frequent access, but at same transfer speed
* Glacier (~$4/TB) - delay of up to 12 hours (smaller files = faster), deleting data *newer* than 3 months incurrs costs

[Glacier Pricing](https://aws.amazon.com/glacier/pricing/)

Lifecycle rules:
* Can create rules to move old data from S3 buckets into Glacier

## EFS vs EBS vs S3

When do you use EFS, EBS, or S3?

Elastic Block Storage (EBS):
* **This is probably what you want**
* EBS is block storage for one EC2 node - designed for general purpose applications
* Cost: ~$120/TB/mo

Elastic File System (EFS):
* EFS is block storage for multiple EC2 nodes - designed for fast read-write operations, many incremental changes to files
* "Elastic" part of EFS - can dynamically grow as hard drive grows (PB+ scale)
* Hard drive on steroids - like plugging in a hard drive over a network, but big/fast/smart enough to be accessible to thousands+ of machines
* Expensive: ~$300/TB/mo

S3:
* S3 is object storage - it stores blobs of raw data, creates snapshots in time
* If you change a single character of a large file, bucket has to create new shapshot
* Booting from S3 as a hard disk would take you about a thousand years... don't do that
* Cheapest: ~$20/TB

Cool but $$$:
* You may see "appliances" mentioned in Amazon documentation - Amazon will ship you a physical data transfer appliance that encrypts and copies data on site ([Snowball](https://docs.aws.amazon.com/snowball/latest/ug/images/Snowball-closed-600w.png))
* Can also purchase special network connections that bypass the public internet - like ISP putting alligator clips between your network lines and Amazon's network lines


