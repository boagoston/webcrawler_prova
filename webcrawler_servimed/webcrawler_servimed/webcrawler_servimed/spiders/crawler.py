import scrapy
import json
import uuid
import sys

class crawlerServimed(scrapy.Spider):
    name = 'crawler_servimed'
    start_urls = ['https://peapi.servimed.com.br/api/usuario/login']

    def __init__(self, pedido_numero=None, *args, **kwargs):
        super(crawlerServimed, self).__init__(*args, **kwargs)
        if not pedido_numero:
            print("Uso: python seumodulo.py <número_do_pedido>")
            sys.exit(1)
        self.pedido_numero = pedido_numero  
        self.generated_uuid = str(uuid.uuid1())
        
    
    def start_requests(self):
        login_data = {
            "usuario": "juliano@farmaprevonline.com.br",
            "senha": "a007299A"
        }

        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accesstoken': self.generated_uuid,
            'cookie': '',
            'content-type': 'application/json',
            'contenttype': 'application/json',
            'accept-language': 'pt-BR,pt;q=0.8',
            'loggeduser': 0,
            'origin': 'https://pedidoeletronico.servimed.com.br',
            'connection': 'keep-alive',
            'priority': 'u=1,i',
            'referer': 'https://pedidoeletronico.servimed.com.br/',
            'sec-ch-ua': '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }


        yield scrapy.Request(
            url=self.start_urls[0],
            method='POST',
            headers=self.headers,
            body=json.dumps(login_data),
            callback=self.after_login
        )

    def after_login(self, response):
        if response.status != 200:
            self.log(f"Login failed with status: {response.status}")
            return

        cookies = response.headers.getlist('set-cookie')
        session_token = None
        access_token = None

        for cookie in cookies:
            cookie_str = cookie.decode('utf-8')  
            if "sessiontoken=" in cookie_str:
                session_token = cookie_str.split(';')[0].split('=')[1]  # Extrai o valor do sessiontoken
            if "accesstoken=" in cookie_str:
                access_token = cookie_str.split(';')[0].split('=')[1]  # Extrai o valor do accesstoken

        if session_token and access_token:
            print(f'Session Token: {session_token}')
            print(f'Access Token: {access_token}')


            data = json.loads(response.text)

            codigo_usuario = data['usuario']['codigoUsuario']
            codigo_externo = data['usuario']['codigoExterno']
            users = data['usuario']['users']

            
            self.headers['loggeduser'] = str(codigo_usuario)
            
            
            self.headers['cookie'] = f"sessiontoken={session_token}; accesstoken={access_token}"

            
            body = {
                "codigoExterno": codigo_externo,
                "codigoUsuario": codigo_usuario,
                "dataFim": "",
                "dataInicio": "",
                "filtro": self.pedido_numero,
                "kindSeller": 0,
                "pagina": 1,
                "registrosPorPagina": 10,
                "users": users
            }

            print(f'Body: {body}')
            print(f'Headers: {self.headers}')

            # Enviar a requisição POST com os dados do pedido
            yield scrapy.Request(
                url=f'https://peapi.servimed.com.br/api/Pedido/ObterTodasInformacoesPedidoPendentePorId/{self.pedido_numero}',
                method='GET',
                headers=self.headers,
                body=json.dumps(body),
                callback=self.parse_pedidos
            )
        else:
            print('Tokens não encontrados.')

    def parse_pedidos(self, response):
        # Imprimindo todos os detalhes da resposta (status, headers, e corpo)
        self.log(f"Response Status Code: {response.status}", level=scrapy.log.DEBUG)
        self.log(f"Response Headers: {response.headers}", level=scrapy.log.DEBUG)
        self.log(f"Response Body: {response.text}", level=scrapy.log.DEBUG)

        # Verificando se a resposta foi bem-sucedida
        if response.status == 200:
            data = json.loads(response.text)
            self.log(f"Data received: {data}")
        else:
            self.log(f"Request failed with status: {response.status}")
            print(f"Response Status: {response.status}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Body: {response.text}")
