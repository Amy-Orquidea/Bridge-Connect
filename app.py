from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class usuario(db.Model):
    cpf = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    senha = db.Column(db.String(15), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    
class nacionalidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    ddd = db.Column(db.String(3), nullable=False)
    



    
        
    
@app.route('/')
def index():
    return redirect('index.html')

if __name__ == '__main__':
    app.run(debug=True)