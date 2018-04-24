import sys
from Dataset import *
from NeuralNets import NeuralNets
from parameters import parameters


def write_output(directory, network, dataset, max_seq_length, max_num_words, acc, parameters):

	with open(directory + 'table_' + network + "_" + data_set + '.csv', 'a') as csv_file:
		writer = csv.writer(csv_file, delimiter =",",quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['network_type', 'max_seq_length', 'max_num_words', 'embedding_size', 'word_embeddings_path', 'batch_size', 'max_epochs', 'kernel_sizes', 'filters', 'num_of_units', 'dropout', 'data_set', 'patience', 'max_acc'])
		writer.writerow([network, max_seq_length, max_num_words, parameters['embedding_size'], parameters["word_embeddings_path"], parameters["batch_size"], parameters["epochs"], parameters["kernel_sizes"],
		parameters["filters"], parameters["num_of_units"], parameters["dropout"], dataset, parameters["patience"], acc])


# Parameters
data_set = parameters["dataset"]
max_seq_length = 60
max_num_words = 1000000 # We don't limit the number of tokens
embedding_size = parameters["embedding_size"]
word_embeddings_path = parameters["word_embeddings_path"]
batch_size = parameters["batch_size"]
epochs = parameters["epochs"]
kernel_sizes = parameters["kernel_sizes"]
filters = parameters["filters"]
num_of_units = parameters["num_of_units"]
dropout = parameters["dropout"]
patience = parameters["patience"]
network = parameters["network_type"]

# Path to train and test set
train = '../data/dbpedia/lemmatize/train.txt'
test = '../data/dbpedia/lemmatize/test.txt'

directory = "output/"
if not os.path.exists(directory):
	os.makedirs(directory)

# Create the dataset and load the data
dataset = Dataset(train, test, word_embeddings_path, max_num_words, max_seq_length, embedding_size)

# Prepare the data for the model
x_train, y_train, x_test, y_test, embedding_matrix, vocab_size, labels_to_ids = dataset.prepare_data()


# The vocab size may be different if the initial max_num_words is greater than the dataset vocabulary
max_num_words = vocab_size

#Initialize the parameters of the network
nn = NeuralNets(filters, kernel_sizes, num_of_units, dropout, patience, embedding_matrix, max_seq_length, max_num_words, word_embeddings_path, embedding_size, batch_size, epochs, labels_to_ids)

# Train the network and return scores (F-score or accuracy)
acc = nn.train_model(x_train, y_train, x_test, y_test)

# Write results to file
write_output(directory, network, data_set, max_seq_length, max_num_words, acc, parameters)




