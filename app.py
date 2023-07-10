from flask import Flask, render_template, request
import requests
import smtplib
import dotenv
import ssl
# USE YOUR OWN nPoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def get_all_posts():
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
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp_server", 11)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.login("sender_email", "password")
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    dotenv.load_dotenv()
