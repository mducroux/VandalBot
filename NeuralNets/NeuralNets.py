# -*- coding: utf-8 -*-
import os
#from parameters import parameters

import numpy as np
from keras.models import Model
from keras.layers.core import Flatten
from keras.layers import GRU, Bidirectional, LSTM, GlobalAveragePooling1D, GlobalMaxPooling1D
from keras.layers import Input, Embedding, Dense, Dropout, Permute, Activation, Lambda
from keras.layers import Conv1D, MaxPooling1D, concatenate, TimeDistributed, Multiply, RepeatVector, Add, Average
from keras import regularizers
from keras.optimizers import *
from keras import backend as K
from TestCallback import TestCallback
from sklearn.model_selection import StratifiedKFold
from sklearn.utils import shuffle

import keras.backend as K
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from EarlyStoppingByPatience import EarlyStoppingByPatience # Chosse between F-score (arg. Task C) and accuracy for the rest
from keras.utils import plot_model 


class NeuralNets(object):
	def __init__(self, filters, kernel_sizes, num_of_units, dropout, patience, embedding_matrix=None, max_seq_length=None, max_num_words=None, word_embeddings_path=None, embedding_size=None, batch_size=None, epochs=None, labels_to_ids=None, bidirectional=True):
		self.embedding_matrix = embedding_matrix
		self.max_seq_length = max_seq_length
		self.max_num_words = max_num_words
		self.word_embeddings_path = word_embeddings_path
		self.embedding_size = embedding_size
		self.batch_size = batch_size
		self.epochs = epochs
		self.filters = filters
		self.kernel_sizes = kernel_sizes
		self.num_of_units = num_of_units
		self.dropout = dropout
		self.patience = patience
		self.bidirectional = bidirectional
		self.labels_to_ids = labels_to_ids
		self.id_to_label = {value: key for key, value in self.labels_to_ids.items()}
		self.num_of_classes = len(labels_to_ids)
		print(self.id_to_label)

	def train_model(self, x, y):

		# Suffle data
		x, y = shuffle(x, y)

		model = None
		model = self.gru()

		early_stopping = EarlyStoppingByPatience(x, y, self.patience, self.id_to_label, self.batch_size)
		model.fit(x, y, batch_size=self.batch_size, epochs=self.epochs, verbose=1, shuffle=True, callbacks=[early_stopping], validation_data=(x, y))
		return early_stopping.max_fscore

		'''

		# Create K-fold
		n_folds = 10
		skf = StratifiedKFold(n_splits=n_folds, shuffle=True)
		i = 0

		# Label for split
		lab = np.asarray([np.argmax(x) for x in y])

		fscore = []

		for train, test in skf.split(x, lab):
			i+=1
			print("\nRunning Fold", str(i), "/", str(n_folds))

			# Initialize and chosse model
			model = None
			model = self.gru()

			x_train = np.asarray(x).take(train, axis=0)
			y_train = np.asarray(y).take(train, axis=0)

			x_test = np.asarray(x).take(test, axis=0)
			y_test = np.asarray(y).take(test, axis=0)

			early_stopping = EarlyStoppingByPatience(x_test, y_test, self.patience, self.id_to_label, self.batch_size)
			testing = TestCallback(x_test, y_test, self.id_to_label, self.batch_size)

			model.fit(x_train, y_train, batch_size=self.batch_size, epochs=self.epochs, verbose=1, shuffle=True, callbacks=[early_stopping], validation_data=(x_test, y_test))

			fscore.append(early_stopping.max_fscore)

		# If fscore change to: "fscore = early_stopping.max_fscore"
		fscore = np.asarray(fscore).mean()

		print("Average fscore", fscore)

		return fscore
	'''

	# CNN
	def cnn(self):

		main_input = Input(shape=(self.max_seq_length, ), dtype='int32', name='main_input')
		embeddings = Embedding(self.max_num_words, self.embedding_size, input_length=self.max_seq_length, weights=[self.embedding_matrix], trainable=False)(main_input)

		print("Building CNN model with single kernel size...")

		kernel_size = self.kernel_sizes[0]
		conv1d = Conv1D(self.filters, kernel_size, padding='valid', activation='relu')(embeddings)
		max_pool = GlobalMaxPooling1D()(conv1d)

		dropout_layer = Dropout(self.dropout)(max_pool)
		predictions = Dense(self.num_of_classes, activation='softmax')(dropout_layer)


		print("Training CNN model...")

		model = Model(inputs=main_input, outputs=predictions)
		model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

		model.summary(line_length=200)

		return model

	# GRU
	def gru(self):

		main_input = Input(shape=(self.max_seq_length, ), dtype='int32', name='main_input')
		embeddings = Embedding(self.max_num_words, self.embedding_size, input_length=self.max_seq_length, weights=[self.embedding_matrix], trainable=False)(main_input)

		if self.bidirectional:
			print("Building B-GRU model...")
			gru_out = Bidirectional(GRU(self.num_of_units, return_sequences=False, dropout=self.dropout, recurrent_dropout=self.dropout))(embeddings)

		else:
			print("Building GRU model...")
			gru_out = GRU(self.num_of_units, return_sequences=False, dropout=self.dropout, recurrent_dropout=self.dropout)(embeddings)


		predictions = Dense(self.num_of_classes, activation='softmax')(gru_out)

		print("Training GRU model...")

		model = Model(inputs=main_input, outputs=predictions)
		model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

		model.summary(line_length=200)

		return model