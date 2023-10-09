
# * ----------------- IMPORTANDO BIBLIOTECAS
import requests
import pandas as pd
from plyer import notification
import sqlite3



# ! ----------------- FUNÇÃO PARA VERIFICAR APIS
def verificar_api(url, nome_api, lista):
    resp = requests.get(url)
    # se a resposta for diferente de 200 (indisponivel)
    if resp.status_code !=200: 
        # colocar nome da api na lista de apis indisponíveis
        lista.append(nome_api)



# ! ----------------- FUNÇÃO NOTIFY API INDISPONÍVEL
def api_indisponivel(lista):
    # se a lista de apis indisponíveis for true, ou seja, se tiver algum item
    if lista: 
        # notify de erro 
        message = f'Não foi possível acessar as seguintes APIs: {", ".join(lista)}'
    notification.notify(
        title='APIs Indisponíveis',
        message=message,
        timeout=15
    )



# ! ----------------- FUNÇÃO PARA RETORNAR MUNICIPIOS DA API DO IBGE
def retorna_municipios(siglaUF):
    # url da api de municipios do ibge
    url = f'https://brasilapi.com.br/api/ibge/municipios/v1/{siglaUF}?providers=dados-abertos-br,gov,wikipedia'
    resp = requests.get(url)
    # se a api estiver disponível
    if resp.status_code == 200:
        # salve os dados json em data_municipios
        data_municipios = resp.json()
        # retorne o valor de data_municipios para ser armazenado na variavel do .py principal
        return data_municipios
    else:
        # se não, imprima essa mensagem de erro
        print(f"Falha na solicitação da API para {siglaUF}.")



# ! ----------------- FUNÇÃO PARA TRATAR DADOS DA API MUNICIPIOS IBGE
def trata_municipio(muni):
    # lista para salvar os dados tratados dos municipios
    lista_municipios = []
    # para cada municipio por uf presente na lista de municipios brutos aninhados
    for lista_municipios_uf in muni:
        # para cada municipio puro presente na lista de municipio por uf 
        for municipio in lista_municipios_uf:
            # atribuindo colunas
            nome = municipio['nome']
            codigo_ibge = municipio['codigo_ibge']
            uf = municipio['uf']
            # adicionando dados tratados a lista de municipios
            lista_municipios.append({'uf': uf,'nome': nome, 'codigo_ibge': codigo_ibge})
    # retornando os dados tratados para serem armazenados na variavel do .py principal
    return lista_municipios



# ! ----------------- FUNÇÃO STRING EM MAIÚSCULO
def texto_em_maiusculo(data, col):
    # colocando caracteres em maiusculo
    data[col] = data[col].str.upper()



# ! -----------------  FUNÇÃO TRANSFORMAR STRING EM DATETIME
def string_data(data):
    # para cada cabeçalho de coluna presente na coluna de um determinado dataframe
    for column in data.columns:
        # se o cabeçalho da coluna conter 'data'
        if 'data' in column:
            # altere o tipo da coluna para datetime
            data[column] = pd.to_datetime(data[column])



# ! ----------------- FUNÇÃO PARA VERIFICAR SE EXISTEM CAMPOS VAZIOS (QUE NÃO PEGAM .isna())
def string_vazia(data, coluna):
    # filtrando colunas com '' 
    resultado = (data[coluna] == '').sum()
    # printando resultado
    vazio = f"A coluna {coluna} do Dataframe possui {resultado} campos em branco"
    return vazio



# ! ----------------- FUNÇÃO TRANSFORMAR STRING '' EM INT
def transforma_int(data, coluna):
    # substituindo '' por 0
    data[coluna] = data[coluna].replace('', 0)
    # transformando para int
    data[coluna] = data[coluna].astype(int)
    # verificando
    data.info()



# ! ----------------- FUNÇÃO PARA ELIMINAR VALORES 0 DO TIPO INT
def elimina_vazios_int(data, coluna):
    # filtrando apenas por valores diferentes de zero
    data = data[data[coluna] != 0]
    # resetando indices
    data.reset_index(drop=True, inplace=True)
    # retornando valor para armazenar na variavel .py principal
    return data



# ! ----------------- FUNÇÃO PARA ELIMINAR VALORES DE TELEFONE COM MENOS DE 7 DIGITOS
def elimina_tel(data, coluna):
    # mudando a coluna para type string
    data[coluna] = data[coluna].astype(str)
    # filtro para selecionar registros com o número de caracteres igual ou maior que 7
    data = data[data[coluna].str.len() >= 7]
    # transformando para int
    data.loc[:, coluna] = data[coluna].astype(int)
    # resetando indice
    data.reset_index(drop=True, inplace=True)
    # retornando valor para armazenar na variavel .py principal
    return data



# ! -----------------  FUNÇÃO PARA ADICIONAR NÚMERO 3 EM TELEFONES COM 7 DIGITOS
def adiciona_3_telefone(data, coluna):
    # filtro transformando a coluna em string e selecionando apenas os telefones com 7 digitos
    filtro = data[coluna].astype(str).str.len() == 7
    # adicionando '3' apenas aos registros filtrados
    data.loc[filtro, coluna] = '3' + data.loc[filtro, coluna].astype(str)
    # convertendo a coluna de volta para inteiros 
    data[coluna] = data[coluna].astype(int)
    # retornando valor para armazenar na variavel .py principal
    return data



# ! -----------------  FUNÇÃO PARA TRANSFORMAR EM FLOAT
def transforma_float(data, coluna):
    # transformando valor para float
    data[coluna] = data[coluna].astype(float)
    # arredondando para duas casas decimais
    data[coluna] = data[coluna].round(2)



# ! ----------------- FUNÇÃO PARA REMOVER CARACTERES ESPECIAIS 
def remove_caractere_especial(data, col):
    # substituido carecteres especiais na string
    data[col] = data[col].str.replace('Ç', 'C')
    data[col] = data[col].str.replace('Á', 'A')
    data[col] = data[col].str.replace('Ã', 'A')
    data[col] = data[col].str.replace('À', 'A')
    data[col] = data[col].str.replace('Â', 'A')
    data[col] = data[col].str.replace('É', 'E')
    data[col] = data[col].str.replace('È', 'E')
    data[col] = data[col].str.replace('Ê', 'E')
    data[col] = data[col].str.replace('Í', 'I')
    data[col] = data[col].str.replace('Ì', 'I')
    data[col] = data[col].str.replace('Ó', 'O')
    data[col] = data[col].str.replace('Ò', 'O')
    data[col] = data[col].str.replace('Ô', 'O')
    data[col] = data[col].str.replace('Ú', 'U')
    data[col] = data[col].str.replace('Ù', 'U')



# ! ----------------- FUNÇÃO PARA VISUALIZAR TABELAS DO DB 
def tabelas_bd():
    # fazendo conexão
    conn = sqlite3.connect('00_db/corretoras-brasil.db')
    # definindo query
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    # salvado os dados em um dataframe
    schema = pd.read_sql(query, conn)
    # imprimindo resultados
    print(schema)
    # fechando conexão
    conn.close()



# ! ----------------- FUNÇÃO PARA SALVAR TABELA NO DB
def salva_bd(df, nome_tabela):
    # fazendo conexão
    conn = sqlite3.connect('00_db/corretoras-brasil.db')
    # salvando dataframe na tabela
    df.to_sql(nome_tabela, conn, if_exists='replace', index=False)
    # fechando conexão
    conn.close()



# ! ----------------- FUNÇÃO PARA VISUALIZAR UMA TABELA EM ESPECIFICO NO DB
def carrega_bd(nome_tabela):
    # fazendo conexão
    conn = sqlite3.connect('00_db/corretoras-brasil.db')
    # fazendo a consulta da tabela nome_tabela
    query = f"SELECT * FROM {nome_tabela}"
    # salvando resultado em uma variavel
    consulta = pd.read_sql(query, conn)
    # fechando conexão
    conn.close()
    # retornando resultado obtido da consulta
    return consulta
