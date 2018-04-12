from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))

    def __init__(self, title, body):
        self.title = title
        self.body = body

  

@app.route("/blog", methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all()
    return render_template("blog.html", blogs=blogs)
    



@app.route("/newpost", methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':

        blog_title = request.form['title']
        blog_body = request.form['body']

        title_error = ""
        body_error = ""
        
        if not blog_title:
            title_error = "Please fill out the title"
        if not blog_body:
            body_error = "Please fill out the body"
        if not title_error or not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog")
        else:
            return render_template("/new_post.html", title_error=title_error, body_error=body_error, blog_title=blog_title, blog_body=blog_body)

    return render_template("/new_post.html")
            
        

    



if __name__ == '__main__':    
    app.run()