from flask import Flask, render_template, request
import requests
import smtplib
import dotenv
import ssl
from os import getenv
# USE YOUR OWN nPoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def get_all_posts():
    send_email()
    return render_template('index.html', all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        print('get')
        return render_template("contact.html", send=False)
    elif request.method == 'POST':
        print('post')
        return render_template('contact.html', send=True)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


def send_email():
    server = None
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP(getenv('SERVER'), int(getenv('PORT')))
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(getenv('EMAIL'), getenv('PASSWORD'))
        server.quit()
    except Exception as e:
        print(e)
        server.quit()


if __name__ == "__main__":
    dotenv.load_dotenv()
    app.run(debug=True, port=5001)
