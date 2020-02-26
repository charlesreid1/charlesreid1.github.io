Title: Deconvoluting Convolutional Neural Networks
Date: 2019-05-29 14:00
Category: Machine Learning
Tags: deep learning, machine learning, neural networks, python, keras, convolutional neural networks, cnn

[TOC]

# Introduction: A Simple CNN Example

As part of our weekly Deep Learning for Genomics reading group
here in the [Lab for Data Intensive Biology (DIB Lab)](http://ivory.idyll.org/lab/),
we are applying convolutional neural networks (deep learning) 
to various problems in genomics and biology.

For the most recent meeting, we prepared some notes on how convolutional
neural networks work. The notes are in the form of a Jupyter notebook.
This blog post summarizes some of the important conclusions from the
notebook and links to relevant sections in the notebook.

In the notebook covered in this blog post, we set up a 
simple convolutional neural network from an example on the
[keras blog](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html).
This example is used to classify input images as being either
a cat or a dog.

All materials covered in this blog post are in the 
[charlesreid1/deconvoluting-convolutions](https://github.com/charlesreid1/deconvoluting-convolutions)
repository on Github.


# Exploring the Data

**TL;DR:** When developing a deep learning model for a problem,
it is important to start by exploring the data and understanding
it thoroughly. 

[Link to "Image Data" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Image-Data)


# Create CNN

**TL;DR:** Our convolutional neural network consists of the following architecture:

* Convolutional Stage #1
    * Convolution (3 x 3 kernel, 32 filters)
    * Activation (ReLU)
    * Max Pooling (2x2)
* Convolutional Stage #2
    * Convolution (3 x 3 kernel, 32 filters)
    * Activation (ReLU)
    * Max Pooling (2x2)
* Convolutional Stage #3
    * Convolution (3 x 3 kernel, 64 filters)
    * Activation (ReLU)
    * Max Pooling (2x2)
* Flatten
* Dense (64 nodes)
* Activation (ReLU)
* Dropout (0.5)
* Dense (1 node)
* Activation (ReLU)

[Link to "Create Convolutional Neural Network" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Create-Convolutional-Neural-Network)


# Analyzing Network Architecture and Tensor Shapes

**TL;DR:** Each step of the neural network transforms
an input tensor of a given shape into an output tensor
of a (potentially different) shape.

In this section of the notebook, we step through each
of the neural network's layers to explain how the size
of each layer's inputs and outputs are determined.

[Link to "Network Architecture/Shapes" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Network-Architecture/Shapes)


## Input Image Layer

**TL;DR:** The size of the cat and dog images is 150 x 150 pixels.
Each image is a color image, so it consists of 3 channels. Therefore,
the input to the very first layer has a shape of

$$
(\mbox{None}, w_0, h_0, c_0) = (\mbox{None}, 150, 150, 3)
$$

(where "None" indicates a variable-size dimension that is equal to
the number of total input images, or alternatively, the number of 
images per batch, if we are using batch learning).

[Link to "Input Image Layer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Input-Image-Layer)


## First Convolution Layer

**TL;DR:** A convolutional layer with a kernel size of $k_1 \times k_1$
and a number of filters $c_1$ will transform the shape of the input image to:

$$
(\mbox{None}, w_1, h_1, c_1) = 
(\mbox{None}, 148, 148, 32)
$$

where

$$
w_1 = w_0 - k_1 + 1 \\
h_1 = h_0 - k_1 + 1
$$

Importantly, each of the three input channels are added together to determine
their contribution to the final convolution filters - the number of input channels
does not affect the number of output channels. 

The total number of output channels is equal to the number of filters
in the convolution layer. 

[Link to "First Convolutional Layer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#First-Convolution-Layer)


## First Activation Layer

**TL;DR:** The activation layer is a straightforward one-to-one mapping -
each individual value from the output of the convolution layer is fed through
the rectified linear unit (ReLU) function and the resulting output value becomes
the input to the next layer. The ReLU function is given by:

$$
\mbox{ReLU}(x) = \max(0,x)
$$

The activation layer does not change the shape of the input tensor.

[Link to "First Activation Layer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#First-Activation-Layer)


## First MaxPooling Layer

**TL;DR:** The max pooling layer is a way of making the final convolutional
filters (the "feature-detectors" of the convolutional neural network) less 
sensitive to the exact placement of features. The pooling layer only affects
the size of the filter, not the number of channels.

If we use a max pooling window of $p_1 \times p_1$, we will reduce the image
size by $\mbox{ceil}(w_1/p_1)$ and $\mbox{ceil}(h_1/p_1)$. This reduces the input tensor shape
to:

$$
(\mbox{None}, \mbox{ceil}(w_1/p_1), \mbox{ceil}(h_1/p_1), c_1) = 
(\mbox{None}, 74, 74, 32)
$$

[Link to "First Max Pooling Layer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#First-Max-Pooling-Layer)


## Second Convolution Layer

**TL;DR:** The second convolutional layer has a kernel size 
of $k_2 \times k_2$ and a number of filters $c_2$, which will
transform the shape of the input image in the same way as 
described for the first convolutional layer.

Note that just as the number of channels (3) in each 
input to the first convolutional layer did not affect
the final number of channels in the output of the convolutional
layer (number of channels was fixed by specifying number of
output filters for the convolutional layer), so the number of
input channels to the second convolutional layer does not affect 
the number of output channels from the second convolutional
layer.

The final shape coming out of the second convolutional layer is:

$$
(\mbox{None}, w_2, h_2, c_2) = 
(\mbox{None}, 72, 72, 32)
$$

where

$$
w_2 = w_1 - k_2 + 1 \\
h_2 = h_1 - k_2 + 1 \\
$$

[Link to "Second Convolutional Layer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Second-Convolution-Layer)


## Second Activation Layer

**TL;DR:** The activation layer again uses a function to
map input values to output values in a one-to-one mapping,
so the activation layer does not change the shape of the 
input tensor.

[Link to "Second Activation Layer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Second-Activation-Layer)


## Second MaxPooling Layer

**TL;DR:** The second max pooling layer uses a pooling
window of size $p_2 \times p_2$. This will reduce the input
size to $\mbox{ceil}(w_2/p_2) \times \mbox{ceil}(h_2/p_2)$. This reduces 
the input tensor shape to:

$$
(\mbox{None}, \mbox{ceil}(w_2/p), \mbox{ceil}(h_2/p), c_2) = 
(\mbox{None}, 36, 36, 32)
$$

[Link to "Second Max Pooling Layer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Second-Max-Pooling-Layer)


## Third Convolution Layer

**TL;DR:** The third convolution layer with a kernel size 
of $k_3 \times k_3$ and $c_3$ output filters will transform
the input tensor shape in the following way (note that the
third convolutional layer has 64 filters, not 32):

$$
(\mbox{None}, w_3, h_3, c_3) =
(\mbox{None}, 34, 34, 64)
$$

where

$$
w_3 = w_2 - k_3 + 1 \\
h_3 = h_2 - k_3 + 1
$$

[Link to "Third Convolutional Layer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Third-Convolution-Layer)


## Third Activation Layer

**TL;DR:** The activation layer again uses a function to
map input values to output values in a one-to-one mapping,
so the activation layer does not change the shape of the 
input tensor.

[Link to "Third Activation Layer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Third-Activation-Layer)


## Third MaxPooling Layer

**TL;DR:** The thid max pooling layer uses a pooling
window of size $p_3 \times p_3$. This will reduce the input
size to $\mbox{ceil}(w_3/p_3) \times \mbox{ceil}(h_3/p_3)$. This reduces 
the input tensor shape to:

$$
(\mbox{None}, \mbox{ceil}(w_3/p_3), \mbox{ceil}(h_3/p_3), c_2) = 
(\mbox{None}, 17, 17, 64)
$$

[Link to "Third Max Pooling Layer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Third-Max-Pooling-Layer)


## Flatten and Dense Layers

**TL;DR:** The flatten layer converts a tensor of dimension $(\mbox{None}, 17, 17, 64)$
into a 1D vector of $17 \times 17 \times 64 = 18,496$ neural network nodes. This does not
change any of the values, it simply reshapes the input tensor.

The first dense layer reduces the flattened $18,496$ nodes to $64$ nodes, using a fully connected
layer of nodes. These values are then passed through an activation function (as with the above
activation layers, this is a one-to-one mapping and does not change the shape of the input tensor).
The dense layer is followed by a dropout layer to help prevent overfitting; this pattern is common
in convolutional neural networks.

The second dense layer further reduces the $64$ nodes to a single node, whose output will determine
whether the input image is a cat or a dog.

[Link to "Flatten Layer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Flatten-Layer)

[Link to "Dense (64) Layers" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Dense-(64))

[Link to "Dense (1) Layers" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Dense-(1))


## Categorical Output

**TL;DR:** Normally when classifying cats and dogs, we would have two output neurons, one to
output a binary yes/no to answer "is this a cat?" and another output a binary yes/no to answer 
"is this a dog?". However, in this example, we assume that _all_ inputs contain either only cats
or only dogs, so the single-output binary classifier is determining whether an image is a dog (0)
or a cat (1).



# Image Transformer

**TL;DR:** The `ImageDataGenerator` class is a class provided by keras
for loading image data from a directory and (optionally) applying various
transformations to the images in order to generate additional training data
from a set of images. For example, the following code block from the 
notebook creates an `ImageDataGenerator` class that will load images from a
folder on disk, and applies various transformations (shearing, zooming, 
and horizontally flipping) to each image during the training process.

```python
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)
```

This can then be used to generate test image data:

```python
train_generator = train_datagen.flow_from_directory(
    'train',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')
```

This will look for images in the relative path `train/data/`
(note the implicit `data/` directory tacked on the end).
Note that this image data generator allows us to use images
that do not have size $150 \times 150$, as they will be re-sized
to `target_size`.

[Link to "Image Transformer" section of notebook](https://tinyurl.com/deconvoluting-convolutions#Image-Transformer)


## Next Steps

Now that we have walked through a sample convolutional neural network
and covered how each layer transforms the size of the input tensor, 
we are ready to start applying convolutional neural networks to real
problems.

Our next blog post will cover the materials in the
[charlesreid1/deep-learning-genomics](https://github.com/charlesreid1/deep-learning-genomics)
repository on Github, which applies the convolutional neural 
network concept in a 1D context (applying convolutions to 1D sequences, 
instead of 2D images) to learn about (and predict) DNA transcription factor 
binding sites.  

