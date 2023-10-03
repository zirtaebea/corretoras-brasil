import requests
from plyer import notification

# verificador de apis
def verificar_api(url, nome_api, lista):
    resp = requests.get(url)
    if resp.status_code !=200: 
        lista.append(nome_api)
        
# notify de erro caso a api não esteja disponível
def api_indisponivel(lista):
    if lista: 
        message = f'Não foi possível acessar as seguintes APIs: {", ".join(lista)}'
    notification.notify(
        title='APIs Indisponíveis',
        message=message,
        timeout=15
    )
    
