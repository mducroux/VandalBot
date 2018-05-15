# -*- coding: utf-8 -*-

# This script convert the data to the right format for the neuralnetworks

import os
import sys, csv
import pickle
import numpy as np
import pandas as pd
from keras.utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import StratifiedKFold, KFold
import fastText


class Object(object):
	pass


class Dataset(object):
	def __init__(self, train_set, word_embeddings_path=None, vocab_size=None, max_seq_length=None, embedding_size=None):
		#Load FastText words embedding from .txt file when initializing the dataset
		self.train_set = train_set
		self.word_embeddings_path = word_embeddings_path
		self.vocab_size = vocab_size
		self.max_seq_length = max_seq_length
		self.embedding_size = embedding_size
		self.labels_to_ids = {}

		assert self.word_embeddings_path is not None, "Provide word embeddings path"

		print('Loading FastText word embeddings...')

		self.embeddings_index = fastText.FastText.load_model('../wiki.fr.bin') # Replace wiki.en.bin by wiki.es.bin for spanish

		#Load data from the file path given by the "dataset" argument
		self.x, self.y = self.__load_data(train_set)

	def __load_data(self, train_name, separator="\t"): # or separator = , ?
		#Initialization of lists containing the text and the labels

		data = data = pd.read_csv("../input.txt", sep="\t", header=None)
		data.columns = ["text", "label"]
		x = [str(x) for x in data["text"].values]
		y = data["label"].values

		return x, y

	def __prepare_embedding_matrix(self, id_to_word):
		print('Preparing embedding matrix...')
		num_words = min(self.vocab_size, len(id_to_word)+1)

		# Initialize embedding matrix
		embedding_matrix = np.zeros((num_words, self.embedding_size))
		for key, value in id_to_word.items():
			word = value

			# Take word only in vocabulary size sorted by occurences
			if key >= self.vocab_size:
				continue

			# Take word embedding of token
			embedding_vector = self.embeddings_index.get_word_vector(word)
			embedding_matrix[key] = embedding_vector

		return embedding_matrix

	def prepare_data(self, sep="\t"):
		train_texts = self.x
		y_train = self.y

		#Convert labels to integer
		train_labels = []
		for label in y_train:
			if label not in self.labels_to_ids.keys():
				self.labels_to_ids[label] = len(self.labels_to_ids)
			label = self.labels_to_ids[label]
			train_labels.append(label)

		print('Found %s datapoints for training data.' % len(train_texts))

		print("Tokenizing and indexing data...")

		# Fit tokenizer on text
		tokenizer = Tokenizer(filters="", num_words=self.vocab_size, lower=True)
		tokenizer.fit_on_texts(train_texts)

		word_to_id = tokenizer.word_index
		id_to_word = {value: key for key, value in word_to_id.items()}

		print('Found %s unique tokens.' % len(word_to_id))

		# Convert text to word ids
		train_texts_to_id = tokenizer.texts_to_sequences(train_texts)

		# Pad texts to the same length
		x = pad_sequences(train_texts_to_id, maxlen=self.max_seq_length, padding='post', truncating='post')

		# Convert label to categorical values
		y = to_categorical(np.asarray(train_labels))

		embedding_matrix = self.__prepare_embedding_matrix(id_to_word)

		return x, y, embedding_matrix, len(embedding_matrix), self.labels_to_ids
