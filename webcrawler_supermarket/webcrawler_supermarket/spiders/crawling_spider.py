import logging
import scrapy

class CrawlingSpider(scrapy.Spider):
    name = "crawling_compra"
    allowed_domains = ["www.compra-agora.com"]
    start_urls = ["https://www.compra-agora.com/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.output_file = "processed_urls.txt"  # Nome do arquivo onde as URLs serão salvas

        # Cria ou limpa o arquivo no início
        with open(self.output_file, "w") as f:
            f.write("")


    def start_requests(self):
        yield scrapy.Request(
            url="https://www.compra-agora.com/",
            callback=self.parse,
        )

    def parse(self, response):
        categorias = self.get_categories(response)
        logging.debug(f"Categorias encontradas: {categorias}")
        for categoria in categorias:
            categoria_url = categoria['url']
            categoria_api_url = categoria_url.replace("/loja/", "/api/catalogproducts/")
            yield scrapy.Request(
                url=response.urljoin(categoria_api_url),
                callback=self.parse_produtos,
                meta={'categoria_texto': categoria['texto']}
            )

    def get_categories(self, response):
        categorias = []
        hover_menu_items = response.css("ul.hover-menu > li.lista-menu-itens")
        for item in hover_menu_items:
            url = item.css("a::attr(href)").get(default="").strip()
            text = ''.join(item.css("a *::text").getall()).strip()
            if url:
                categorias.append({'texto': text, 'url': url})
        return categorias

    def parse_produtos(self, response):
        try:
            paginas_total = response.json().get('paginacao', {}).get('PaginasTotal', 1)
        except ValueError:
            logging.error("Erro ao tentar decodificar a resposta JSON.")
            return

        categoria_texto = response.meta.get('categoria_texto', 'Desconhecido')
        logging.info(f"Extraindo produtos da categoria: {categoria_texto}")

        for pagina in range(1, paginas_total + 1):
            pagina_url = f"{response.url}?p={pagina}"
            yield scrapy.Request(
                url=pagina_url,
                callback=self.parse_produtos_pagina,
                meta={'categoria_texto': categoria_texto, 'pagina_url': pagina_url}
            )

    def parse_produtos_pagina(self, response):
        pagina_url = response.meta.get('pagina_url')

        self.save_processed_url(pagina_url)

        produtos = response.json().get('produtos', [])
        logging.debug(f"Produtos encontrados nesta página: {len(produtos)}")

        for produto in produtos:
            nome = produto.get('Nome', '').strip()
            marca = produto.get('Marca', '').strip()
            foto = produto.get('Foto', '')
            imagem_url = f"https://images-unilever.ifcshop.com.br/produto/{foto}"

            logging.info(f"Produto encontrado: {nome} - {marca} - {imagem_url}")

            if nome or marca or imagem_url:
                yield {
                    'nome': nome,
                    'marca': marca,
                    'imagem_url': imagem_url
                }
            else:
                logging.warning(f"Produto não extraído corretamente: {produto}")

    def save_processed_url(self, url):
        """Salva a URL processada em um arquivo de texto."""
        with open(self.output_file, "a") as f:
            f.write(url + "\n")
        logging.info(f"URL salva: {url}")
