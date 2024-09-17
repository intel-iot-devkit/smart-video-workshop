'''
  Copyright (c) 2018 Intel Corporation.

  Permission is hereby granted, free of charge, to any person obtaining
  a copy of this software and associated documentation files (the
  "Software"), to deal in the Software without restriction, including
  without limitation the rights to use, copy, modify, merge, publish,
  distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so, subject to
  the following conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

# Good visual ilustration of the model we will build
# http://scs.ryerson.ca/~aharley/vis/conv/

# Sequential Network Model https://keras.io/models/sequential/
from keras.models import Sequential
# Core Layers https://keras.io/layers/core/
# Dense: densely-connected NN layer, to be used as classification layer
# Flatten: layer to flatten the convolutional layers
from keras.layers import Dense, Flatten
# Convolutional Layers https://keras.io/layers/convolutional/
# Conv2D: 2D convolution Layer
from keras.layers import Conv2D
# Pooling Layer: https://keras.io/layers/pooling/
# MaxPooling2D: Max pooling operation for spatial data
from keras.layers import MaxPooling2D
# Utilities https://keras.io/utils/
from keras.utils import np_utils
# MNIST Dataset https://keras.io/datasets/
# Dataset of 60,000 28x28 handwritten images of the 10 digits, along with a test set of 10,000 images.
from keras.datasets import mnist

# Load MNIST data set in two sets: Trainning (60K IMAGES) and Testing (10k images)
(train_dataset, train_classes),(test_dataset, test_classes) = mnist.load_data()

# Adjust datasets to TensorFlow
# Reduce image channels from 3 to 1
train_dataset = train_dataset.reshape(train_dataset.shape[0], 28, 28, 1)
test_dataset = test_dataset.reshape(test_dataset.shape[0], 28, 28, 1)

# Covert data from int8 to float32
train_dataset = train_dataset.astype('float32')
test_dataset = test_dataset.astype('float32')

# Normalize data to speed up processing time
train_dataset = train_dataset / 255
test_dataset = test_dataset / 255

# Convert class data from numerical to categorical
train_classes = np_utils.to_categorical(train_classes, 10)
test_classes = np_utils.to_categorical(test_classes, 10)

# Create the Convolutional Neural Network
cnn = Sequential()

# Add the convolutional layer with 32 filters, 3x3 convolution window,
# 28 x 28 x 1 pixels imput array and Rectified Linear Unit activation function
cnn.add(Conv2D(32, (3,3), input_shape = (28, 28, 1), activation = 'relu'))

# Add one Pooling layer with default 2x2 size
cnn.add(MaxPooling2D())

# Add one flattening layer to convert the output matrix to a vector to be the Deep Neural Network input
cnn.add(Flatten())

# Add one hidden layer with 128 neurons and Rectified Linear Unit activation function
cnn.add(Dense(units = 128, activation = 'relu'))

# Add the output layer with 10 neurons (one for each class) with Softmax as the activation function
cnn.add(Dense(units = 10, activation = 'softmax'))

# Compile the CNN with:
#  - Categorical crossentropy as the loss function
#  - Adam optimizer
#  - Accuracy as the results evaluation metric
cnn.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

# Execute the training on 5 epochs, validating the generated model with test dataset on each epoch
cnn.fit(train_dataset, train_classes, batch_size = 128, epochs = 5, validation_data = (test_dataset, test_classes))

# Extract and print the Accuracy results
result = cnn.evaluate(test_dataset, test_classes)
print ('Accuracy = ' + str(result[1] * 100) + "%")
