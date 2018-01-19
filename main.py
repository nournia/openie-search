
from __future__ import unicode_literals
import json
from flask import Flask, request, abort
from hazm import Normalizer
from search import find_informations


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

normalizer = Normalizer()


@app.route('/search', methods=['POST'])
def search():
	if 'argument0' not in request.form or 'argument1' not in request.form or 'relation' not in request.form:
		abort(400)

	query = map(normalizer.normalize, (request.form['argument0'], request.form['argument1'], request.form['relation']))
	return json.dumps(find_informations(*query), ensure_ascii=False)


@app.route('/')
def main():
	return 'Baaz Search Server!'


if __name__ == '__main__':
	app.run(debug=True)
