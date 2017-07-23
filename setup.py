try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description' : 'This is the Columbus replacement: FUstercluCK!',
	'author' : 'Chad Curkendall',
	'url' : 'URL to get it at', 
	'download_url' : '''It's on the server in the Apps directory''',
	'author_email': 'BlueBuell@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['FUstercluCK'],
	'scripts': [],
	'name': 'fusterkluck'
}

setup(**config)