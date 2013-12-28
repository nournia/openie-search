
from __future__ import unicode_literals, print_function
from index import index_dir, schema
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from hazm import word_tokenize

searcher = open_dir(index_dir, schema=schema).searcher()
parser = QueryParser('', schema)
qtokens = lambda field, phrase: [field+ word for word in word_tokenize(phrase) if word]


def find_informations(argument0, argument1, relation):
	parts = qtokens('argument0:', argument0) + qtokens('argument1:', argument1) + qtokens('relation:', relation)
	query = parser.parse(' '.join(parts))
	results = searcher.search(query, limit=100)
	return {'results': map(dict, results), 'hits': len(results)}
