from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'uahfkahdlfhuhkn8392uh'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog_listing', methods=['POST', 'GET'])
def blog_listing():
    return render_template('blog_listing.html')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == '' or body == '':
            flash("The title or body can not be empty.")
            return redirect('/newpost')

        titles = Blog.query.filter_by(title=title).first()
        if not titles:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog')
        else:
            flash("A blog with the same title exists. Please choose a different title.")
            return redirect('/newpost')

    return render_template('newpost.html')


@app.route('/', methods=['POST', 'GET'])
@app.route('/blog')
def blog():
    # return "<h1>TEST!</h1>"
    return render_template('blog.html', title="Blog")


if __name__ == "__main__":
    app.run()
