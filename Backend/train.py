import nltk
import json
import random
import numpy as np
import pickle
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents
with open('intents.json', encoding='utf-8') as file:
    intents = json.load(file)

# Preprocessing
words, classes, documents = [], [], []
ignore_chars = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = sorted(set([lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_chars]))
classes = sorted(set(classes))

# Save words & classes to pickle
with open("chatbot_data.pkl", "wb") as f:
    pickle.dump((words, classes), f)

# Create training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = [lemmatizer.lemmatize(w.lower()) for w in doc[0]]
    
    for w in words:
        bag.append(1 if w in pattern_words else 0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
X_train, y_train = np.array([i[0] for i in training]), np.array([i[1] for i in training])

# Build Neural Network Model
model = Sequential([
    Dense(128, input_shape=(len(X_train[0]),), activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dense(len(y_train[0]), activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer=SGD(learning_rate=0.01, momentum=0.9), metrics=['accuracy'])
model.fit(X_train, y_train, epochs=200, batch_size=5, verbose=1)

# Save model
model.save("chatbot_model.h5")
print("✅ Training completed! Model saved as 'chatbot_model.h5'.")
print("✅ Vocabulary saved as 'chatbot_data.pkl'.")
