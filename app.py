import os

from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80))
#     email = db.Column(db.String(120), unique=True)
#
#     def __init__(self, name, email):
#         self.name = name
#         self.email = email
#         self.nothing = 10
#
#     def __repr__(self):
#         return '<Name %r>' % self.name


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/interactive/')
def interactive():
	return render_template('interactive.html')

@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res

@app.route('/background_process')
def background_process():
	try:
		lang = request.args.get('proglang', 0, type=str)
		if lang.lower() == 'python':
			return jsonify(result='You are wise')
		else:
			return jsonify(result='Try again.')
	except Exception as e:
		return str(e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)