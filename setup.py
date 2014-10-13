from setuptools import setup

setup(name='baaz-search',
	version='0.2',
	description='Baaz Search App',
	author='Alireza Nourian',
	author_email='az.nourian@gmail.com',
	url='http://www.sobhe.ir/baaz/',
	install_requires=[
		'Flask==0.10.1',
		'Jinja2==2.7.1',
		'Werkzeug==0.9.4',
		'gunicorn==19.1.0',
		'Whoosh==2.5.6',
		'hazm==0.3',
		'progress==1.2'
	],
)
