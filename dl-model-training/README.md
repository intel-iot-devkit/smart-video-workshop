# Deep Learning Tutorial
## MNIST Database - Handwritten digits (0-9)

On this tutorial we will use Python* to implement one [Convolutional Neural Network](https://en.wikipedia.org/wiki/Convolutional_neural_network) - a simplified version of [LeNet](https://en.wikipedia.org/wiki/Convolutional_neural_network#LeNet-5) - that will recognized Handwritten digits. A project like this one, using the MNIST dataset is considered as the "Hello World" of Machine Learning.

We will use [Keras*](https://keras.io), [TensorFlow*](https://www.tensorflow.org) and the [MNIST database](https://en.wikipedia.org/wiki/MNIST_database).

According to the description on their website, *"**Keras** is a high-level neural networks API, written in Python and capable of running on top of TensorFlow, CNTK, or Theano*. **It was developed with a focus on enabling fast experimentation. Being able to go from idea to result with the least possible delay is key to doing good research.**"*

We will use TensorFlow as the backend for Keras. TensorFlow is an open source software library for high performance numerical computation.

The MNIST database is a large database of handwritten digits that is commonly used for training various image processing systems. MNIST database is also available as a Keras dataset, with 60k 28x28 images of the 10 digits along with a test set of 10k images, so it is very easy to import and use it on our code.

One good visual and interactive reference on what we are developing can be found [here](http://scs.ryerson.ca/~aharley/vis/conv/). The basic difference between our code and this interactive sample is the number and size of convolutional and fully-connected layers (LeNet uses two of each, we will use a single one, to reduce training time). We also adjusted the layers size to balance between accuracy and training time. We are achieving 98,54% of accuracy with less than 2 minutes training time on an Intel® Core™ processor.

This code can also be optimized by several ways to increase accuracy, and we would like to invite you to explore this later, changing the number of epochs, filters, fully-connected neurons and also including additional convolutional and fully connected layers. You can also use [flattening](https://keras.io/layers/core/#flatten), [dropout](https://keras.io/layers/core/#dropout) and [batch normalization](https://keras.io/layers/normalization/) layers. Other optimization techniques can also be applied, so feel free to use this tutorial code as a base to explore those optimization techniques.

In a nutshell, the convolutional and pooling layers are responsible for extracting a set of features from the input images, and the fully-connected layers are responsible for classification.

Convolutional layers applies a set of filters to the input image to extract important features from the image. The filters are small matrixes also called image kernels that can be repeatedly applied to the input image ("sliding" the filter on the image). You may already used those filters on traditional image processing applications such as GIMP (i.e. blurring, sharpening or embossing). [This article](http://setosa.io/ev/image-kernels/) gives a good overview on image kernels with some live experiments. Each filter will generate a new image that will be the input for the next layer, typically a pooling layer.

Pooling layers reduces the spatial size of the image (downsampling), reducing the computation in the network and also controlling overfitting.

Fully connected layers are traditional Neural Network layers.

## Installing the Python* libraries

To install the necessary Python libraries on Linux, you need to run:
```
sudo pip install keras tensorflow
```
## Run the tutorial

```
python Deep_Learning_Tutorial.py
```

## How the tutorial code works

The complete code for this tutorial can be found [here](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/dl-model-training/Deep_Learning_Tutorial.py)

### Importing the necessary objects from Keras*

[Sequential Network Model](https://keras.io/models/sequential):

```Python
from keras.models import Sequential
```
[Core Layers](https://keras.io/layers/core/):
  * **Dense:** densely-connected NN layer, to be used as classification layer
  * **Flatten:** layer to flatten the convolutional layers

```Python
from keras.layers import Dense, Flatten
```
[Convolutional Layers](https://keras.io/layers/convolutional/):
  * **Conv2D:** 2D convolution Layer

```Python
from keras.layers import Conv2D
```
[Pooling Layer](https://keras.io/layers/pooling/):
  * **MaxPooling2D:** Max pooling operation for spatial data

```Python
from keras.layers import MaxPooling2D
```
[Utilities](https://keras.io/utils/):
```Python
from keras.utils import np_utils
```
[MNIST Dataset](https://keras.io/datasets/):
  * Dataset of 60,000 28x28 handwritten images of the 10 digits, along with a test set of 10,000 images.

```Python  
from keras.datasets import mnist
```
### Download and load the MNIST database
This will load the MNIST Dataset on four different variables:
  * **train_set:** Dataset with the training data (60k elements)
  * **train_classes:** Dataset with the equivalent training classes (60k elements)
  * **test_dataset:** Dataset with test data (10k elements)
  * **test_classes:** Dataset with the equivalent test classes (10k elements)

```Python
(train_dataset, train_classes),(test_dataset, test_classes) = mnist.load_data()
```
**NOTE:** only on the first run on your machine, this will download the MNIST Dataset.

### Adjust the datasets to TensorFlow*

First step, we need to reduce the image channels, from 3 (color) to 1 (grayscale):
```Python
train_dataset = train_dataset.reshape(train_dataset.shape[0], 28, 28, 1)
test_dataset = test_dataset.reshape(test_dataset.shape[0], 28, 28, 1)
```

Second step, we will convert the data from int8 to float32:
```Python
train_dataset = train_dataset.astype('float32')
test_dataset = test_dataset.astype('float32')
```
Third step, we need to normalize the data to speed up processing time:

```Python
train_dataset = train_dataset / 255
test_dataset = test_dataset / 255
```
Forth step, convert the classes data from numerical to categorical:
```Python
train_classes = np_utils.to_categorical(train_classes, 10)
test_classes = np_utils.to_categorical(test_classes, 10)
```
Now the data is ready to be processed by the CNN.

### Create our Convolutional Neural Network (CNN)

It is very simple and easy to create Neural Networks with Keras. We basically create the network, add the necessary layers, compile and execute the training.

First thing is to create a Sequential Neural Network:
```Python
cnn = Sequential()
```
We now add the input layer, a 2D convolutional layer with 32 filters, 3x3 filter kernel size, input shape of 28 x 28 x 1 (as we adjusted on the training dataset) and using Rectified Linear Unit (relu) as the activation function.

```Python
cnn.add(Conv2D(32, (3,3), input_shape = (28, 28, 1), activation = 'relu'))
```
**NOTE:** We need to inform the *input_shape* parameter only if the convolutional layer is the input layer (first CNN layer). If you add another layers later on, you don't need to use this parameter.

We add one Pooling layer using the default 2x2 size. This means that this layer will reduce by half the input image  in both spatial dimentions.
```Python
cnn.add(MaxPooling2D())
```
At this point, a traditional LeNet network would add another two layers, one convolutional and one pooling, basically repeating the two lines of code we just created, (removing the *input_shape* from the first one). As explained before, to speed processing time and make it more easy to understand, we decided to use just the two layers we just created.

Now we need to convert the output of the polling layer from a matrix to a vector, to be used by the classification part of our neural network. We do that using on flattening layer:
```Python
cnn.add(Flatten())
```

Our data is now ready for the classification part of our neural network, that will be implemented using just two layers, one hidden layer and one output layer.

The first classification layer will be a fully-connected layer with 128 neurons and using rectified linear unit as the activation function.
```Python
cnn.add(Dense(units = 128, activation = 'relu'))
```

We now add another fully-connected layer that will be our output layer. Please note that this layer has 10 neurons, because we have 10 classes on our dataset. The activation function user here is Softmax.
```Python
cnn.add(Dense(units = 10, activation = 'softmax'))
```

Before we train the model, we need to "compile" it to configure the learning process.

We will compile the CNN using *categorical crossentropy* as the loss function, *adam* as the optimizer and using accuracy as the results evaluation metric that will be show on the end of each apoch and also on the end of the training process.

```Python
cnn.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
```
**NOTE:** Adam is a gradient descent optimization algorithm. A good introduction to Adam can be found [here](https://machinelearningmastery.com/adam-optimization-algorithm-for-deep-learning/).

Our CNN is now ready to be trained.

### Training our CNN

To train the CNN we call the Fit method. On this training we will define:
  * **Training dataset and training classes:** our training dataset and training classes adjusted on the beginning of this tutorial.
  * **Batch size:** number of samples to be used per each gradient update, in our case, 128 (default is 32).
  * **epochs:**  number of epochs that will be used on the training, in our case, 5 (for time saving purposes).
  * **validation_data:** the dataset used to validate the training on the end of each epoch. Here is where we inform out test dataset.

```Python
cnn.fit(train_dataset, train_classes, batch_size = 128, epochs = 5, validation_data = (test_dataset, test_classes))
```
It will take a few minutes to run, and it will inform you the progress on the console. Note that it will inform the evolution of the loss (*loss:*) and accuracy (*acc:*) during the execution of each epoch, and this data is computed using the training data, so it cannot be used to evaluate the improvement of the epoch on the overall accuracy.

At the end of each epoch, Keras will use the test dataset we provided to evaluate the epoch results, and this data will be displayed as *val_loss:* and *val_acc:* and those are good parameters to follow on each epoch to see how the accuracy improves. In general, the more epochs you run, more accuracy you will have (and more time you will need to run the training), but **increasing the number of epochs is just one drop on the ocean of possibilities we have to optimize our CNN.**

### Evaluating the training results

The simplest way to evaluate the training results is to use the *evaluate* method. It will show the same data as we saw on *val_loss* and *val_acc* on the end of the last epoch, but now we can use this data. On our tutorial, we will just print it on the console:
```Python
result = cnn.evaluate(test_dataset, test_classes)
print ('Accuracy = ' + str(result[1] * 100) + "%")
```
To have detailed information about our network accuracy for each class, we can use one confusion matrix (a.k.a error matrix). *Scikit-learn* library can be used to do that and more information about it can be found [here](http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html). We will not implement the confusion matrix on this tutorial, but there are several online samples on how to create a confusion matrix using Keras and Scikit-learn and also on how to interpret the results.
