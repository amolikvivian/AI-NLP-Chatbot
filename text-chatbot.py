import json
import nltk
import random
import pickle
import tflearn
import numpy as np 
import tensorflow as tf
from nltk.stem.lancaster import LancasterStemmer

#Initializing Lancaster Stemmer
stemmer = LancasterStemmer()

#Loading dataset
with open('dataset/dataset.json') as file:
	data = json.load(file)

with open('data.pickle', 'rb') as f:
    words, labels, train,  output = pickle.load(f)


#Building network
net = tflearn.input_data(shape = [None, len(train[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation = 'softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)

#Loading Model
model.load('models/chatbot-model.tflearn')


def bag_of_words(s, words):

	bag = [0 for _ in range(len(words))]

	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i, w in enumerate(words):
			if(w == se):
				bag[i] = 1

	return np.array(bag)


def chat():
	print('[INFO] Start talking...(type quit to exit)')
	while True:
		inp = input('You: ')

		#Type quit to exit
		if inp.lower() == 'quit':
			break

		#Predicting input sentence tag
		predict = model.predict([bag_of_words(inp, words)])
		predictions = np.argmax(predict)
		
		tag = labels[predictions]
		#Printing response
		for t in data['intents']:
			#print(t['tag'])
			if t['tag'] == tag:
				responses = t['responses']
				
		outputText = random.choice(responses)		
		print (outputText)

chat()
