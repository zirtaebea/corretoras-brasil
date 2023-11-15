# corretoras-brasil

Projeto final do curso de Python da Coderhouse. O objetivo desta aplicação foi desenvolver um pipeline de dados, incluindo extração, tratamento e armazenamento dos dados em um Banco de Dados.

## 📋 Pré-requisitos

- Python 3
- Visual Code Studio

## 🔧 Instalação

Baixe os arquivos:

- [tables.py](https://github.com/zirtaebea/corretoras-brasil/blob/main/tables.py)
- [functions.py](https://github.com/zirtaebea/corretoras-brasil/blob/main/functions.py)

## 💻 APIs

Para a elaboração do projeto, foram consumidos os dados disponibilizados pela **Brasil API** que compila dados sobre diversas instâncias sobre o Brasil. Foram utilizadas as APIs:

- Corretoras
- Munícipios (IBGE)
- Unidades Federativas (IBGE)

### Corretoras

Retorna as corretoras de títulos e valores mobiliários presentes nas informações da CVM.

```
https://brasilapi.com.br/api/cvm/corretoras/v1
```

### Municípios (IBGE)

Retorna os municípios de uma determinada unidade federativa (uf).

```
https://brasilapi.com.br/api/ibge/municipios/v1/{siglaUF}?providers=dados-abertos-br,gov,wikipedia
```

Onde `siglaUf` refere-se a unidade federativa desejada.

### Unidades federativas (IBGE)

Retorna as unidades federativas do Brasil

```
https://brasilapi.com.br/api/ibge/uf/v1
```

## 📁 Arquivos

O arquivo **[tables.py](https://github.com/zirtaebea/corretoras-brasil/blob/main/tables.py)** possui o caminho de extração, tratamento e armazenamento dos dados em .csv e em um banco de dados (corretoras-brasil.db).

O arquivo **[functions.py](https://github.com/zirtaebea/corretoras-brasil/blob/main/functions.py)** possui as funções que serão implementadas dentro do arquivo principal de tabelas e funções de notificação em caso de erro de execução de alguma API.

### Importando bibliotecas

Você pode conferir quais bibliotecas e suas respectivas versões utilizadas na elaboração do projeto acessando [requirements.txt](https://github.com/zirtaebea/corretoras-brasil/blob/main/requirements.txt).

## ⚙️ Estrutura e execução

O processo de recebimento dos dados, tratamento e armazenamento está dividido da seguinte forma no arquivo **tables.py**:

1. Acessando dados das APIs
2. Salvando dados brutos em .csv
3. Tratamento de dados
4. Salvando bases tratadas em .csv
5. Armazenamento dos dados tratados em um banco de dados relacional

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

### Consulta de tabelas

Para consultar as tabelas criadas você pode utilizar a seguinte função **tabelas_bd()**.

Para consultar uma tabela em específico você pode utilizar a seguinte função **carrega_bd()**.

