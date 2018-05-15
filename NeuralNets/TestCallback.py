# This callback evaluate on the test set and write the predictions to a file. 

import os
import numpy as np
import datetime

import keras
from keras.callbacks import Callback

class TestCallback(keras.callbacks.Callback):
	def __init__(self, x_test, y_test, id_to_label, batch_size):
		self.x_test = x_test
		self.y_test = y_test
		self.id_to_label = id_to_label
		self.batch_size = batch_size


	def on_epoch_end(self, epoch, logs={}):

		predictions = self.model.predict(self.x_test, batch_size=self.batch_size)
		# parse predictions
		self.__parse_predictions(predictions)

	# Write predictions to file
	def __parse_predictions(self, predictions):
		y_hat = []
		for i, prediction in enumerate(predictions):
			y_hat.append(np.argmax(prediction))

		predictions = y_hat
		
		open("output/predictions_all.txt", 'w').close()
		for i in range(len(predictions)):
			with open("output/predictions_all.txt", "a") as f:
					pred_label = self.id_to_label[predictions[i]]
					true_label = self.id_to_label[np.where(self.y_test[i] == 1)[0][0]]
					f.write(str(i+1) + " " + true_label + " " + pred_label + "\n")