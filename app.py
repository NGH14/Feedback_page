from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_feedbackmail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pgfflqdcwytbbf:41f60f4cff3c71b5b2bf52f7d6684e641a7362729c43ca015789a5474aeb505d@ec2-52-205-3-3.compute-1.amazonaws.com:5432/d56bca18fa913v'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///pgfflqdcwytbbf:41f60f4cff3c71b5b2bf52f7d6684e641a7362729c43ca015789a5474aeb505d@ec2-52-205-3-3.compute-1.amazonaws.com:5432/d56bca18fa913v'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    service = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, service, rating, comments):
        self.customer = customer
        self.service = service
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        service = request.form['service']
        rating = request.form['rating']
        comments = request.form['comments']    
        
        # Return if not fill.
        if customer == '' or service == '':
            return render_template('feedback.html', message='Please enter yourname and the sevice field')
        if db.session.query(Feedback).filter(Feedback.customer == customer & Feedback.service == service).count() == 0:
            data = Feedback(customer, service, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, service, rating, comments)
            return render_template('success.html')
        return render_template('feedback.html', message= 'You have already submitted feedback ') 

if __name__ == '__main__':
    app.run()
    