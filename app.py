from flask import Flask, render_template

app = Flask(__name__)


class Quote:
    def __init__(self, text, author):
        self.text = text
        self.author = author


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', quotes=[
        Quote("As the Chinese say, 1001 words is worth more than a picture.", "John McCarthy"),
        Quote("Use a picture. It's worth a thousand words.", "Arthur Brisbane")])


if __name__ == "__main__":
    app.run(debug=True)
