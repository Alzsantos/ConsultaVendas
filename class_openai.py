import openai
import json
from config import buscar_chave_api, buscar_organization_id

from sql_server import executa_consulta_gpt_banco_sqlserver

class ChatGPT:
    
    def __init__(self):
        
        openai.api_key = buscar_chave_api()
        openai.organization=buscar_organization_id()
        
        self.executou_busca_instrucao=False
        self.erro_busca_instrucao=False
        self.confirmacao_instrucao=False
        
        self.lista_mensagens=[]
        
        self.contexto = """Context: O modelo de dados do sistema que você de desenvolve é em SQL Server. As tabelas existentes são:        
        Tabela tb_cliente: Esta tabela contém o cadastro de clientes. Os seus campos são:
        - id_cliente: Chave primária da tabela, contém o id que identifica o cliente.
        - nome_cliente: Armazena o nome do cliente.
        - tipo_cliente: contém o tipo do cliente. Pode ser F para pessoa física ou J para pessoa jurídica.
        
        Tabela tb_departamento: Contém os departamentos da empresa. Os seus campos são:
        - id_departamento: Chave primária da tabela, contém o id que identifica o departamento.
        - nome_departamento: Contém o nome do departamento da empresa.
        
        Tabela tb_produto: Armazena os produtos comercializados pela empresa. Os campos são:
        - id_produto: Chave primária da tabela, este campo é o identificador do produto.
        - descricao: Armazena o nome/descrição do produto.
        - preco_sugerido: É o preço unitário sugerido para a venda do produto.
        - id_departamento: Este campo se relaciona com o campo id_departamento da tabela tb_departamento. Ele identifica o departamento da empresa responsável pela comercialização do produto.
        
        Tabela tb_venda: Armazena as vendas realizadas pela empresa. Cada venda é um ticket. Uma venda deve ser feita para um cliente. Uma venda pode ter vários detalhes_venda. Mas um detalhe_venda só pode pertencer à uma venda. O valor total do ticket (venda) é a soma da quantidade existente em cada produto do detalhe da venda multiplicado pela quantidade existente em cada detalhe da venda. Seus campos são:
        - id_venda: Chave primária da tabela, este campo identifica a venda.
        - data_venda: Data da realização da venda.
        - id_cliente: Chave estrangeira, este campo se relaciona com o campo id_cliente da tabela tb_cliente e identifica o cliente para o qual foi feita a venda.
        
        Tabela tb_detalhe_venda: Contém a lista dos produtos que fazem parte da venda realizada pela empresa e que está registrada na tabela tb_venda. Uma venda pode ter vários detalhes mas cada detalhe só pode pertencer a uma venda. Cada detalhe também só pode ser de um produto. O valor do detalhe é obtido multiplicando a quantidade do produto pelo preço indivudual de venda. A soma de todos os valores de detalhe de uma venda resulta no valor total da venda. Seus campos são:
        - id_detalhe_venda: Chave primária da tabela, identifica o registro contendo o detalhe da venda.
        - id_venda: Chave estrangeira, este campo se relaciona com o campo id_venda da tabela tb_venda e indica de qual venda este registro faz parte.
        - id_produto: Chave estrangeira, este campo se relaciona com o campo id_produto da tabela tb_produto e indica qual o produto que foi vendido.
        - quantidade_produto: Indica a quantidade do produto que foi vendido nesta venda.
        - preco_unitario_venda: Indica o preço unitário que o produto efetivamente foi vendido."""
               
    
    def obter_chatgpt_instrucao_select(self, pergunta, erro):   
        
        self.executou_busca_instrucao=False
        
        if erro=="":
        
            self.lista_mensagens.append({"role": "user", "content": "Role: Você é um desenvolvedor de sistemas."})        
            self.lista_mensagens.append({"role": "user", "content": self.contexto})
            self.lista_mensagens.append({"role": "user", "content": "Você precisa criar uma instrução de Select para extrair os dados que responde a pergunta: "})        
            self.lista_mensagens.append({"role": "user", "content": pergunta})        
            self.lista_mensagens.append({"role": "user", "content": "Esta instrução de Select será executada no banco de dados para extrair as informações."})    
            self.lista_mensagens.append({"role": "user", "content": "Traduza códigos para os seus significados em português. Por exemplo, dia da semana retorne Domingo e não retorne o número 1"})    
        else:
            self.lista_mensagens.append({"role": "user", "content": "A insrução gerada foi executada no banco e gerou este erro: " + erro})    
            
        self.lista_mensagens.append({"role": "user", "content": "Retorne um json com os seguintes atributos: conseguiu_montar_instrucao_sql (true or false), instrucao_sql e motivo_nao_ter_montado"})
        
        try:
            
            self.resposta = openai.chat.completions.create(messages=self.lista_mensagens, model="gpt-3.5-turbo")
            resultado = json.loads(self.resposta.choices[0].message.content)            
            self.lista_mensagens.append({"role": "assistant", "content": self.resposta.choices[0].message.content})
            self.executou_busca_instrucao=bool(resultado["conseguiu_montar_instrucao_sql"])
            self.instrucao_sql=resultado["instrucao_sql"] 
            self.erro_busca_instrucao=False
            
        except:
            self.erro_busca_instrucao=True
        
    def confirmar_chatgpt_resposta(self):
        
        if  self.erro_busca_instrucao:           
            return        
        
        self.lista_mensagens.append({"role": "user", "content": "A reposta anterior está correta? Retorne um json com o campo resposta_correta (true or false)"})        
                
        try:
        
            self.resposta = openai.chat.completions.create(messages=self.lista_mensagens, model="gpt-3.5-turbo")            
            self.lista_mensagens.append({"role": "assistant", "content": self.resposta.choices[0].message.content})
            resultado = json.loads(self.resposta.choices[0].message.content)                        
            self.confirmacao_instrucao=bool(resultado["resposta_correta"])                        
            self.erro_confirmacao_instrucao=False
            
        except:
            self.erro_confirmacao_instrucao=True
            self.confirmacao_instrucao=False
            
    
    
    def confirmar_todos_campos_chatgpt_resposta(self):
        
        if  self.erro_busca_instrucao:            
            return
        if not self.confirmacao_instrucao:
            return
        
        self.lista_mensagens.append({"role": "user", "content": "Todos os campos utilizados existem nas tabelas passadas? Retorne um jsom com o campo todos_campos_existem (true or false)"})        
                
        try:
        
            self.resposta = openai.chat.completions.create(messages=self.lista_mensagens, model="gpt-3.5-turbo")            
            self.lista_mensagens.append({"role": "assistant", "content": self.resposta.choices[0].message.content})
            resultado = json.loads(self.resposta.choices[0].message.content)                                               
            self.confirmacao_instrucao=bool(resultado["todos_campos_existem"])
            self.erro_confirmacao_instrucao=False
            
        except:
            self.erro_confirmacao_instrucao=True
            self.confirmacao_instrucao=False
    
            
    def obter_chatgpt_nova_instrucao_select(self):
        
        if self.confirmacao_instrucao:
            
            return
        
        self.lista_mensagens.append({"role": "user", "content": "Você respondeu que a instrução sql não estava correta. Qual seria a instrução SQL correta"})        
        self.lista_mensagens.append({"role": "user", "content": "Retorne um json com os seguintes atributos: conseguiu_montar_instrucao_sql (true or false), instrucao_sql e motivo_nao_ter_montado"})
        
        try:
            self.resposta = openai.chat.completions.create(messages=self.lista_mensagens, model="gpt-3.5-turbo")
            resultado = json.loads(self.resposta.choices[0].message.content)            
            self.lista_mensagens.append({"role": "assistant", "content": self.resposta.choices[0].message.content})
            self.executou_busca_instrucao=bool(resultado["conseguiu_montar_instrucao_sql"])
            self.instrucao_sql=resultado["instrucao_sql"]            
        except:
            self.executou_busca_instrucao=False
            
    def obter_instrucao_select(self, pergunta, erro):
        
        for contador in range(1, 6):
            
            if erro =="":            
                self.lista_mensagens=[]           

            self.obter_chatgpt_instrucao_select(pergunta, erro)
            self.confirmar_chatgpt_resposta()
            self.confirmar_todos_campos_chatgpt_resposta()
            if self.confirmacao_instrucao:
                    return True
            
            print(contador)
            self.obter_chatgpt_nova_instrucao_select()
            self.confirmar_chatgpt_resposta()
            self.confirmar_todos_campos_chatgpt_resposta()
            if self.confirmacao_instrucao:
                return True
        
        return False
    
    def obter_html_resposta_consulta_banco(self, json_resposta):
       
        self.lista_mensagens.append({"role": "user", "content": "A instrução que você gerou foi executada no SQL Server e o resultado é este json:"})        
        self.lista_mensagens.append({"role": "user", "content": json_resposta})
        self.lista_mensagens.append({"role": "user", "content": "Gere um html utilizando bootstrap que será colocado dentro de uma div para que esta resposta seja mostrada no sistema"})        
        self.lista_mensagens.append({"role": "user", "content": "Valores devem estar formatados para a o idioma Portugês-Brasil e as fontes devem ter tamanho pequeno.Não use as tags <h1>, <h2> nem <h3>"})        
        self.lista_mensagens.append({"role": "user", "content": "Retorne um json com os atributos htmldiv e htmlLink"})
        
        try:
            self.resposta = openai.chat.completions.create(messages=self.lista_mensagens, model="gpt-3.5-turbo")            
            self.lista_mensagens.append({"role": "assistant", "content": self.resposta.choices[0].message.content})
            resultado = json.loads(self.resposta.choices[0].message.content) 
            return resultado["htmldiv"]
            
        except:
            self.executou_busca_instrucao=False
            
            return ""
    
  


             
                
            
            
        

