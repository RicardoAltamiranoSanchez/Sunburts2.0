from flask import Flask, render_template, request, url_for,session
from database import db
from forms import Usuario_form
from models import Usuario

from flask_migrate import Migrate
from werkzeug.utils import redirect
app=Flask(__name__)
#Configuracion para la base de datos
USER_DB='postgres'
PASS_DB='admin'
URL_DB='localhost'
NAME_DB='Tienda3B'
FULL_URL_DB=f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'#CADENA DE CONEXION COMPLETA
app.config['SQLALCHEMY_DATABASE_URI']=FULL_URL_DB#cual es laconexion de la bd que va utilizar
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)
migrate=Migrate()
migrate.init_app(app,db)
#Configuracion de flak-wtf osa el form
app.config['SECRET_KEY']='llave_maestra'
@app.route('/')
def Inicio():
    # listado de personas
    usuario = Usuario.query.all()  # obtnemos toda la informacion dentro de esta tabla
    # personas.Persona.query.order_by(id)ordenamos con este metodo de pendiendo el como ordenamos dentro del corchetes
    total_usuario = Usuario.query.count()  # Obtenemos la cantidad total de registros dentro de la tabla
    app.logger.debug(f'Listado de personas{usuario}')
    app.logger.debug(f'Total de personas{total_usuario}')
    return render_template('index.html',usario=usuario,total_usuario=total_usuario)
@app.route('/Registro',methods=['GET','POST'])
def Registrar():
    usuario=Usuario()
    usuario_formulario=Usuario_form(obj=usuario)
    if request.method =='POST':
        if usuario_formulario.validate_on_submit():  # preguntamos si el formulario si es valido solo si se hace elenvio del formulario
            usuario_formulario.populate_obj(usuario)  # llenamos el objetos que persona que definimos de clase models
            app.logger.debug(f'Persona a insertar {usuario}')
            # insertamos el nuevo registro
            db.session.add(usuario)  # mandamos a llamar el metodo db de base de datos y abrimos una session y lo add para añadir ala base dedatos
            db.session.commit()  # guardamos la informacion en la base de datos
            return redirect(url_for('Inicio'))  # lo derijimos ala pagina una pagina especifica
    return render_template('registro.html',formulario=usuario_formulario)

@app.route('/Iniciar_Sesion',methods=['GET','POST'])
def Iniciar_Sesion():
    usuario=Usuario.query.all()
    if request.method == 'POST':  # decimos si es metodo es post
        login_usuario = request.form['login_usuario']  # obtenemos la informacion del form registrada con corchetes de array
        login_password=request.form['login_password']

        if session['username']==login_usuario and session['username']==login_password:
          return redirect(url_for('Menu'))  # volvemos al inicio
    return render_template('login.html')
@app.route('/Menu_principal')
def Menu():
    return render_template('menu.html')
