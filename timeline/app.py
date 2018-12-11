import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'timeline.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'false'
db = SQLAlchemy(app)


class HistoricalEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.label}'


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        start_year = request.form['start_year']
        end_year = request.form['end_year']

        new_event = HistoricalEvent(name=name, description=description, start_year=start_year, end_year=end_year)
        db.session.add(new_event)
        db.session.commit()

    all_events = HistoricalEvent.query.all()

    return render_template('index.html', events=all_events)


if __name__ == "__main__":
    app.run(debug=True)
