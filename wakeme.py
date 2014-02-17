#!/usr/bin/env python

from functions import *


app = Flask(__name__)
app.secret_key = os.environ['sk']


@app.route('/alarm/create/')
def create():
	create_call(request.values.get('From'),*request.values.get('Body').split('|'))


if __name__ == '__main__':
	if os.environ.get('PORT'):
		app.run(host='0.0.0.0',port=int(os.environ.get('PORT')),debug=os.getenv('dev','False') == 'True')
	else:
		app.run(host='0.0.0.0',port=5000,debug=os.getenv('dev','False') == 'True')
