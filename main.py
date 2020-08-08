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
with open('dataset/dataset.json') as f:
	data = json.load(f)

try:
	with open('data.pickle', 'rb') as f:
		words, labels, train,  output = pickle.load()

except:

	words = []
	x_docs = [] #Patterns - Sentences
	y_docs = [] #Tags for patterns
	labels = []

	#Looping over all data in json file as dictionaries
	for intent in data['intents']:

		#Looping over the patterns - input sentences
		for pattern in intent['patterns']:
			
			#Tokenizing each word in each pattern sentences
			tokenizedWords = nltk.word_tokenize(pattern)

			#Extending words list with lists of tokens
			words.extend(tokenizedWords)

			#Appending docs lists with sentence and respective tag
			x_docs.append(tokenizedWords)
			y_docs.append(intent['tag'])

			#Appending labels list with tags
			if(intent['tag'] not in labels):
				labels.append(intent['tag'])

	#Sorting labels
	labels = sorted(labels)

	#Stemming words and sorting - Stemming refers to findin the root of every word
	words = [stemmer.stem(w.lower()) for w in words if w not in '?']
	words = sorted(list(set(words)))

	train = []
	output = []

	#Creating a Bag of Words - One Hot Encoding
	out_empty = [0 for _ in range(len(labels))]
	for x, doc in enumerate(x_docs):
		bag = []
		stemmedWords = [stemmer.stem(w) for w in doc]

		#Marking word index as 1
		for w in words:
			if w in stemmedWords:
				bag.append(1)
			else:
				bag.append(0)

		outputRow = out_empty[:]
		outputRow[labels.index(y_docs[x])] = 1

		train.append(bag)
		output.append(outputRow)

	#Converting data into numpy array
	train = np.array(train)
	output = np.array(output)

	#Saving data
	with open('data.pickle', 'wb') as f:
		pickle.dump((words, labels, train, output), f)

#Building network
net = tflearn.input_data(shape = [None, len(train[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation = 'softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
	model.load('models/chatbot.model')
except:
	#Training model
	model.fit(train, output, n_epoch = 1000, batch_size = 8, show_metric = True)
	#Saving model
	model.save('models/chatbot.model')


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
		inp = input('You:')

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
				
		print(random.choice(responses))

chat()