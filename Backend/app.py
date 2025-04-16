from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
import json
import random
import numpy as np
import pickle
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load trained model & data
lemmatizer = WordNetLemmatizer()
model = load_model("chatbot_model.h5")

with open("chatbot_data.pkl", "rb") as f:
    words, classes = pickle.load(f)

with open("intents.json", encoding='utf-8') as file:
    intents = json.load(file)

# Preprocessing functions
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    return [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [1 if w in sentence_words else 0 for w in words]
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    return classes[np.argmax(res)]

def chatbot_response(msg):
    tag = predict_class(msg)
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "Sorry, I don't understand."

# Chat API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    response = chatbot_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

