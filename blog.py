from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

DATABASE = "blog.db"
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'

app = Flask(__name__)

app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	status_code = 200
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or \
		request.form['password'] != app.config['PASSWORD']:
			error = "Invalid credentials. Please try again"
			status_code = 401
		else:
			session['logged_in'] = True
			return redirect(url_for('main'))
	return render_template('login.html', error=error), status_code

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash("로그인부터 해야지!")
			return redirect(url_for('login'))
	return wrap

@app.route('/main')
@login_required
def main():
	g.db = connect_db()
	cur = g.db.execute('SELECT * FROM posts')
	posts = [ dict(title=row[0], post=row[1]) for row in cur.fetchall() ]
	return render_template('main.html', posts=posts)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)