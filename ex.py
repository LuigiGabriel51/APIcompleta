import requests

url_servicos = "http://127.0.0.1:5000/listaDeServicos"

servicos = requests.get(url_servicos)
print(servicos)