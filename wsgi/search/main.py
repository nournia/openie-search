
from __future__ import unicode_literals
import os, json
from flask import Flask, request, abort
from hazm import sent_tokenize, word_tokenize, Normalizer, Lemmatizer, POSTagger, DependencyParser
from search import find_informations


resources = os.environ['OPENSHIFT_DATA_DIR']

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

normalizer  = Normalizer()
lemmatizer = Lemmatizer()
tagger = POSTagger(path_to_model=os.path.join(resources, 'persian.tagger'), path_to_jar=os.path.join(resources, 'stanford-postagger.jar'))
parser = DependencyParser(lemmatizer=lemmatizer, tagger=tagger, working_dir=resources)


@app.route('/')
def main():
	return 'Baaz Search Server!'


@app.route('/search', methods = ['POST'])
def search():
	if not 'argument0' in request.form or not 'argument1' in request.form or not 'relation' in request.form:
		abort(400)

	query = map(normalizer.normalize, (request.form['argument0'], request.form['argument1'], request.form['relation']))
	return json.dumps(find_informations(*query), ensure_ascii=False)


# hazm api

@app.route('/hazm/normalize', methods = ['POST'])
def normalize():
	if not 'text' in request.form:
		abort(400)

	return normalizer.normalize(request.form['text'])


@app.route('/hazm/tokenize', methods = ['POST'])
def tokenize():
	if not 'normalized_text' in request.form:
		abort(400)

	return json.dumps(map(word_tokenize, sent_tokenize(request.form['normalized_text'])), ensure_ascii=False)


@app.route('/hazm/tag', methods = ['POST'])
def tag():
	if not 'tokenized_text' in request.form:
		abort(400)
	tokenized_text = json.loads(request.form['tokenized_text'])

	return json.dumps(tagger.tag_sents(tokenized_text), ensure_ascii=False)


@app.route('/hazm/lemmatize', methods = ['POST'])
def lemmatize():
	if not 'tagged_text' in request.form:
		abort(400)
	tagged_text = json.loads(request.form['tagged_text'])

	return json.dumps([[lemmatizer.lemmatize(word, tag) for word, tag in sentence] for sentence in tagged_text], ensure_ascii=False)


@app.route('/hazm/parse', methods = ['POST'])
def parse():
	if not 'tagged_text' in request.form:
		abort(400)
	tagged_text = json.loads(request.form['tagged_text'])

	return json.dumps([dependency_graph.to_conll(10) for dependency_graph in parser.tagged_parse_sents(tagged_text)], ensure_ascii=False)


if __name__ == '__main__':
	app.run(debug=True)
