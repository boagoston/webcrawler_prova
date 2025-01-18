from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "crawling_compra_agora"
    allowed_domains = ["www.compra-agora.com"]
    start_urls = ["https://www.compra-agora.com/"]

    rules = (
        # LinkExtractor para categorias principais (ignorando subcategorias)
        Rule(LinkExtractor(allow=r'/loja/([^/]+)/\d+$'), callback='parse_categoria', follow=True),
    )

    def parse_categoria(self, response):
        # Extração do nome da categoria (ajuste conforme necessário)
        categoria = response.xpath("//h1[contains(@class, 'titulo-categoria')]//text()").get()

        # Exibindo o nome da categoria e a URL
        yield {
            'url': response.url
        }