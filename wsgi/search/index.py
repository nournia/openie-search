
from __future__ import unicode_literals, print_function
import os, gzip
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis.filters import Filter
from whoosh.analysis.tokenizers import RegexTokenizer
from hazm import word_tokenize, Lemmatizer


class LemmaFilter(Filter):
	def __init__(self):
		self.lemmatizer = Lemmatizer()

	def __call__(self, tokens):
		for token in tokens:
			token.text = self.lemmatizer.lemmatize(token.text)
			yield token


resources = os.environ['OPENSHIFT_DATA_DIR']
index_dir = os.path.join(resources,'index')
analyzer = RegexTokenizer() | LemmaFilter()
schema = Schema(
	argument0=TEXT(stored=True, analyzer=analyzer),
	argument1=TEXT(stored=True, analyzer=analyzer),
	relation=TEXT(stored=True, analyzer=analyzer),
	sentence=STORED)


if __name__ == '__main__':
	with gzip.open(os.path.join(resources,'informations.txt.gz'), 'r') as file:
		with create_in(index_dir, schema).writer() as writer:
			sentence = ''
			for line in file:
				line = line.strip().decode('utf8')
				if line.startswith('#'):
					sentence = line[2:]
				elif line:
					information = line.split(' - ')
					if len(information) == 3:
						writer.add_document(argument0=information[0], argument1=information[1], relation=information[2], sentence=sentence)
					# else: print('invalid:', line)
