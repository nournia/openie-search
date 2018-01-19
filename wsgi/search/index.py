
from __future__ import unicode_literals, print_function
import os, gzip, codecs, shelve
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis.analyzers import StemmingAnalyzer
from hazm import word_tokenize, Lemmatizer
from progress.bar import Bar


resources = os.environ['OPENSHIFT_DATA_DIR']
index_dir = os.path.join(resources,'index')

lemmatizer = Lemmatizer()
def lemmatize(w): return lemmatizer.lemmatize(w.replace('_', ' '))
analyzer = StemmingAnalyzer(stemfn=lemmatize)
schema = Schema(
	argument0=TEXT(stored=True, analyzer=analyzer),
	argument1=TEXT(stored=True, analyzer=analyzer),
	relation=TEXT(stored=True, analyzer=analyzer),
	sentence=STORED)


def get_informations():
	bar = Bar('Progress (100k)')
	with gzip.open(os.path.join(resources,'informations.txt.gz'), 'r') as file:
		sentence, informations = '', []
		for i, line in enumerate(file):
			if i and not i % 100000: bar.next()
			line = line.strip().decode('utf8')
			if line.startswith('#'):
				if informations:
					yield sentence, informations
					informations = []
				sentence = line[2:]
			elif line:
				information = line.split(' - ')
				if len(information) == 3:
					informations.append(information)
				# else: print('invalid:', line)


def get_frequents():
	filename = os.path.join(resources,'frequents.txt')
	if os.path.isfile(filename):
		frequents = set(codecs.open(filename, encoding='utf8').read().split('\n'))

		filename = os.path.join(resources,'exceptions.txt')
		if os.path.isfile(filename):
			for item in set(codecs.open(filename, encoding='utf8').read().split('\n')):
				frequents.remove(item)

		return frequents
	else:
		counts = shelve.open(filename +'.counts')
		for _, informations in get_informations():
			for item in set(sum(informations, [])):
				if len(item) < 50:
					if item in counts:
						counts[item] += 1
					else:
						counts[item] = 1

		frequents = [(word, count) for word, count in counts.items() if count > 1]
		print(len(frequents), 'frequents')

		frequents = [word for word, count in sorted(frequents, key=lambda item: item[1], reverse=True)]
		print(*frequents, sep='\n', file=codecs.open(filename, 'w', 'utf8'))
		return set(frequents)


if __name__ == '__main__':
	frequents = get_frequents()
	with create_in(index_dir, schema).writer() as writer:
		for sentence, informations in get_informations():
			for information in informations:
				if information[0] in frequents and information[1] in frequents and information[2] in frequents:
					writer.add_document(argument0=information[0], argument1=information[1], relation=information[2], sentence=sentence)
