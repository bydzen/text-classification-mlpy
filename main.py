# -*- coding: utf-8 -*-
"""Copy of Deep Learning for Text Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SGAPBW2KyI8hbmN85jbAJ1BFF_numZkd

# Import Libraries
"""

import numpy as np
from keras.layers import Activation, Conv1D, Dense, Embedding, Flatten, Input, MaxPooling1D, SimpleRNN
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.datasets import fetch_20newsgroups
from keras.metrics import categorical_accuracy

"""# Preprocessing the data
You already learned that we have to tokenize the text before we can feed it into a neural network. This tokenization process will also remove some of the features of the original text, such as all punctuation or words that are less common.
"""

# http://qwone.com/~jason/20Newsgroups/
dataset = fetch_20newsgroups(subset='all', shuffle=True)

texts = dataset.data # Extract text.
target = dataset.target # Extract target.

dataset.target_names

print (target[:10])

print (len(texts))
print (len(target))
print (len(texts[0].split()))
print (texts[0])
print (target[0])
print (dataset.target_names[target[0]])

"""Remember we have to specify the size of our vocabulary. Words that are less frequent will get removed. In this case we want to retain the 20,000 most common words."""

vocab_size = 20000 # Define the vocabulary size

tokenizer = Tokenizer(num_words=vocab_size) # Setup tokenizer
tokenizer.fit_on_texts(texts) # Fitting the tokenizer on the data
sequences = tokenizer.texts_to_sequences(texts) # Generate sequences

print (tokenizer.texts_to_sequences(['Hello King, how are you?']))

print (len(sequences))
print (len(sequences[0]))
print (sequences[0])

word_index = tokenizer.word_index
print('Found {:,} unique words.'.format(len(word_index)))

"""Our text is now converted to sequences of numbers. It makes sense to convert some of those sequences back into text to check what the tokenization did to our text. To this end we create an inverse index that maps numbers to words while the tokenizer maps words to numbers."""

# Create inverse index mapping numbers to words
inv_index = {v: k for k, v in tokenizer.word_index.items()}

# Print out text again
for w in sequences[0]:
    x = inv_index.get(w)
    print(x,end = ' ')

"""# Measuring text length
Let's ensure all sequences have the same length.
"""

# Get the average length of a text
avg = sum(map(len, sequences)) / len(sequences)

# Get the standard deviation of the sequence length
std = np.sqrt(sum(map(lambda x: (len(x) - avg)**2, sequences)) / len(sequences))

avg,std

"""You can see, the average text is about 300 words long. However, the standard deviation is quite large which indicates that some texts are much much longer. If some user decided to write an epic novel in the newsgroup it would massively slow down training. So for speed purposes we will restrict sequence length to 100 words. You should try out some different sequence lengths and experiment with processing time and accuracy gains."""

print(pad_sequences([[1,2,3]], maxlen=5))
print(pad_sequences([[1,2,3,4,5,6]], maxlen=5))

max_length = 300 # Set the maximum length of the each data
data = pad_sequences(sequences, maxlen=max_length) # Padding each data

"""# Turning labels into One-Hot encodings
Labels can quickly be encoded into one-hot vectors with Keras:
"""

from keras.utils import to_categorical

labels = to_categorical(np.asarray(target))
print('Shape of data:', data.shape)
print('Shape of labels:', labels.shape)

print (target[0])
print (labels[0])

"""# Split dataset into training and testing data"""

train_size = int(len(data) * .8) # Set training data size
xtrain = data[:train_size]
ytrain = labels[:train_size]

xtest = data[train_size:]
ytest = labels[train_size:]

xtest_texts = texts[train_size:]

print(len(xtrain))
print(len(xtest))

"""# Create Model (MLP)"""

modelNN = Sequential()
modelNN.add(Input(shape=(max_length,)))
modelNN.add(Activation('relu'))
modelNN.add(Dense(128, activation='sigmoid'))
modelNN.add(Dense(64, activation='sigmoid'))
modelNN.add(Dense(20, activation='softmax'))
modelNN.summary()

modelNN.compile(optimizer='adam',
                        loss='categorical_crossentropy',
                        metrics=[categorical_accuracy])

histNN = modelNN.fit(xtrain,ytrain,validation_split=0.2,epochs=10)

"""# Create Model (Simple RNN)"""

modelRNN = Sequential()
modelRNN.add(Embedding(input_dim=vocab_size,
                       output_dim=64,
                       input_length=max_length,
                       trainable=False))
modelRNN.add(SimpleRNN(64))
modelRNN.add(Dense(20, activation='softmax'))
modelRNN.summary()

# https://stackoverflow.com/questions/42081257/keras-binary-crossentropy-vs-categorical-crossentropy-performance
modelRNN.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[categorical_accuracy])

histRNN = modelRNN.fit(xtrain, ytrain, validation_split=0.2, epochs=2)

"""# Create Model (LSTM)"""

from keras.layers import LSTM

modelLSTM = Sequential()

# https://stackoverflow.com/questions/42081257/keras-binary-crossentropy-vs-categorical-crossentropy-performance
modelLSTM.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[categorical_accuracy])

histLSTM = modelLSTM.fit(xtrain, ytrain, validation_split=0.2, epochs=2)

"""# Create Model (CNN)"""

modelCNN = Sequential()
modelCNN.add(Embedding(input_dim=vocab_size,
                       output_dim=64,
                       input_length=max_length,
                       trainable=False))
modelCNN.add(ConvID(64, 2, activation='relu'))
modelCNN.add(MaxPooling1D(2))
modelCNN.add(ConvID(64, 2, activation='relu'))
modelCNN.add(MaxPooling1D(2))
modelCNN.add(ConvID(64, 2, activation='relu'))
modelCNN.add(MaxPooling1D(2))

model CNN.add(Flatten())

modelCNN.add(Dense(64, activation='relu'))
modelCNN.add(Dense(20, activation='softmax'))
modelCNN.summary()

# https://stackoverflow.com/questions/42081257/keras-binary-crossentropy-vs-categorical-crossentropy-performance
modelCNN.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[categorical_accuracy])

histCNN = modelCNN.fit(xtrain, ytrain, validation_split=0.2, epochs=10)

"""Our model achieves 66% accuracy on the validation set. Systems like these can be used to assign emails in customer support centers, suggest responses, or classify other forms of text like invoices which need to be assigned to an department. Let's take a look at how our model classified one of the texts:"""

import matplotlib.pyplot as plt

def plot_graphs(history, string):
  plt.plot(history.history[string])
  plt.plot(history.history['val_'+string])
  plt.xlabel("Epochs")
  plt.ylabel(string)
  plt.legend([string, 'val_'+string])
  plt.show()
  
plot_graphs(histNN, "categorical_accuracy")
plot_graphs(histNN, "loss")

"""# Example Prediction"""

example = xtest[1000] # Get the tokens
print (xtest_texts[1000])

# Print tokens as text
for w in example:
    x = inv_index.get(w)
    print(x,end = ' ')

# Get prediction
pred = modelCNN.predict(example.reshape(1,100))

# Output predicted category
target_names[np.argmax(pred)]
