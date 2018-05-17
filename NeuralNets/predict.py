import pickle
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import fastText
from keras.models import load_model

def pred(text):

	texts = []
	texts.append(text)

	embeddings_index = fastText.FastText.load_model('../wiki.fr.bin')

	with open('tokenizer.pickle', 'rb') as handle:
	    tokenizer = pickle.load(handle)

	word_to_id = tokenizer.word_index
	id_to_word = {value: key for key, value in word_to_id.items()}

	texts_to_id = tokenizer.texts_to_sequences(texts)

	x = pad_sequences(texts_to_id, maxlen=250, padding='post', truncating='post')

	embedding_matrix = np.zeros((len(id_to_word) + 1, 300))
	for key, value in id_to_word.items():
		word = value

		# Take word embedding of token
		embedding_vector = embeddings_index.get_word_vector(word)
		embedding_matrix[key] = embedding_vector

	model = load_model("models/0.9684210526315788.h5")

	prediction = model.predict(x, batch_size=256)

	return [np.argmax(pred) for pred in prediction][0]

print(pred("<br/> Datafications biographiques en cours de création Nom et Prénom Pseudo Biographie Albà Jacas Arnau Arnau Auguste Piccard Alemán Ignacio Sukarno Nacho Wolfgang Pauli Asin Ghislain Esteban Robin Ghislain Michael Schumacher Bacuet Quentin QuentinB Charles de Gaulle Badoux Christophe Dylan Christophe Donald Trump Barman Raphaël Raphael.barman Gustave Ador Baud Matthieu Sébastien Michel Titi Henry Dunant Ben Hallam Mohamed Houssam Houssm Sigmund Freud Bickel Marc Marcus Henri Dès Bossy Thierry Thierry Arthur Honegger Bouchiba Sonia Amina Sonia Daniel Brélaz Boyer Thomas Paul Jean Tboyer Franz Beckenbauer Burkhard Julien Yuuki JulienB Roman Polanski Caforio Andrea Felice Qantik Benito Mussolini Cavaleri Alexandre Guy Burgerpop Guillaume Henri Dufour Charrière Jonathan O ' showa Mao Zedong Cinéus Jennifer Marthe JenniCin Walter Mittelholzer Dewaele Alexis Claude André Vlaedr Robert Oppenheimer Fahli Marouane Fournier Romain Romain Fournier Richard Wagner Giorla Matteo MatteoGiorla Magic Johnson Gomez Vivolo Antoine Antonias Banderos Philippe Suchard Hirt Grégoire Hirtg Alain Morisod Jolles Marc André Olivier Mj2905 Hergé Jourdan Alex Alexj Gioachino Rossini Kieliger Leandro Leandro Kieliger Thomas Edison Lang Robin Alex roblan11 Jean Tinguely Launay Antoine Zacharie AntoineL Ernesto Rafael Guevara Leao Loureiro Claudio Claudioloureiro Bill Gates Leblanc Martin Charles Martin Jacques-Yves Cousteau Lee Pierre-Alexandre Wen Hao Loïs PA Nicolas Bouvier Li Ziyan Icebaker Le Corbusier Mayrhofer Grégoire Adrien Gregoire3245 Nicéphore Niépce Monbaron Aurélien Ken Amonbaro Phil Collins Morel Sébastien Musluoglu Cem Ates Musluoglucem Winston Churchill Naas Nawel Nawel Élisabeth II Pannatier Arnaud Arnaudpannatier Bobby Fischer Perrard Karine Kperrard Lénine Phan Hoang Kim Lan Kl Paul Klee Roth Christine Béatrice Wanda Paul Maillefer Sekarski Samuel Joseph-Jean Nameless Albert Einstein Selim Stephan Sameh Saad JiggyQ Franklin D . Roosevelt Snoeijs Jan Herman Ann Snus Joseph Staline Ukachi Chibueze Verdier Aurélien Thomas Mathieu Aureliver Claude Nicollier Viaccoz Cédric Cedricviaccoz Adolf Hitler Wagner Patrik Alexander Mireille Fidel Castro Wicht Bruno Brunowicht Steffi Graf <br/> Henri Dès par Marcus , Marc Bickel Claude Nicollier par Aureliver , Aurélien Verdier Daniel Brélaz par Sonia Bouchiba Roger Federer par Sébastien Morel Robert Oppenheimer par Alexis Dewaele , Vlaedr Sigmund Freud par Houssm , Houssam Ben Hallam Donald Trump par christophe / Christophe Badoux Lénine par Kperrard , Karine Perrard Benito Mussolini par Andrea Caforio Jean Tinguely par roblan11 / Robin Lang Bobby Fischer par Arnaud Pannatier Paul Klee par kl / Kim Lan Phan Hoang Jacques-Yves Cousteau par Martin Leblanc Auguste Piccard par Arnau / Arnau Albà Hergé par Marc Jollès Luigi Luzzatti par Fabrice Guibert Nicéphore Niépce par Gregoire3245 , Gregoire Mayrhofer Nicolas Bouvier par Pierre-Alexandre Lee Roman Polanski par Julien Burkhard Arthur Honegger par Thierry Bossy Mao Zedong par O ' showa ( Jonathan Charrière ) Philippe Suchard par Antonias Banderos Thomas Edison par Leandro Kieliger Walter Mittelholzer par Jennifer Cinéus ( JenniCin ) Magic Johnson par Matteo Giorla Richard Wagner par Romain Fournier Le Corbusier par Ziyan Li Wolfgang Pauli par  Nacho  , Ignacio Aleman Charles de Gaulle par QuentinB , Quentin Bacuet Joseph Staline par Snus , Jan Snoeijs Winston Churchill par Musluoglucem , Musluoglu Cem Ates Bill Gates par Claudioloureiro , Claudio Loureiro Paul Maillefer par Christine Roth Steffi Graf par Brunowicht , Bruno Wicht Franklin D . Roosevelt par JiggyQ , Stephane Selim Wikipedia https : //fr.wikipedia.org/wiki/Biographie."))