import nltk
import numpy as np
from numpy.linalg import norm
from math import log
from numpy.linalg import norm

nltk.download('punkt')
nltk.download('gutenberg')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.corpus import gutenberg

docs = {}
for fileid in gutenberg.fileids():
  if fileid.startswith("shakespeare") or fileid.startswith("austen"): # Only get Shakespeare and Austen documents
    words = gutenberg.words(fileid)
    docs[fileid] = [word.lower() for word in words] # Associate the file name with the lowercased words from that file

sorted_doc_names = sorted(docs.keys()) # List of the document/file names in alphabetical order
print(sorted_doc_names)

hamlet_words = docs['shakespeare-hamlet.txt'] # Example: To access the words from Hamlet, use Hamlet file name
print(hamlet_words[:30]) # The associated value with that file name key is the list of words

#Extract vocab, convert to a sorted list, print length
vocab_set = set()
for doc_name in sorted_doc_names:
    for word in docs[doc_name]:
        vocab_set.add(word)
vocab_list = list(vocab_set)
vocab_list.sort()
print(len(vocab_list))

#term-document matrix for all corpuses. Takes a long time to run
i = len(vocab_list); j = len(sorted_doc_names)
freq_matrix = np.zeros((i, j))

for doc_count, doc_name in enumerate(sorted_doc_names):
    print(doc_name, "in progress")

    for vocab_count, vocab in enumerate(vocab_list):
        for word in docs[doc_name]:
            if word == vocab:
                freq_matrix[vocab_count][doc_count] += 1
    print(freq_matrix)


#another matrix based on the last. TF-IDF weighted values instea of raw freq
i = len(vocab_list); j = len(sorted_doc_names)
tf_idf_matrix = np.zeros((i, j))

for row_index, row in enumerate(freq_matrix):
    for column_index, element in enumerate(row):
        tf_idf_matrix[row_index][column_index] = (
            (log(element+1)) *
            (log((len(sorted_doc_names))/(element+1))))

print(tf_idf_matrix)

#Format into a useable list
def word_vector(word, matrix):
    return matrix[vocab_list.index(word)]

print(word_vector("the", freq_matrix))
print(word_vector("the", tf_idf_matrix))

#now we can check each spesific corpus against our vectors
def doc_vector(file_name, matrix):
    return matrix[:, sorted_doc_names.index(file_name)]

print(len(doc_vector("shakespeare-hamlet.txt", freq_matrix)), "\n", doc_vector("shakespeare-hamlet.txt", freq_matrix), "\n\n")
print(len(doc_vector("shakespeare-hamlet.txt", tf_idf_matrix)), "\n", doc_vector("shakespeare-hamlet.txt", tf_idf_matrix))


#looking for spesific words and the similarity between them
def sim(vector_1, vector_2):
    return np.dot(vector_1, vector_2)/np.linalg.norm(vector_1) * np.linalg.norm(vector_2)

print(sim(word_vector("king", freq_matrix), word_vector("queen", freq_matrix)))
print(sim(word_vector("king", freq_matrix), word_vector("apple", freq_matrix)))
print('\n')
print(sim(word_vector("king", tf_idf_matrix), word_vector("queen", tf_idf_matrix)))
print(sim(word_vector("king", tf_idf_matrix), word_vector("apple", tf_idf_matrix)))

#Compute the centroid for Jane Austen's works and the centroid for Shakespeare's works
#Compute and print the cosine similarity between the two centroids using your similarity function.
austen_k = 0; shake_k = 0; austen_centroid = 0; shake_centroid = 0
for name in sorted_doc_names:
    if "austen" in name:
        austen_k += len(tf_idf_matrix[:, sorted_doc_names.index(name)])
        austen_centroid += np.sum(tf_idf_matrix[:, sorted_doc_names.index(name)])

    elif "shakespeare" in name:
        shake_k += len(tf_idf_matrix[:, sorted_doc_names.index(name)])
        shake_centroid += np.sum(tf_idf_matrix[:, sorted_doc_names.index(name)])

austen_centroid /= austen_k
shake_centroid /= shake_k

print(" Jane Austen: ", austen_centroid, "\n\n", "Shakespeare: ", shake_centroid)
print("\n", "Similarity: ", sim(austen_centroid, shake_centroid))
