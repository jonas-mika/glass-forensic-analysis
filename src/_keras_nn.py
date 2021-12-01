"""
    A simple neural network written in Keras (TensorFlow backend) to classify the IRIS data
"""

import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from sklearn.metrics import accuracy_score

iris_data = load_iris() # load the iris dataset

x = iris_data.data
y_ = iris_data.target # Convert data to a single column

# One Hot encode the class labels
encoder = OneHotEncoder(sparse=False)
y = encoder.fit_transform(y_.reshape(-1, 1))
#print(y)

# Split the data for training and testing
#train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.20)

# Build the model

model = Sequential()

model.add(Dense(10, input_shape=(4,), activation='relu', name='fc1'))
model.add(Dense(10, activation='relu', name='fc2'))
model.add(Dense(3, activation='softmax', name='output'))

# Adam optimizer with learning rate of 0.001
optimizer = Adam(lr=0.001)
model.compile(optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

print('Neural Network Model Summary: ')
print(model.summary())

# Train the model
model.fit(x, y, verbose=0, batch_size=5, epochs=100)

# Test on unseen data
#print(sum(np.argmax(model(train_x).numpy(), axis=1) == train_y) / 150)

pred = np.argmax(model.predict(x), axis=1)
print(pred)
print(y)
print(accuracy_score(y_, pred))

results = model.evaluate(x, y)

print('Final test set loss: {:4f}'.format(results[0]))
print('Final test set accuracy: {:4f}'.format(results[1]))
