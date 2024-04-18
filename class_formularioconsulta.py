from app import app
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, validators

class FormularioConsulta(FlaskForm):
    textoConsulta=TextAreaField("Descreva o que deseja saber", [validators.DataRequired(), validators.Length(min=1)])
    consultar=SubmitField("Consultar")
    limpar=SubmitField("Limpar")
    html_resposta = StringField("")
    html_resposta.data=""

    
