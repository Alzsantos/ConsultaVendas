from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

SECRET_KEY = 'exemploconsultavendaschatgpt'

KEY_VAULT = "chavedev"
NOME_SEGREDO_API = "ChatGPT-API-Key"
NOME_ORGANIZATION_ID="ChatGPT-API-Organization-ID"
NOME_STRING_CONEXAO_BANCO_CONSULTA='String-Conexao-BancoSQL-Consulta'


def buscar_chave_api():
    
    return buscar_segredo(NOME_SEGREDO_API)     


def buscar_organization_id():
    
    return buscar_segredo(NOME_ORGANIZATION_ID)    


def buscar_string_conexao_banco_usuario_consulta():
    
    return buscar_segredo(NOME_STRING_CONEXAO_BANCO_CONSULTA)
    
    

def buscar_segredo(nome_segredo):
    
    credencial = DefaultAzureCredential()

    secret_client = SecretClient(vault_url=f"https://{KEY_VAULT}.vault.azure.net/", credential=credencial)

    valor_segredo = secret_client.get_secret(nome_segredo)

    return valor_segredo.value


