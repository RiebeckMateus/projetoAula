import scrapy
import csv

# atualização novamente no branch principal (foi nomeado de master pelo VSC)

class Magalu(scrapy.Spider):
    name = 'm'
    custom_settings = {
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    
    def start_requests(self):
        yield scrapy.Request(f'https://www.magazineluiza.com.br/eletrodomesticos/l/ed/')
    
    def parse(self, response):
        total = response.xpath('//button[@type="next"]//ancestor::ul//li[position() = last() -1]//text()').get()
        for i in range(1, int(total) + 1):
            yield scrapy.Request(f'https://www.magazineluiza.com.br/eletrodomesticos/l/ed/?page={i}', callback=self.parse2)
            
    def parse2(self, response):
        blocos = response.xpath('//div[@data-testid="product-list"]//li')
        for bloco in blocos:
            title = bloco.xpath('.//h2[@data-testid="product-title"]//text()').get()
            price = bloco.xpath('.//p[@data-testid="price-value"]//text()').get()
            yield{
                'title' : title,
                'price' : price
            }