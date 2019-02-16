from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import User, Blog
from app import app, db
import re


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'email' not in session and '/static/' not in request.path:
        return redirect('/login')


@app.route("/logout", methods=['POST'])
def logout():
    del session['email']
    return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        elif user and user.password != password:
            flash('Incorrect password')
        elif email == '' and password == '':
            flash('Email and Password can not be empty')
        else:
            flash('User does not exist')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        existing_user = User.query.filter_by(email=email).first()

        if email == '' and password == '' and verify == '':
            flash('Email and Password fields can not be empty')
            return render_template('signup.html')

        if existing_user:
            flash('{} Already an account'.format(email))
            return render_template('signup.html')
        if email == '':
            flash('Email field required')
            return render_template('signup.html')
        if not existing_user and password == '':
            flash('Password field required')
            return render_template('signup.html')
        if not existing_user and (len(password) < 3 or len(password) > 20) and password != verify:
            flash('Invalid Password')
            flash('Passwords do not match')
            return render_template('signup.html')
        if not existing_user and password != verify:
            flash('Passwords do not match')
            return render_template('signup.html')

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['email'] = email

        return redirect('/')

    return render_template('signup.html')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(email=session['email']).first()

        if title == '' or body == '':
            flash("The title or body can not be empty.")
            return redirect('/newpost')

        titles = Blog.query.filter_by(title=title).first()
        if not titles:
            new_blog = Blog(title, body, owner)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id={}'.format(new_blog.id))
        else:
            flash("A blog with the same title exists. Please choose a different title.")
            return redirect('/newpost')

    return render_template('newpost.html')

@app.route('/', methods=['POST', 'GET'])
def index():
  blogs = Blog.query.all()
  return render_template('index.html', blogs=blogs)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    blog = Blog.query.filter_by(id=blog_id).first()
    if not blog_id:
        blogs = Blog.query.all()
        return render_template('blog.html', title="Blog", blogs=blogs, blog_title='Build a Blog')
    else:
        return render_template('blog.html', title="Blog", blog_title=blog.title, body=blog.body)


if __name__ == "__main__":
    app.run()
