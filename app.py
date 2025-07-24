from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


class Usuarios(db.Model):
    email = db.Column(db.String(50), nullable=False, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    lingua = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(15), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    advogado_email = db.Column(db.String(50), db.ForeignKey('advogados.email'), nullable=True)
    advogado = db.relationship('Advogados', backref='usuarios')
    ong_id = db.Column(db.Integer, db.ForeignKey('ong.id'), nullable=True)
    ong = db.relationship('Ongs', backref='usuarios')    
      
class Advogados(db.model):
    email = db.Column(db.String(50), nullable=False, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    
class Ongs(db.model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    
class Empresas(db.model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    salario = db.Column(db.Float(4.2), nullable=False)
    especificacoes = db.Column(db.String(120), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    contato = db.Column(db.String(20), nullable=False)

class Advogados_Ongs(db.Model):
    advogado_email = db.Column(db.String(50), db.ForeignKey('advogados.email'), nullable=False)
    advogado = db.relationship('Advogados', backref='ongs')
    ong_id = db.Column(db.Integer, db.ForeignKey('ong.id'), nullable=False)
    ong = db.relationship('Ongs', backref='advogados')
    
class Empresas_Usuarios(db.Model):
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    usuario_email = db.Column(db.String(50), db.ForeignKey('usuario.email'), nullable=False)
    usuario = db.relationship('Usuarios', backref='empresas')
    empresa = db.relationship('Empresas', backref='usuarios')
        
@app.route('/index', methods=['GET'])
def index():
    return render_template('.html')

@app.route('/cadastro/usuario', methods=['GET', 'POST'])
def cadastroUsuario():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        lingua = request.form['lingua']
        senha = request.form['senha']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        db.session.add(Usuarios(email=email, nome=nome, lingua=lingua, senha=senha, telefone=telefone, endereco=endereco))
        db.session.commit()
        return redirect('/')
    return render_template('.html')

@app.route('/cadastro/advogado', methods=['GET', 'POST'])
def cadastroAdvogado():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        telefone = request.form['telefone']
        db.session.add(Advogados(email=email, nome=nome, telefone=telefone))
        db.session.commit()
        return redirect('/')
    return render_template('.html')

@app.route('/cadastro/ong', methods=['GET', 'POST'])
def cadastroOng():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        db.session.add(Ongs(nome=nome, endereco=endereco))
        db.session.commit()
        return redirect('/')
    return render_template('.html')

@app.route('/cadastro/empresa', methods=['GET', 'POST'])
def cadastroEmpresa():
    if request.method == 'POST':
        nome = request.form['nome']
        salario = float(request.form['salario'])
        especificacoes = request.form['especificacoes']
        endereco = request.form['endereco']
        contato = request.form['contato']
        db.session.add(Empresas(nome=nome, salario=salario, especificacoes=especificacoes, endereco=endereco, contato=contato))
        db.session.commit()
        return redirect('/')
    return render_template('.html')

@app.route('/lista/usuarios', methods=['GET'])
def listaUsuarios():
    usuarios = Usuarios.query.all()
    return render_template('.html', usuarios=usuarios)

@app.route('/lista/advogados', methods=['GET'])
def listaAdvogados():
    advogados = Advogados.query.all()
    return render_template('.html', advogados=advogados)

@app.route('/lista/ongs', methods=['GET'])
def listaOngs():
    ongs = Ongs.query.all()
    return render_template('.html', ongs=ongs)

@app.route('/lista/empresas', methods=['GET'])
def listaEmpresas():
    empresas = Empresas.query.all()
    return render_template('.html', empresas=empresas)



if __name__ == '__main__':
    app.run(debug=True)