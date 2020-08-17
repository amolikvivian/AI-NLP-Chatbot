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
model.load('models/model.tflearn')


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
    print("Start talking with the bot (say 'end' to stop)!")
    
    r = sr.Recognizer()

    while True:

        
        with sr.Microphone() as source:

            try:        
                r.adjust_for_ambient_noise(source, duration=0.2)
                inputAudio = r.listen(source)

                inputText = r.recognize_google(inputAudio)
                inputText = inputText.lower()

                print('You:', inputText)
                
                if inputText.lower() == "end":
                    print('Bye!')
                    break

                results = model.predict([bag_of_words(inputText, words)])
                results_index = numpy.argmax(results)
                tag = labels[results_index]

                for tg in data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']

                print('Bot: ', random.choice(responses))

            except:
                print('Sorry, I could not understand what you said, please try again')
                print('[INFO] Speak again...')

chat()
