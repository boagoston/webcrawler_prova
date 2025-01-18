from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging

class CrawlingSpider(CrawlSpider):
    name = "crawling_compra_agora"
    allowed_domains = ["www.compra-agora.com"]
    start_urls = ["https://www.compra-agora.com/"]

    rules = (
        # LinkExtractor para categorias principais. O regex está buscando URLs que seguem este formato: /loja/{categoria}/{id}
        # É possível fazer o recorte das URLs por regex utilizando o LinkExtractor, mas é importante ter cuidado para não capturar URLs indesejadas
        # alem disso, legibilidade do codigo é comprometida

        #Rule(LinkExtractor(allow=r'/loja/([^/]+)/\d+$'), callback='parse_categoria', follow=True),
    )


    def parse_categoria(self, response):

        hover_menu_items = response.css("ul.hover-menu > li.lista-menu-itens")
        
        for item in hover_menu_items:
            url = item.css("a::attr(href)").get(default="").strip()
            logging.info(f"URL extraída: {url}")

            if url:
                logging.info(f"URL: {url}")
                yield {
                    'url': url,
                }
