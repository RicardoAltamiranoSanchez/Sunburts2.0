from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Usuario_form(FlaskForm):#clase para el form
    nombre=StringField('Nombre',validators=[DataRequired()])#Aqui ya es codigo html
    apellido=StringField('Apellido')
    correo=StringField('Email',validators=[DataRequired()])
    usuario=StringField('Usuario')
    contrasenia=StringField('Contraseña',validators=[DataRequired()])
    Enviar=SubmitField('Registrarse')#este es para el boton