# corretoras-brasil

Projeto final do curso de Python da Coderhouse. Trata-se de um banco de dados sobre as corretoras de títulos e valores mobiliários presentes no sistema de Comissão de Valores Mobiliários (CVM), cujos dados foram adquiridos pela API do Brasil API.

## 📌 Sobre

O objetivo deste projeto é criar um banco de dados sobre as corretoras de títulos e valores mobiliários no país, sendo relacionados com os dados municipais e estaduais disponibilizados pelo Instituto Brasileiro de Geografia e Estatística - IBGE. Os dados foram obtidos pela Brasil API, que compila dados sobre diversas instâncias sobre o Brasil.

### API

Para coleta dos dados, foi utilizado a API do Brasil API, que conta com diversos dados do Brasil. A documentação da API utilizada pode ser acessada clicando [aqui](https://brasilapi.com.br/docs#tag/Corretoras). Para o projeto, foram utilizadas as seguintes APIs:

- CVM
- Munícipios (IBGE)
- Unidades Federativas (IBGE)

## 📋 Pré-requisitos

- Python 3
- Visual Code Studio

## 🔧 Instalação

Baixe os arquivos:

- [tables.py]()
- [functions.py]()

### Arquivos

O arquivo **tables.py** possui o caminho de extração, tratamento e armazenamento dos dados em .csv e em um banco de dados (corretoras-brasil.db).

O arquivo **functions.py** possui as funções que serão implementadas dentro do arquivo principal de tabelas (tables.py) e funções de notificação em caso de erro de execução de alguma API.

### Importando bibliotecas

Você pode conferir quais bibliotecas e suas respectivas versões utilizadas na elaboração do projeto acessando [requirements.txt]().

## ⚙️ Estrutura e execução

O processo de recebimento dos dados, tratamento e armazenamento está dividido da seguinte forma no arquivo **tables.py**:

1. Acessando dados das APIs
2. Salvando dados brutos em .csv
3. Tratamento de dados
4. Stack e unstack para visualização de dados
5. Salvando bases tratadas em .csv
6. Armazenamento dos dados tratados em um banco de dados relacional

## 🔩 Testes

### Verificação de APIs

Verifica se foi possível acessar as APIs das Corretoras e dos Estados usando as **funções verificar_api e api_indisponível**.

```
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
```

Lembrando que a **função verificar_api**, que fica no arquivo **functions.py**, tem como parâmetros a url do API, nome da tabela e a lista api_erro, que armazena o nome da tabela caso a API estiver indisponível.

```
def verificar_api(url, nome_api, lista):
    resp = requests.get(url)
    # se a resposta for diferente de 200 (indisponivel)
    if resp.status_code !=200:
        # colocar nome da api na lista de apis indisponíveis
        lista.append(nome_api)
```

A função **api_indisponivel** tem como parâmetro a lista com os nomes das APIs que não foram acessadas. A função recebe os nomes e notifica o usuário quais APIs estão indisponíveis.

```
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
```

### Tratamento de dados

Para a identificação dos dados a serem tratados, foram utilizados os métodos `.info()` e `.head()` para poder identificar:

- Formato das tabelas
- Existência de valores nulos
- Missing Values não nulos
- Duplicatas
- Colunas não essenciais para a análise da tabela
- Tratamento de campos (retirada de caracteres especiais e aplicação do .upper())
- Valores incompletos
- Transformação de tipos de dados

```
# CORRETORAS
print(corretoras.info())
corretoras.head()

# ESTADOS
print(estados.info())
estados.head()

# MUNICIPIOS
print(municipios.info())
municipios.head()
```

Lembrando que o processo de verificação do tratamento desses dados é contínuo durante toda a execução a fim de manter os dados com maior qualidade possível.

#### Funções de tratamento de dados

O tratamento de dados foi otimizado com algumas funções. 

A função ```trata_municipio()``` trata os dados iniciais recebidos pela API de municípios. A função recebe como parâmetro o DataFrame que contem os dados brutos dos municípios. Os dados em questão são estão aninhados, ou seja, trata-se de uma lista dentro de uma lista. O objetivo da função é justamente desaninhar os dados e deixá-los em formato de tabela.
```
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
``` 


Para deixar os caracteres em maiúsculo, utilize ```texto_em_maiusculo()```, que recebe como parâmetros o DataFrame e a coluna que você deseja deixar em maiúsculo.
```
def texto_em_maiusculo(data, col):
    # colocando caracteres em maiusculo
    data[col] = data[col].str.upper()
```


A transformação de dados de string para datetime é feita por meio da função ```string_data()```, que recebe como parâmetro o DataFrame e identifica as colunas que possuem o nome 'data'. 
```
def string_data(data):
    # para cada cabeçalho de coluna presente na coluna de um determinado dataframe
    for column in data.columns:
        # se o cabeçalho da coluna conter 'data'
        if 'data' in column:
            # altere o tipo da coluna para datetime
            data[column] = pd.to_datetime(data[column])
```



Os campos que possuem valores vazios, mas que não são considerados nulos, são tratados com a função ```string_vazia()```, que recebe como parâmetros o DataFrame e a coluna que deseja tratar. 
```
def string_vazia(data, coluna):
    # filtrando colunas com '' 
    resultado = (data[coluna] == '').sum()
    # printando resultado
    vazio = f"A coluna {coluna} do Dataframe possui {resultado} campos em branco"
    return vazio
```



Para eliminar campos vazios string em campos int utilize ```elimina_vazios_int()```, que recebe o DataFrame e a coluna e transforma os '' em zeros.
```
def elimina_vazios_int(data, coluna):
    # filtrando apenas por valores diferentes de zero
    data = data[data[coluna] != 0]
    # resetando indices
    data.reset_index(drop=True, inplace=True)
    # retornando valor para armazenar na variavel .py principal
    return data
```

A função ```transforma_float()```, recebe um DataFrame e uma coluna como parâmetros e tem como objetivo transformar campos em float com duas casas decimais. 
```
def transforma_float(data, coluna):
    # transformando valor para float
    data[coluna] = data[coluna].astype(float)
    # arredondando para duas casas decimais
    data[coluna] = data[coluna].round(2)
```

O tratamento de caracteres especiais é feito pela função ```remove_caractere_especial()```, recebendo o DF e a coluna que deseja ser tratada. 
```
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
```

O tratamento da coluna de telefone do DataFrame corretoras é feito com a função ```adciona_3_telefone()```, recebendo o DF e a coluna que deseja ser tratada. O objetivo da função é adicionar o número 3 em telefones que contenham apenas 7 dígitos. 
```
def adiciona_3_telefone(data, coluna):
    # filtro transformando a coluna em string e selecionando apenas os telefones com 7 digitos
    filtro = data[coluna].astype(str).str.len() == 7
    # adicionando '3' apenas aos registros filtrados
    data.loc[filtro, coluna] = '3' + data.loc[filtro, coluna].astype(str)
    # convertendo a coluna de volta para inteiros 
    data[coluna] = data[coluna].astype(int)
    # retornando valor para armazenar na variavel .py principal
    return data
```

### Consulta de tabelas

Para consultar as tabelas criadas você pode utilizar a seguinte função **tabelas_bd()**.

```
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
```

Para consultar uma tabela em específico você pode utilizar a seguinte função **carrega_bd()**.

```
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
```
