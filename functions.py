
import requests
import pandas as pd
from plyer import notification
import sqlite3


def verificar_api(url, nome_api, lista):
    """
    Verifica APIs indisponíveis

    Parâmetros:
    url: url da API
    nome_api: nome da API
    lista: lista de APIs indisponíveis

    """
    resp = requests.get(url)
    if resp.status_code != 200:
        lista.append(nome_api)


def api_indisponivel(lista):
    """
    Notifica APIs indisponíveis

    Parâmetros:
    lista: lista de apis indisponíveis

    """
    if lista:
        message = f'Não foi possível acessar as seguintes APIs: {", ".join(lista)}'
    notification.notify(
        title='APIs Indisponíveis',
        message=message,
        timeout=15
    )


def retorna_municipios(siglaUF):
    """
    Retorna os dados brutos dos municípios por unidade federativa

    Parâmetros:
    siglaUF: Sigla da unidade federativa (Exemplo: SP, BA, RJ)

    Retorna: 
    Lista de municípios por unidade federativa. 
    Caso a api estiver indisponível, uma mensagem de erro irá aparecer. 

    """
    url = f'https://brasilapi.com.br/api/ibge/municipios/v1/{siglaUF}?providers=dados-abertos-br,gov,wikipedia'
    resp = requests.get(url)
    if resp.status_code == 200:
        data_municipios = resp.json()
        return data_municipios
    else:
        print(f"Falha na solicitação da API para {siglaUF}.")


def trata_municipio(muni):
    """
    Trata os dados recebidos pela API de municípios, desaninhando e renomeando colunas.

    Parâmetros:
    muni: lista com os dados dos municípios

    Retorna: 
    Lista de municípios tratados

    """
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
            lista_municipios.append(
                {'uf': uf, 'nome': nome, 'codigo_ibge': codigo_ibge})
    return lista_municipios


def texto_em_maiusculo(data, col):
    """
    Transforma um conjunto de strings em maiúsculo

    Parâmetros:
    data: dataframe a ser trabalhado
    col: coluna na qual os caracteres serão alterados

    """
    data[col] = data[col].str.upper()


def string_data(data):
    """
    Transforma dados de data que estão no formato string para datetime

    Parâmetros:
    data: dataframe trabalhado

    """
    for column in data.columns:
        if 'data' in column:
            data[column] = pd.to_datetime(data[column])


def string_vazia(data, coluna):
    """
    Identifica e quantifica as colunas que possuem valores vazios que não são reconhecidos pelo método .isna()

    Parâmetros:
    data: dataframe trabalhado
    coluna: coluna a ser trabalhada

    Retorna: 
    A quantidade de campos vazios de uma determinada coluna.

    """
    resultado = (data[coluna] == '').sum()
    vazio = f"A coluna {coluna} do Dataframe possui {resultado} campos em branco"
    return vazio


def transforma_int(data, coluna):
    """
    Transforma campos string '' em zeros 

    Parâmetros:
    data: dataframe trabalhado
    coluna: coluna a ser trabalhada

    """
    data[coluna] = data[coluna].replace('', 0)
    data[coluna] = data[coluna].astype(int)


def elimina_vazios_int(data, coluna):
    """
    Elimina os campos que possuem o valor 0 de uma determinada coluna

    Parâmetros:
    data: dataframe trabalhado
    coluna: coluna a ser trabalhada

    Retorna:
    Dataframe filtrado sem os zeros na coluna indicada

    """
    data = data[data[coluna] != 0]
    data.reset_index(drop=True, inplace=True)
    return data


def elimina_tel(data, coluna):
    """
    Elimina campos que possuem telefones com menos de 7 dígitos

    Parâmetros:
    data: dataframe trabalhado
    coluna: coluna a ser trabalhada

    Retorna:
    Dataframe filtrado apenas com telefones com 7 ou 8 dígitos 

    """
    data[coluna] = data[coluna].astype(str)
    data = data[data[coluna].str.len() >= 7]
    data.loc[:, coluna] = data[coluna].astype(int)
    data.reset_index(drop=True, inplace=True)
    return data


def adiciona_3_telefone(data, coluna):
    """
    Adiciona o número 3 na frente dos telefones que possuem 7 dígitos

    Parâmetros:
    data: dataframe trabalhado
    coluna: coluna a ser trabalhada

    Retorna:
    Dataframe filtrado com todos os telefones com 8 dígitos

    """
    filtro = data[coluna].astype(str).str.len() == 7
    data.loc[filtro, coluna] = '3' + data.loc[filtro, coluna].astype(str)
    data[coluna] = data[coluna].astype(int)
    return data


def transforma_float(data, coluna):
    """
    Transforma campos em float de uma determinada coluna

    Parâmetros:
    data: dataframe trabalhado
    coluna: coluna a ser trabalhada

    """
    data[coluna] = data[coluna].astype(float)
    data[coluna] = data[coluna].round(2)


def remove_caractere_especial(data, col):
    """
    Remove os caracteres especiais de uma coluna

    Parâmetros:
    data: dataframe trabalhado
    col: coluna a ser trabalhada

    """
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


def tabelas_bd():
    """
    Estabelece uma conexão com o banco de dados e mostra todas as tabelas existentes nele.

    """
    conn = sqlite3.connect('00_db/corretoras-brasil.db')
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    schema = pd.read_sql(query, conn)
    print(schema)
    conn.close()


def salva_bd(df, nome_tabela):
    """
    Salva uma tabela nova no banco de dados

    Parâmetros:
    df: dataframe trabalhado
    nome_tabela: nome dado a tabela dentro do banco de dados

    """
    conn = sqlite3.connect('00_db/corretoras-brasil.db')
    df.to_sql(nome_tabela, conn, if_exists='replace', index=False)
    conn.close()


def carrega_bd(nome_tabela):
    """
    Consulta uma tabela em um banco de dados

    Parâmetros:
    nome_tabela: nome da tabela no banco de dados

    Retorna:
    Dados da tabela obtidos durante a consulta

    """
    conn = sqlite3.connect('00_db/corretoras-brasil.db')
    query = f"SELECT * FROM {nome_tabela}"
    consulta = pd.read_sql(query, conn)
    conn.close()
    return consulta


def unstacked_count_agg(df, index, coluna, agg):
    """
    Realiza unstack (desempilhamento) de um dataframe

    Parâmetros:
    df: dataframe trabalhado
    index: coluna a ser desempilhada
    coluna: coluna para agregação
    agg: o tipo de agregação

    Retorna:
    Dataframe desempilhado e agregado com base em outra coluna

    """
    # agrupando o df e adicionando uma função de agregação
    grouped = df.groupby([f'{index}', f'{coluna}'])[f'{coluna}'].agg(agg)
    # unstack na segunda coluna
    unstacked = grouped.unstack(level=1)
    unstacked = unstacked.fillna(0)
    return unstacked


def stacked_tabela(df, index, colunas):
    """
    Realiza stack (empilhamento) de um dataframe

    Parâmetros:
    df: dataframe trabalhado
    index: coluna para ser utilizada como index 
    colunas: colunas a serem empuilhadas

    Retorna:
    Dataframe empilhado com base em determinadas colunas

    """
    # df com as colunas a serem empilhadas
    stacked_df = df.set_index([index])[colunas].stack().reset_index()
    stacked_df.columns = [index, 'colunas_empilhadas', 'valores']
    return stacked_df


def alerta_etapa_concluida(base, nome, etapa):
    """
    Alerta de etapa concluida

    Parâmetros:
    base: dataframe trabalhado
    nome: nome do dataframe
    etapa: etapa concluida

    """
    if base:
        message = f'A base {nome} foi {etapa} com sucesso'
        notification.notify(
            title='Concluído',
            message=message,
            timeout=15)
