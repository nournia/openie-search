
from __future__ import unicode_literals, print_function
import os, gzip
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis.analyzers import StemmingAnalyzer
from hazm import word_tokenize, Lemmatizer
from progress.bar import Bar


resources = os.environ['OPENSHIFT_DATA_DIR']
index_dir = os.path.join(resources,'index')

lemmatizer = Lemmatizer()
def lemmatize(w): return lemmatizer.lemmatize(w)
analyzer = StemmingAnalyzer(stemfn=lemmatize)
schema = Schema(
	argument0=TEXT(stored=True, analyzer=analyzer),
	argument1=TEXT(stored=True, analyzer=analyzer),
	relation=TEXT(stored=True, analyzer=analyzer),
	sentence=STORED)


if __name__ == '__main__':
	bar = Bar('Progress (10k)')
	with gzip.open(os.path.join(resources,'informations.txt.gz'), 'r') as file:
		with create_in(index_dir, schema).writer() as writer:
			sentence = ''
			for i, line in enumerate(file):
				if i and not i % 10000: bar.next()
				line = line.strip().decode('utf8')
				if line.startswith('#'):
					sentence = line[2:]
				elif line:
					information = line.split(' - ')
					if len(information) == 3:
						writer.add_document(argument0=information[0], argument1=information[1], relation=information[2], sentence=sentence)
					# else: print('invalid:', line)
