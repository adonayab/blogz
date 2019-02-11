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
