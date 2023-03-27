import nltk, json, gensim.downloader, warnings, math
import numpy as np
import tensorflow as tf
from numpy.linalg import norm
from math import log
from collections import defaultdict
from nltk.tokenize import regexp_tokenize
from nltk.tokenize import word_tokenize
from nltk.sentiment.util import split_train_test
from nltk.corpus import words
from nltk.metrics.distance import edit_distance
from nltk.classify import SklearnClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn.exceptions import ConvergenceWarning
from statistics import mean, stdev

glove = gensim.downloader.load('glove-twitter-25')

nltk.download('punkt')
nltk.download('words')

#Autocorrect
print(len(words.words('en')))
print(len(words.words('en-basic'))) # Use this one to keep runtimes short

corups = "en-basic"
user_input = input("Type a word: ")
correct = False
for word in words.words(corups):
    if user_input == word:
        print("Word is in vocabulary")
        correct = True

min_edit_word_distance = 1000
min_edit_word = ""
if correct == False:
    for word in words.words(corups):
        if min_edit_word_distance > edit_distance(user_input, word):
            min_edit_word_distance = edit_distance(user_input, word)
            min_edit_word = word
    print("Did you mean ", min_edit_word, "?", sep="")

#Data Preparation
data = []
with open("clothing.json", "r") as f:
  for line in f.readlines():
    item = json.loads(line)
    data.append(item)

data[:5]

small_count = 0; fit_count = 0; large_count = 0; rating_count = [0,0,0,0,0]
for review in data:

    if review['fit'] == 'small':
        small_count += 1
    elif review['fit'] == 'fit':
        fit_count += 1
    else:
        large_count += 1

    rating_count[review['rating']-1] += 1

print("small_count:", small_count, "\nfit_count:", fit_count,
     "\nlarge_count:", large_count, end="\n\n")

for i, rating in enumerate(rating_count):
    print ("# of", i+1, "star ratings:", rating)

review_list = []
for review in data:
    review_list.append(tuple((review['review'],review['fit'])))

print(review_list[:5])

#Feature Extraction and Regexes
"""
pseudocode:
f_comparison_word_count(doc): returns the count of comparison words too, more, runs, than, little, and all words that end with er (i.e. contain at least one letter followed by er)
You should use regexp_tokenize to match all words in the text with your regex pattern in order to get the count of relevant words.

f_measurement_count(doc): returns the count of measurement-related tokens that include digits, specifically the following:
Height measurements of the form x'y for digits x and y. For example, 5'6" would be matched as the token 5'6 (some reviewers leave off the inches marker, so we can ignore it).
Cup sizes which are 2 digits followed by at least one alphanumeric value, e.g. 34DD or 32B.
Overall outfit sizes that are standalone numerical values of at least one digit. For example, size 3 fits me would match 3.

f_word_count(doc): returns the number of words in the review text.
"""
def f_comparison_word_count(doc):
    regex = r"too|more|runs|than|little|.er"
    return(len(regexp_tokenize(doc, pattern=regex)))

def f_measurement_count(doc):
    regex = r"\d'\d|\d\d+|\d+"
    return(len(regexp_tokenize(doc, pattern=regex)))

def f_word_count(doc):
    regex = r"\b\w+"
    return(len(regexp_tokenize(doc, pattern=regex)))

#counts the number of times "comfort, comfortable, comforting" appears.
#useful for determining comfort
def f_comfort_count(doc):
    regex = r"comfort+"
    return(len(regexp_tokenize(doc, pattern=regex)))

def extract_features(doc):
    return({'f_comparison_word_count': f_comparison_word_count(doc),
               'f_measurement_count':  f_measurement_count(doc),
               'f_word_count': f_word_count(doc),
               'f_comfort_count': f_comfort_count(doc)})

"""
the first element is the normalized feature dictionary based on extract_features and the distribution of each feature's values
the second element is the label for the document
"""
scaled_dict = []
features_scaled = {}
for j, review in enumerate(review_list):
    normalized_values = np.empty(4)
    features = extract_features(review[0])
    feature_values = np.array(list(features.values()))
    #print(j, feature_values)

    #Have to check that all the feature values are non 0 in order to not get NaN on Inf as result
    if feature_values.all() != 0:
        normalized_values += ((feature_values - mean(feature_values)) / stdev(feature_values))
        #print(normalized_values)

        for i, value in enumerate(normalized_values):
            features_scaled[list(features)[i]] = value

        #print(features_scaled)
        scaled_dict.append(((features_scaled, review[1])))
        features_scaled = {}

        if math.isnan (float(value)) == True:
            print(row, value)

print(scaled_dict[:10])

#Cross-Validation
def get_folds(docs, k=5):
    np_docs = np.array(docs)
    return [x.tolist() for x in np.array_split(np_docs,k)]

print(get_folds(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']))

def cross_validation(classifier, docs, k=5):
    correct = 0
    accuracy = []
    doc_list = get_folds(docs,k)
    classify_fold = k-1

    while(classify_fold >= 0):
        for i, doc_fold in enumerate(doc_list):
            if i != classify_fold:
                 classifier.train(doc_fold)
            else:
                for doc in doc_fold:
                    if classifier.classify(doc[0]) == doc[1]:
                        correct += 1
                    classify_fold -= 1
                accuracy.append((correct / len(doc_fold))*100)
    print('\n', str(classifier), " Accuracy: %", round((sum(accuracy)/len(accuracy)), 2), sep='')

warnings.filterwarnings(action='ignore', category=ConvergenceWarning)

perceptron = SklearnClassifier(Perceptron())
log_reg = SklearnClassifier(LogisticRegression())

cross_validation(perceptron, scaled_dict)
cross_validation(log_reg, scaled_dict)

#Word Vectors and Neural Networks
"""
Here we are looking through the data, using GloVE vectors to represent each review as a vector of 25
Then, we evaluate a basic neural network using those vectors, tensorflow
"""

x = []
y = []
for review in review_list:
    vectors = []
    parse_review = False

    for word in review[0].split():
        if word in glove:
            parse_review = True
            #print(np.array(glove[word]))
            #print(np.array(glove[word]))
            vectors.append(np.array(glove[word]))

        else:#cant parse reviews that dont have a vector list in glove
            break
    if parse_review == True:
        vectors = np.array(vectors)
        #print(np.mean(vectors, axis=0))
        x.append(np.mean(vectors, axis=0))

        if review[1] == "small":
            y.append(0)
        elif review[1] == "fit":
            y.append(1)
        else:
            y.append(2)

x = np.array(x)
y = np.array(y)

x_train, x_test = split_train_test(x)
y_train, y_test = split_train_test(y)
print(len(x_train), len(y_train))
print(x_train[:5], x_test[:5], y_train[:5], y_test[:5])

model = tf.keras.models.Sequential([
  tf.keras.layers.Input(shape=(25,)),
  tf.keras.layers.Dense(50, activation='relu'),
  tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
loss, accuracy = model.evaluate(x_test, y_test)
print("Accuracy:", accuracy)
