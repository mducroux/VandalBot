# This callback takes care of keeping track of the epochs and perform early stopping if necessary
import os
import keras
from keras.callbacks import Callback
import numpy as np

class EarlyStoppingByPatience(Callback):
	def __init__(self, x_test, y_test, patience, id_to_label, batch_size):
		super(Callback, self).__init__()
		self.x_test = x_test
		self.y_test = y_test
		self.id_to_label = id_to_label
		self.batch_size = batch_size
		self.patience = patience
		
		self.max_fscore = 0

		self.max_epoch_id = 0
		self.patience_counter = 0
		self.epochs = []
		self.epoch_counter = 1

	def on_epoch_end(self, epoch, logs={}):

		# Compute accuracy
		def acc(self,predictions):

			numLabels = 0
			numCorrLabels = 0

			for i in range(len(predictions)):
				pred_label = self.id_to_label[predictions[i]]
				true_label = self.id_to_label[np.where(self.y_test[i] == 1)[0][0]]
				numLabels += 1
				if pred_label == true_label:
					numCorrLabels += 1

			current_acc = numCorrLabels/float(numLabels)

			self.epochs.append({'Acc': float(current_acc)})

			if current_acc <= self.max_acc:
				self.patience_counter = self.patience_counter + 1
				if self.patience_counter >= self.patience:
					self.model.stop_training = True
			else:
				self.max_acc = current_acc

				self.max_epoch_id = self.epoch_counter
				self.patience_counter = 0

				# Uncomment to write model to file
				#print("Saving model...")
				#self.model.save("models/" + str(current_acc) +'.h5')  # creates a HDF5 file 'my_model.h5'

			self.epoch_counter += 1

		# Compute F-score for task C
		def f_score(self, predictions):

			tp = 0
			fn = 0
			fp = 0

			for i in range(len(predictions)):
				pred_label = self.id_to_label[predictions[i]]
				true_label = self.id_to_label[np.where(self.y_test[i] == 1)[0][0]]
				
				if true_label == 0:
					if pred_label == 0:
						tp += 1
					if pred_label == 1:
						fn += 1

				elif true_label == 1:
					if pred_label == 0:
						fp += 1

			if tp != 0:
				precision = float(tp) / (tp + fp)
				recall = float(tp) / (tp + fn)
			else:
				precision = 0
				recall = 0

			current_fscore = float(2 * precision * recall) / (precision + recall)

			print("\nTest F-score: ", current_fscore, "\n")

			self.epochs.append({'fscore': float(current_fscore)})

			if current_fscore <= self.max_fscore:
				self.patience_counter = self.patience_counter + 1
				if self.patience_counter >= self.patience:
					self.model.stop_training = True
			else:
				self.max_fscore = current_fscore

				self.max_epoch_id = self.epoch_counter
				self.patience_counter = 0

				#write model file
				#print("Saving model...")
				#self.model.save("models/" + str(current_fscore) +'.h5')  # creates a HDF5 file 'my_model.h5'

			self.epoch_counter += 1

		# Predict on validation set 		
		predictions = self.model.predict(self.x_test, batch_size=self.batch_size)

		# Select class with maximum probability
		y_hat = []
		for i, prediction in enumerate(predictions):
			y_hat.append(np.argmax(prediction))

		predictions = y_hat
		f_score(self, predictions)#Replace by: "acc(predictions)" for precision