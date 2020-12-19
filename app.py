from flask import Flask, render_template, request, url_for, session, flash
from database import db
from forms import Usuario_form
from models import Usuario
from flask_cors import CORS

from flask_migrate import Migrate
from werkzeug.utils import redirect
app=Flask(__name__)
CORS(app)
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
    if 'username' in session:#Si el usaurio ya hizo dentro de la session in dentro
        return f'Ya hecho login {session("username")}'
    # listado de personas
    usuario = Usuario.query.all()  # obtnemos toda la informacion dentro de esta tabla
    # personas.Persona.query.order_by(id)ordenamos con este metodo de pendiendo el como ordenamos dentro del corchetes
    total_usuario = Usuario.query.count()  # Obtenemos la cantidad total de registros dentro de la tabla
    app.logger.debug(f'Listado de personas{usuario}')
    app.logger.debug(f'Total de personas{total_usuario}')
    return render_template('base.html',usario=usuario,total_usuario=total_usuario)
@app.route('/Registro',methods=['GET','POST'])
def Registrar():
    usuario = Usuario()  # Creamos una nueva clae de modelos  tipo perosna
    persona_form = Usuario_form(obj=usuario)  # form es de formulario y debemos instaciar la clase de tipo models socializar
    if request.method == 'POST':  # preguntamos si el tipo de metodo es de tipo post importamos del objeto flask.request
        if persona_form.validate_on_submit():  # preguntamos si el formulario si es valido solo si se hace elenvio del formulario
            persona_form.populate_obj(usuario)  # llenamos el objetos que persona que definimos de clase models
            app.logger.debug(f'Persona a insertar {usuario}')
            # insertamos el nuevo registro
            db.session.add(usuario)  # mandamos a llamar el metodo db de base de datos y abrimos una session y lo add para añadir ala base dedatos
            db.session.commit()  # guardamos la informacion en la base de datos
            return redirect(url_for('Iniciar_Sesion'))  # lo derijimos ala pagina una pagina especifica
    return render_template('index2.html', forma=persona_form)
@app.route('/Iniciar_Sesion',methods=['GET','POST'])
def Iniciar_Sesion():
    if request.method == 'POST':  # decimos si es metodo es post

        if Usuario.query.filter_by(correo=request.form['login_correo']).first() and Usuario.query.filter_by(contrasenia=request.form['login_password']).first():

          app.logger.info(f'entrando ala consola {request.path}')
          return redirect(url_for('Bienvenido'))# volvemos al inicio
        flash('Entro al incio')
    return render_template('index2.html')
@app.route('/Menu_principal')
def Menu():
    return render_template('menu.html')
@app.route('/Listado')
def Listado():
    usuarios=Usuario.query.all()
    #usuarios = Usuario.query.get_or_404(id)  # por si hay un error
    app.logger.debug(f' ver persona:{usuarios}')
    return render_template('listado.html', usuarios=usuarios)
@app.route('/bienvenido')
def Bienvenido():
    return render_template('Bienvenido.html')
if __name__==('__main__'):
    app.run(debug=True)