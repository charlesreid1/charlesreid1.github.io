Title: Deep Learning for Genomics: Part 1: Keras Convolutional Neural Networks for DNA Sequences
Date: 2019-05-08 14:00
Category: Computational Biology
Tags: python, keras, computational biology, bioinformatics, algorithms, dna, machine learning, deep learning, neural networks, convolutional neural networks, cnn
Status: draft

# Table of Contents

* Context: deep learning for biological sciences

* Problem statement: predicting DNA binding sequences
    * The data
    * Sequence data
    * Chromatin data

* Building the neural network
    * Convolutional neural network (1d for sequence)
    * 1D Convolutional neural network architecture

* 1D CNN: Sequence Data Only
    * Creating the network architecture
    * Preparing the data
    * Training the model
    * Assessing the model

* 1D CNN: Sequence and Chromatin Data
    * Creating the network architecture
    * Preparing the data
    * Training the model
    * Assessing the model

# Context: Deep Learning for the Life Sciences (the O'Reilly Book)

Lately we have been involved with a deep learning reading group
that is just getting started at the [Lab for Data-Intensive Biology](https://ivory.idyll.org/lab/),
captained by Professor Titus Brown (both the lab and the reading group).

To get us started, we've been following along with a
recently-published O'Reilly book, [<u>Deep Learning for the
Life Sciences</u>](https://www.oreilly.com/library/view/deep-learning-for/9781492039822/).
The entire book focuses on the use of deep learning
and neural networks for various problems in the biological
sciences, but we are particularly interested in Chapter 6,
"Deep Learning for Genomics".

In particular, we're interested in the content of Chapter 6,
which is on utilizing neural networks for genomic sequences.

In this post we'll walk through the basics of setting up
a 1D convolutional neural network in [Keras](https://keras.io)
(a neural networks library in Python) to learn from
sequential 1D data (like a DNA sequence).

# The Problem: DNA Binding Sequences

We motivate the problem of setting up a neural network and making
predictions using sequential data using a problem presented
in Chapter 6: the problem of predicting when a DNA sequence
will be a binding site for a transcription factor.

A sequence of DNA is a string of characters drawn from a
four-letter alphabet, GTAC, corresponding to guanine, thymine,
adenine, and cytosine. This chain of DNA is a way of storing
information in a chain of macromolecules.

To turn this biological information into biological function, 
the DNA must first be converted into RNA, and the RNA is
then converted into proteins, ribozymes, and other functional
macromolecules.

The conversion of DNA to RNA is the process of [transcription](https://en.wikipedia.org/wiki/Transcription_(biology))
and begins with the molecule responsible for RNA creation,
called RNA polymerase, binding to the DNA at a particular
location, called a "promoter".  

For obvious reasons, it is useful to be able to predict
where DNA transcription into RNA begins. But it is difficult
to predict, as there are many rules and special cases.

This is the type of problem that deep learning is well-suited
for: a problem that is too complicated for a human to fully
enumerate with rules, and for which there are mountains of
data to train a machine learning algorithm.

## The Data

Data for this problem are contained in the [deepchem/DeepLearningLifeSciences](https://github.com/deepchem/DeepLearningLifeSciences)
repository on Github in the Chapter06 folder.

The data are stored in four files - one for each of the variables
$X$ (input matrix), $y$ (output values), $w$ (weights), and
ids (labels).

The data are stored in the [joblib](https://github.com/joblib/joblib)
format, so you will need the joblib Python module
installed to load it (we cover this in the 
prerequisites section below).

The joblib files are similar to Python pickles; they store the
data in an encoded format that makes it possible to quickly
dump and load the data as numpy arrays.

### Sequence Data

### Chromatin Data

## Required Packages

First, we should state that despite the fact that the book
<u>Deep Learning for the Life Sciences</u> is written using
the [deepchem](https://github.com/deepchem/deepchem)
deep learning library, we had a number of difficulties
installing deepchem and ended up converting the neural
networks from deepchem to Keras. Thus, deepchem is not 
required to follow along with this blog post.

What is required:

* [joblib](https://github.com/joblib/joblib)
* [numpy](https://www.numpy.org/)
* [sklearn](https://scikit-learn.org/)
* [keras](https://keras.io)
* [matplotlib](https://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/)

# Building the Neural Network

keras
sequential model
add layers

## Convolutional Neural Networks

cnn layers/pattern
2d example
1d example

## 1D Convolutional Neural Networks for Sequences



<br />
<br />

# 1D CNN: Sequence Data Only

## Creating the Network Architecture

## Preparing the Data

## Training the Model

## Assessing the Model


<br />
<br />

# 1D CNN: Sequence and Chromatin Data 

## Creating the Network Architecture

## Preparing the Data

## Training the Model

## Assessing the Model



