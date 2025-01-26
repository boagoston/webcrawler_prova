from scrapy.spiders import CrawlSpider, Rule
import logging
import scrapy
import os
from dotenv import load_dotenv
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder


class CrawlingSpider(scrapy.Spider):
    name = "crawling_compra_agora"
    allowed_domains = ["www.compra-agora.com"]
    start_urls = ["https://www.compra-agora.com/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        load_dotenv()
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
                
        if not self.username or not self.password:
            raise ValueError("As variáveis de ambiente USERNAME e PASSWORD não foram definidas!")

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.compra-agora.com/",
            callback=self.parse,
        )

    # def get_login_page(self, response):
    #     data = {
    #         "usuarioCnpj": self.username,
    #         "usuarioSenhaCA": self.password
    #     }
    #     logging.info(f"data: {data}" )

        

    #     yield scrapy.FormRequest(
    #         url="https://www.compra-agora.com/cliente/logar",
    #         formdata={"data": data},
    #         headers={
    #             "Content-Type": "application/x-www-form-urlencoded",
    #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    #         },
    #         callback=self.after_login,
    #     )

    # def after_login(self, response):
    #     json_response = response.json()

    #     if json_response.get("success"):
    #         logging.info("Login realizado com sucesso!")
    #         user_id = json_response.get("user_id")
    #         user_type = json_response.get("user_type")
    #         logging.info(f"ID do usuário: {user_id}, Tipo: {user_type}")

    #         # Depois de logado, agora realiza a extração das categorias
    #         yield scrapy.Request(
    #             url="https://www.compra-agora.com/", 
    #             callback=self.parse
    #         )
    #     else:
    #         logging.error(f"Resposta do login: {json_response}")
    #         logging.error("Falha no login")

    def parse(self, response):
        # Extração das categorias
        categorias = self.get_categories(response)
        logging.info(f"Categorias encontradas: {categorias}")
        for categoria in categorias:
            categoria_url = response.urljoin(categoria['url'])
            yield response.follow(categoria_url, callback=self.parse_produtos)

    def get_categories(self, response):
        categorias = []
        hover_menu_items = response.css("ul.hover-menu > li.lista-menu-itens")
        for item in hover_menu_items:
            url = item.css("a::attr(href)").get(default="").strip()
            if url:
                categorias.append({'url': url})
        return categorias

    def parse_produtos(self, response):
        produtos = response.css('ul#shelf-content-items li.shelf-item')

        logging.info(f"HTML da página: {response.text[:1000]}")

        with open("pagina_produtos.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        logging.info(f"Produtos encontrados: {len(produtos)}")

        for produto in produtos:
            nome = produto.css('a.produto-nome::text').get(default="").strip()
            marca = produto.css('a.produto-marca::text').get(default="").strip()
            imagem = produto.css('img::attr(src)').get(default="").strip()

            if nome or marca or imagem:
                yield {
                    'nome': nome,
                    'marca': marca,
                    'imagem': imagem,
                }
            else:
                logging.warning(f"Produto não extraído corretamente: {produto.get()}")

