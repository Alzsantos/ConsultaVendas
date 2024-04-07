from flask import render_template, request, flash, url_for
from consultavenda import app
from class_formularioconsulta import FormularioConsulta
from class_openai import ChatGPT
from sql_server import executa_consulta_gpt_banco_sqlserver
import pyodbc


@app.route('/')
def index():    
    with app.app_context():    
        formulario=FormularioConsulta(request.form)
        return render_template('consultavendas.html', form=formulario)
@app.route('/consultar', methods=['POST'])
def consultar():
    with app.app_context():  
        
                
        formulario=FormularioConsulta(request.form)
        
        chatgpt=ChatGPT()
        
        erroSQL=""
                    
        for contador in range(1, 3):    
                
            resultado_obtencao_query = chatgpt.obter_instrucao_select(formulario.textoConsulta.data, erroSQL)
            
            if resultado_obtencao_query:
            
                try:            
                    resultado_json = executa_consulta_gpt_banco_sqlserver(chatgpt.instrucao_sql)
                    html= chatgpt.obter_html_resposta_consulta_banco(resultado_json)
                    
                    if html != "":                            
                        formulario.html_resposta.data=html
                    else:
                        formulario.html_resposta.data=""
                    return render_template('consultavendas.html', form=formulario)
                    
                except pyodbc.ProgrammingError as erro:
                   
                    erroSQL=erro.args[1]
                    
        
        formulario.html_resposta.data="Infelizmente não foi possível obter a resposta. Por favor, tente mais tarde."
        return render_template('consultavendas.html', form=formulario)             
                 
                

    
    

