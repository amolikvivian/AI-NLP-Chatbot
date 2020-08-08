# AI-NLP-Chatbot
An NLP based Chatbot over a simple fully connected neural network architecture using Tensorflow. Trained over a custom dataset specified in the JSON file.

## Prerequisites
Run `pip install -r requirements.txt` in your terminal to install all required libraries

## Dataset
The `dataset.json` contains the intents on which the model is trained. Each pattern (sentence) and response is given a particular tag. The model classifies each input sentence under
and gives out a random answer corresponding to that tag. The json file can be formatted according to the user's requirements.
