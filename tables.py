
# * ----------------- IMPORTANDO BIBLIOTECAS

import requests
import functions as fun
import pandas as pd

# * ----------------- ACESSANDO APIS
# ! 1) LISTA DE ERRO
# lista para armazenar os nomes das APIs que não foram carregadas com sucesso
api_erro = []



# ! 2) URL DAS APIS
# corretoras
resp_corretoras = "https://brasilapi.com.br/api/cvm/corretoras/v1"

# estados
resp_estados = "https://brasilapi.com.br/api/ibge/uf/v1"



# ! 3) RETORNANDO DADOS DAS APIS

# 3.1) pegando dados API municipios do IBGE
# definindo lista de municipios para armazenar os dados da api de municípios
dados_municipios = []

# a api de municípios é necessita de uma chave para ser chamada (a sigla da unidade federativa)
# lista de siglas das unidades federativas para inserir na url da api e gerar dados dos municipios
siglas_uf = ['RO', 'AC', 'AM', 'RR', 'PA', 'AP', 'TO', 'MA', 'PI', 
    'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA', 'MG', 
    'ES', 'RJ', 'SP', 'PR', 'SC', 'RS', 'MS', 'MT', 'GO', 'DF']

# iterador de siglas para poder acessar os dados de município de cada uf
# para cada uf na lista siglas_uf
for uf in siglas_uf:
        # foi feita uma função cujo objetivo é retornar os dados da api
        # armazenando os dados da função (que recebe a uf dentro da lista de siglas_uf)
        muni_uf = fun.retorna_municipios(uf)
        # para cada cidade presente na lista muni_uf
        for cidade in muni_uf:
            # criando coluna uf para adicionar a lista de dados da api
            cidade['uf'] = uf
            # fazendo um append de todos os municipios de cada uf na lista dados_municipio
            dados_municipios.append(muni_uf)

# tratando lista dados municipios para tirar dados aninhados
data_municipios = fun.trata_municipio(dados_municipios)


# 3.2) verificação de apis de corretoras e estados usando a função verificar_api
#corretoras
fun.verificar_api(resp_corretoras, "Corretoras", api_erro)

#estados
fun.verificar_api(resp_estados, "Estados", api_erro)

# se uma das apis (corretoras ou estado) estiver indisponível:
if api_erro: 
    fun.api_indisponivel(api_erro)
# se não, armazene os dados nessas variáveis:    
else:
    data_corretoras = requests.get(resp_corretoras).json()
    data_estados = requests.get(resp_estados).json()



#  ! 4) COLOCANDO DADOS DAS APIS EM DATAFRAMES
#corretoras
corretoras = pd.DataFrame(data_corretoras)

# estados
estados = pd.DataFrame(data_estados)

# municipios
municipios = pd.DataFrame(data_municipios)




# * ----------------- SALVANDO BASES BRUTAS .CSV
# corretoras
corretoras.to_csv('01_csv_files/dados_brutos/corretoras_bruto.csv')

# estados
estados.to_csv('01_csv_files/dados_brutos/estados_bruto.csv')

# municipios
municipios.to_csv('01_csv_files/dados_brutos/municipios_bruto.csv')




# * ----------------- TRATAMENTO DE DADOS
# ! 1) VERIFICAÇÃO DE DADOS
# verificando as tabelas 

# CORRETORAS
# print(corretoras.info()) 

# ESTADOS 
# print(estados.info()) 

# MUNICIPIOS
# print(municipios.info()) 



# ! 2) TRATANDO DADOS DF CORRETORAS
# transformando dados de data de string para datetime
fun.string_data(corretoras)

# COLUNA 'telefone': 
# eliminando linhas que não possuem números de telefone
fun.string_vazia(corretoras, 'telefone') # * 41 campos em branco

# transformando coluna para tipo int
fun.transforma_int(corretoras, 'telefone')

# eliminando vazios
corretoras_tratado = fun.elimina_vazios_int(corretoras, 'telefone')

# eliminando números com menos de 7 digitos
corretoras_tratado = fun.elimina_tel(corretoras_tratado, 'telefone')

# adicionando o número 3 em telefones que possuem 7 digitos
corretoras_tratado = fun.adiciona_3_telefone(corretoras_tratado, 'telefone')


# COLUNA 'email', 'complemento', 'bairro', 'type', 'pais', 'cep':
# dropando colunas com muitos missing values não essenciais para a análise
corretoras_tratado = corretoras_tratado.drop(['email', 'complemento', 'bairro', 'type', 'pais', 'cep'], axis=1)
corretoras_tratado.reset_index(drop=True, inplace=True)


# COLUNA 'cnpj': 
# transformar para int
fun.transforma_int(corretoras_tratado, 'cnpj')

# dropando duplicatas
corretoras_tratado = corretoras_tratado.drop_duplicates(subset='cnpj', keep='last')

# COLUNA 'codigo_cvm': 
# transformar para int
fun.transforma_int(corretoras_tratado, 'codigo_cvm')


# COLUNA 'valor_patrimonio_liquido', 'logradouro', 'municipio', 'nome_comercial':
# remover valores vazios pontuais nas demais colunas que possuem valores vazios 
fun.string_vazia(corretoras_tratado, 'valor_patrimonio_liquido') #* 3 em branco
fun.string_vazia(corretoras_tratado, 'logradouro') #* 1 em branco
fun.string_vazia(corretoras_tratado, 'municipio') #* 1 em branco -- se apagar o registro em branco do logradouro, apaga esse registro tb
fun.string_vazia(corretoras_tratado, 'nome_comercial') #* 14 valores em branco

# valor_patrimonio_liquido 
corretoras_tratado = corretoras_tratado[corretoras_tratado['valor_patrimonio_liquido']!= '']

# logradouro
corretoras_tratado = corretoras_tratado[corretoras_tratado['logradouro']!= '']

#nome_comercial
corretoras_tratado = corretoras_tratado[corretoras_tratado['nome_comercial']!= '']
corretoras_tratado = corretoras_tratado[corretoras_tratado['nome_comercial']!= '--']
corretoras_tratado = corretoras_tratado[corretoras_tratado['nome_comercial']!= '-----']


# COLUNA 'valor_patrimonio_liquido':
# transformar para float com duas casas decimais
fun.transforma_float(corretoras_tratado, 'valor_patrimonio_liquido')

# remover valores = 0
corretoras_tratado = corretoras_tratado[corretoras_tratado['valor_patrimonio_liquido'] != 0]

# COLUNA 'nome_social', 'nome_comercial', 'logradouro':
# strings em maiúsculo
fun.texto_em_maiusculo(corretoras_tratado, 'nome_social')
fun.texto_em_maiusculo(corretoras_tratado, 'nome_comercial')
fun.texto_em_maiusculo(corretoras_tratado, 'logradouro')

# COLUNA 'municipio':
# retirar caracteres especiais
fun.remove_caractere_especial(corretoras_tratado, 'municipio')

# TODAS AS COLUNAS
# ordenando colunas
nova_ordem_colunas = ['codigo_cvm','cnpj', 'nome_social', 'nome_comercial', 'status', 'telefone', 'uf', 'municipio', 'logradouro', 'data_patrimonio_liquido', 'valor_patrimonio_liquido', 'data_inicio_situacao', 'data_registro']
corretoras_tratado = corretoras_tratado[nova_ordem_colunas]


# resetando index
corretoras_tratado.reset_index(drop=True, inplace=True)



# ! 3) TRATANDO DADOS DF ESTADOS

# reorganizando colunas
# COLUNA 'id'
id = [estados['id'] for estados in data_estados]

# COLUNA 'uf'
sigla = [estados['sigla'] for estados in data_estados]

# COLUNA 'nome'
nome = [estados['nome'] for estados in data_estados]

# COLUNA 'regiao'
regiao = [estados['regiao']['nome'] for estados in data_estados]

# COLUNA 'sigla_regiao'
sigla_regiao = [estados['regiao']['sigla'] for estados in data_estados]

# adicionando dados tratados em um novo dataframe
estados_tratado = pd.DataFrame({
    "uf": sigla, 
    "id": id,
    "nome": nome,
    "regiao": regiao,
    "sigla_regiao": sigla_regiao
})

# COLUNA 'nome' e 'regiao':
# colocando caracteres em maiusculo
fun.texto_em_maiusculo(estados_tratado, 'nome')
fun.texto_em_maiusculo(estados_tratado, 'regiao')

# tirando caracteres especiais
fun.remove_caractere_especial(estados_tratado, 'nome')


# COLUNA 'id':
# transformando para int
fun.transforma_int(estados_tratado, 'id')



# ! 4) TRATANDO DADOS DF MUNICIPIOS
# TODAS AS COLUNAS:
# removendo duplicatas
municipios.drop_duplicates()

# resetando index
municipios.reset_index(drop=True, inplace=True)

# COLUNA 'nome':
# colocando todos os nomes em maíusuculo
fun.texto_em_maiusculo(municipios, 'nome')

# retirando caracteres especiais
fun.remove_caractere_especial(municipios, 'nome')

# renomeando a coluna 'nome' para 'municipio'
municipios_tradado = municipios.rename(columns={'nome': 'municipio'})

# TODAS AS COLUNAS:
# reordenando colunas
nova_ordem_municipio = ['codigo_ibge', 'municipio', 'uf']
municipios_tratado = municipios_tradado[nova_ordem_municipio]




# * ----------------- SALVANDO BASES TRATADAS .CSV
# corretoras
corretoras_tratado.to_csv('01_csv_files/dados_tratados/corretoras_tratado.csv')

# estados
estados_tratado.to_csv('01_csv_files/dados_tratados/estados_tratado.csv')

# municipios
municipios_tratado.to_csv('01_csv_files/dados_tratados/municipios_tratado.csv')




# * ----------------- ARMAZENANDO DADOS EM UM DB
# corretoras
fun.salva_bd(corretoras_tratado, 'corretoras')

# estados
fun.salva_bd(estados_tratado, 'estados')

# municipios
fun.salva_bd(municipios_tratado, 'municipios')

# consultando
fun.tabelas_bd()