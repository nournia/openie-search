
from __future__ import unicode_literals
import json
from flask import Flask, request, abort
from hazm import Normalizer
from search import find_informations


application = Flask(__name__)
application.config['PROPAGATE_EXCEPTIONS'] = True
normalizer = Normalizer()



@application.route('/search', methods=['POST'])
def search():
	if 'argument0' not in request.form or 'argument1' not in request.form or 'relation' not in request.form:
		abort(400)

	query = map(normalizer.normalize, (request.form['argument0'], request.form['argument1'], request.form['relation']))
	return json.dumps(find_informations(*query), ensure_ascii=False)


@application.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'origin, x-requested-with, content-type')
	response.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
	return response


@application.route('/')
def main():
	return 'Baaz Search Server!'


if __name__ == '__main__':
	application.run(debug=True)
