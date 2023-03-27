import nltk, random
import numpy as np
from math import log
from nltk.classify import SklearnClassifier
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression

nltk.download('vader_lexicon')
nltk.download('movie_reviews')
nltk.download('punkt')

from nltk.sentiment import vader
from nltk.corpus import movie_reviews

raw_docs = []                                     # Our custom dataset list
for label in movie_reviews.categories():          # Categories are 'neg' and 'pos'
  files = movie_reviews.fileids(label)            # Get list of file names associated with label
  for file in files:
    words_from_file = movie_reviews.words(file)   # Get words in file (one movie review)
    words_with_label = (words_from_file, label)   # Place raw words with label in a tuple
    raw_docs.append(words_with_label)             # Add tuple to our docs list

random.shuffle(raw_docs)                          # Randomize document positions

lexicon = vader.SentimentIntensityAnalyzer().make_lex_dict() # Get lexicon dictionary

"""
f_log_doc_length(doc): returns the logarithm of the length of the document
The log() function is already imported for you above from the math package.
f_contains_exclamation(doc): returns 1 if the string "!" appears in doc, 0 otherwise
f_positive_sentiment_sum(doc): returns the sum of the sentiment scores of the positive words in doc based on the scores in lexicon
f_negative_sentiment_sum(doc): returns the sum of the sentiment scores of the negative words in doc based on the scores in lexicon
extract_features(doc): returns a dictionary with 4 key-value pairs, one for each feature as described
"""

def f_log_doc_length(doc):
    return log(len(doc))

def f_contains_exclamation(doc):
    for t in doc:
        if t == "!":
            return 1
    return 0

def f_positive_sentiment_sum(doc):
    sum = 0
    for t in doc:
        if t in lexicon and lexicon[t] > 0:
            sum += lexicon[t]
    return (sum)

def f_negative_sentiment_sum(doc):
    sum = 0
    for t in doc:
         if t in lexicon and lexicon[t] < 0:
            sum += lexicon[t]
    return (sum)

def extract_features(doc):
    out = {'log_doc_length': f_log_doc_length(doc),
              'contains_exclamation': f_contains_exclamation(doc),
              'positive_word_sentiment_sum': f_positive_sentiment_sum(doc),
              'negative_word_sum': f_negative_sentiment_sum(doc)}
    return out

for i, doc in enumerate (raw_docs):
    print(extract_features(doc[0]), '\n')

    if i >= 2:
        break

#new list with return of extract_features and label
dataset = []
for doc in raw_docs:
    dataset.append((extract_features(doc[0]), doc[1]))

train_set = dataset[:int(len(dataset)/10*9)]
test_set = dataset[int(len(dataset)/10*9):]

print(len(test_set), len(train_set))
print(test_set[:3], '\n\n', train_set[:3])

"""
pseudocode:
repeat until X iterations have occurred:
  for each document in documents:
    classify the document using weight vector
    update weight vector if necessary
"""

w = np.array([0.0,0.0,0.0,0.0])
i = 0

while i < 30:
    #print("w, k, feature, predicted, doc[1]")

    i += 1
    for doc in train_set:
        fx = np.array(list(doc[0].values()))

        #classify the document using weight vector
        predicted = ''

        #I have no idea if this is correct but im rolling with it
        if np.dot(w,fx) >= 0: predicted = 'pos'
        elif np.dot(w,fx) < 0: predicted = 'neg'

        #update weight vector if necessary
        if predicted != doc[1]:
            if doc[1] == 'pos': w += fx
            elif doc[1] == 'neg': w -= fx
        #print(w, k, feature, predicted, doc[1])

    print(w, end = '\n')

#train and test the classifier we made
correct = 0
for doc in test_set:
        fx = np.array(list(doc[0].values()))

        #classify the document using weight vector
        predicted = ''

        if np.dot(w,fx) >= 0: predicted = 'pos'
        elif np.dot(w,fx) < 0: predicted = 'neg'

        #check if prediction was correct
        if predicted == doc[1]:
            correct += 1

print("Binary Perception Accuracy: %", round(correct / (len(test_set))*100, 2), sep='')

#Logistic Regression
log_reg = SklearnClassifier(LogisticRegression())
correct = 0
log_reg.train(train_set)
for doc in test_set:
    if log_reg.classify(doc[0]) == doc[1]:
        correct += 1

print("\n\nLogistic Regression Accuracy: %", round((correct / len(test_set))*100, 2), sep='')
