Title: Timing and Profiling Go Code
Date: 2018-12-28 20:00
Category: Rosalind
Tags: go, golang, rosalind, bioinformatics
Status: draft

## Performance of Iterative Approach

- timing
- profiling (line by line)
- why string construction is slow

## Improving Performance with Alternate Data Structure

solutions that don't change the algorithm:
- use a string buffer
- list of strings, joining them at the end
- use fact that you know length of DNA string

## Improving Performance with Alternate Algorithm

alternate algorithm:
- reducing DNA to different type

solutions that don't change the approach:
- use a string buffer
- use a list of strings and join them at the end
