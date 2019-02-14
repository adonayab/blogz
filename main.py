from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'uahfkahdlfhuhkn8392uh'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password


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

    # TODO : implement user signup

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        
        if password != verify:
            flash("Passwords do not match")
            return redirect('/signup')

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()
            session['user'] = user.email
            return redirect("/")
        else:
            flash('Email adress "{}" already an account'.format(existing_user.email))
            return render_template('signup.html')
    
    return render_template('signup.html')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == '' or body == '':
            flash("The title or body can not be empty.")
            return redirect('/newpost')

        titles = Blog.query.filter_by(title=title).first()
        if not titles:
            new_blog = Blog(title=title, body=body, owner=owner)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id={}'.format(new_blog.id))
        else:
            flash("A blog with the same title exists. Please choose a different title.")
            return redirect('/newpost')

    return render_template('newpost.html')


@app.route('/', methods=['POST', 'GET'])
@app.route('/blog')
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
