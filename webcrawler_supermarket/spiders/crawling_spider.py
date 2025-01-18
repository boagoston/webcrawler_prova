from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "crawling_compra_agora"
    allowed_domains = ["www.compra-agora.com"]
    start_urls = ["https://www.compra-agora.com/"]

    rules = (
        # LinkExtractor para categorias principais, o regex está buscando URLs que seguem este formato: /loja/{categoria}/{id}
        Rule(LinkExtractor(allow=r'/loja/([^/]+)/\d+$'), callback='parse_categoria', follow=True),
    )

    def parse_categoria(self, response):

        # Exibindo o nome da categoria e a URL
        yield {
            'url': response.url
        }