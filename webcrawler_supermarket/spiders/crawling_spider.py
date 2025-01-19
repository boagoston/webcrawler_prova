from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
import scrapy

class CrawlingSpider(scrapy.Spider):
    name = "crawling_compra_agora"
    allowed_domains = ["www.compra-agora.com"]
    start_urls = ["https://www.compra-agora.com/"]

    rules = (
        # LinkExtractor para categorias principais. O regex está buscando URLs que seguem este formato: /loja/{categoria}/{id}
        # É possível fazer o recorte das URLs por regex utilizando o LinkExtractor, mas é importante ter cuidado para não capturar URLs indesejadas
        # alem disso, legibilidade do codigo é comprometida

        #Rule(LinkExtractor(allow=r'/loja/([^/]+)/\d+$'), callback='parse_categoria', follow=True),
    )


    def parse(self, response):
        categorias = self.get_categories(response)
        for categoria in categorias:
            # Certifique-se de que a URL completa seja usada
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
        produtos = response.css('li.shelf-item')
        for produto in produtos:
            yield {
                'nome': produto.css('a.produto-nome::text').get(),
                'marca': produto.css('a.produto-marca::text').get(),
                'imagem': produto.css('img::attr(src)').get(),
            }