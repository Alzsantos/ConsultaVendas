import pyodbc
import json
from decimal import Decimal

from config import buscar_string_conexao_banco_usuario_consulta

def executa_consulta_gpt_banco_sqlserver(comandoSQL):

    try:
    
        string_conexao = buscar_string_conexao_banco_usuario_consulta()            
    
        with pyodbc.connect(string_conexao) as conexao:
            cursor = conexao.cursor()           
    
            cursor.execute(comandoSQL)
            
            resultados = [dict(zip([coluna[0] for coluna in cursor.description], 
                       [str(valor) for valor in linha])) 
              for linha in cursor.fetchall()]
            
            cursor.close()

        json_resultados = json.dumps(resultados)
        
        return json_resultados

    except pyodbc.Error as e:
        
        print("Erro ao executar consulta SQL:", e)
        return None


