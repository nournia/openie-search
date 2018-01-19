
from __future__ import unicode_literals
import os, json
from flask import Flask, request, abort
from hazm import Normalizer
from search import find_informations


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

normalizer  = Normalizer()


@app.route('/search', methods = ['POST'])
def search():
	if not 'argument0' in request.form or not 'argument1' in request.form or not 'relation' in request.form:
		abort(400)

	query = map(normalizer.normalize, (request.form['argument0'], request.form['argument1'], request.form['relation']))
	return json.dumps(find_informations(*query), ensure_ascii=False)


@app.route('/')
def main():
	return 'Baaz Search Server!'


if __name__ == '__main__':
	app.run(debug=True)
