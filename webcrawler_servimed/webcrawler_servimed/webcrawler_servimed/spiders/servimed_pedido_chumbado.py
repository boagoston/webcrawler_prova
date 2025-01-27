import scrapy
import json
import uuid
import sys
import os
from dotenv import load_dotenv

class ServimedPedidoSpider(scrapy.Spider):
    def __init__(self, pedido_numero=None, *args, **kwargs):
        super(ServimedPedidoSpider, self).__init__(*args, **kwargs)
        if not pedido_numero:
            print("Uso: python seumodulo.py <número_do_pedido>")
            sys.exit(1)
        self.pedido_numero = pedido_numero
        self.generated_uuid = str(uuid.uuid1())
    
    
    
    name = 'servimed_pedido'

    load_dotenv()
    accesstoken = os.getenv('ACCESS_TOKEN')
    cookies = os.getenv('COOKIES')

    print(f"accesstoken: {accesstoken}")
    print(f"cookies: {cookies}")
    
    
    
    def start_requests(self):
        url = f'https://peapi.servimed.com.br/api/Pedido/ObterTodasInformacoesPedidoPendentePorId/{self.pedido_numero}'
        self.log("Procurando pedido...")
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'pt-BR,pt;q=0.8',
            'accesstoken': self.accesstoken,
            'content-type': 'application/json',
            'contenttype': 'application/json',
            'cookie': self.cookies,
            'loggeduser': '22850',
            'origin': 'https://pedidoeletronico.servimed.com.br',
            'priority': 'u=1, i',
            'referer': 'https://pedidoeletronico.servimed.com.br/',
            'sec-ch-ua': '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        }

        yield scrapy.Request(
            url=url,
            method='GET',
            headers=headers,
            callback=self.parse_response
        )

    def parse_response(self, response):
        data = json.loads(response.text)

        if response.status == 200:
            if not data.get('itens'):
                yield {"mensagem": f"Pedido {self.pedido_numero} não encontrado."}
                self.salvar_json({"ERRO": "PEDIDO_NAO_ENCONTRADO"})
            else:
                self.log(f"Pedido {self.pedido_numero} encontrado.")
                
                rejeicao = data.get('rejeicao', None)
                if rejeicao is None:
                    rejeicao = data.get('pedidoStatusId', "Desconhecido")
                
                rejeicao = str(rejeicao).strip()
                self.log(f"Situação: {rejeicao}")

                itens = []

                for item in data.get('itens', []):
                    produto = item.get('produto', {})
                    produto_id = produto.get('id', None)
                    descricao = produto.get('descricao', None)
                    quantidade_faturada = item.get('quantidadeFaturada', 0)

                    itens.append({
                        'codigo_produto': produto_id,
                        'descricao': descricao,
                        'quantidade_faturada': quantidade_faturada
                    })
                
                json_data = {
                    'motivo': rejeicao,
                    'itens': itens
                }

                self.salvar_json(json_data)

                yield {
                    'motivo': rejeicao,
                    'itens': itens
                }

        else:
            self.log(f"Request failed with status: {response.status}")

    def salvar_json(self, data):
        if not os.path.exists('pedidos'):
            os.makedirs('pedidos')

        output_file = os.path.join('pedidos', f"pedido_{self.pedido_numero}.json")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
