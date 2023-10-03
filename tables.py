import requests
import functions as fun
import pandas as pd

# lista para armazenar os nomes das APIs que não foram carregadas com sucesso
api_erro = []

# pegando dados da API
resp_corretoras = requests.get("https://brasilapi.com.br/api/cvm/corretoras/v1")
resp_bancos = requests.get("https://brasilapi.com.br/api/banks/v1")
resp_cidade = requests.get("https://brasilapi.com.br/api/cptec/v1/cidade")
resp_estados = requests.get("https://brasilapi.com.br/api/ibge/uf/v1")

# verificação de apis usando a função verificar_api
fun.verificar_api("https://brasilapi.com.br/api/cvm/corretoras/v1", "Corretoras", api_erro)
fun.verificar_api("https://brasilapi.com.br/api/banks/v1", "Bancos", api_erro)
fun.verificar_api("https://brasilapi.com.br/api/cptec/v1/cidade", "Cidades", api_erro)
fun.verificar_api("https://brasilapi.com.br/api/ibge/uf/v1", "Estados", api_erro)

# se api x estiver indisponível:
if api_erro: 
    fun.api_indisponivel(api_erro)
# se não, armazene os dados nessas variáveis:    
else:
    data_corretoras = requests.get("https://brasilapi.com.br/api/cvm/corretoras/v1").json()
    data_bancos = requests.get("https://brasilapi.com.br/api/banks/v1").json()
    data_cidade = requests.get("https://brasilapi.com.br/api/cptec/v1/cidade").json()
    data_estados = requests.get("https://brasilapi.com.br/api/ibge/uf/v1").json()

# colocando dados em um dataframe
corretoras = pd.DataFrame(data_corretoras)
bancos = pd.DataFrame(data_bancos)
cidade = pd.DataFrame(data_cidade)
estados = pd.DataFrame(data_estados)