import scrapy
import json
from securitites.items import SecurititesItem
from decimal import Decimal

class SecuriSpider(scrapy.Spider):
    name = 'securi'
    allowed_domains = ['finance.ifeng.com']
    start_urls = ["http://app.finance.ifeng.com/list/stock.php?t=ha","http://app.finance.ifeng.com/list/stock.php?t=sa","http://app.finance.ifeng.com/list/stock.php?t=hb","http://app.finance.ifeng.com/list/stock.php?t=sb","http://app.finance.ifeng.com/list/stock.php?t=zxb","http://app.finance.ifeng.com/list/stock.php?t=cyb"]
    # start_urls = ["http://app.finance.ifeng.com/list/stock.php?t=ha"]
    hrefList = ["http://app.finance.ifeng.com/list/stock.php?t=ha", "http://app.finance.ifeng.com/list/stock.php?t=sa", "http://app.finance.ifeng.com/list/stock.php?t=hb",
                "http://app.finance.ifeng.com/list/stock.php?t=sb", "http://app.finance.ifeng.com/list/stock.php?t=zxb", "http://app.finance.ifeng.com/list/stock.php?t=cyb"]

    def parse(self, response):
        # for sel in response.xpath('//table/tr[position()>1 and position()<3]'):
        for sel in response.xpath('//table/tr[position()>1 and position()<'+str(len( response.xpath('//table/tr')))+']'):
            item = SecurititesItem()
            item['plate'] = response.css(
                '.block').xpath("h1[1]/text()").extract()[0]
            item["link"] = sel.xpath("td[1]/a/@href").extract()[0]
            item["uuid"] = int(sel.xpath("td[1]/a/text()").extract()[0])
            item["name"] = sel.xpath("td[2]/a/text()").extract()[0]
            item["nowPrice"] = float(
                sel.xpath("td[3]/span/text()").extract()[0])
            item["volume"] = sel.xpath("td[6]/text()").extract()[0]
            yield scrapy.Request(item["link"], meta={'item': item}, callback=self.parse_page_detail)
        lastLink = response.urljoin(response.xpath('//table/tr[last()]/td/a[last()]/@href').extract()[0])
        if lastLink in self.hrefList:
            pass
        else:
            self.hrefList.append(lastLink)
            yield scrapy.Request(lastLink, self.parse)

    def parse_page_detail(self,response):
        concept = []
        item = response.meta['item']
        item['code_mgsy'] = float(response.css('#caiwuzhaiyao').xpath('./li[1]//td[2]/text()').extract()[0])
        item['code_mgjzc'] = float(response.css('#caiwuzhaiyao').xpath('./li[2]//td[2]/text()').extract()[0])
        item['code_business'] = response.css('.lastBot').xpath('./span[1]/text()').extract()[0][5:]
        for sel in response.css('.lastBot').xpath('./span[2]/a'):
            concept.append(sel.xpath('./text()').extract()[0])
        item['code_concept'] = ','.join(concept)    
        tragetUrl = response.url.split('/')[-2]
        yield scrapy.Request('https://hq.finance.ifeng.com/q.php?l=' + tragetUrl, meta={'item': item}, callback=self.parse_num_detail)

    def parse_num_detail(self, response):
        item = response.meta['item']
        dataStr = bytes.decode(response.body)[11:-3]
        dataDir = json.loads(dataStr.replace("'", "\""))
        item['code_PE'] = float(Decimal(dataDir['sh' + str(item['uuid'])][0]/ item['code_mgsy']).quantize(Decimal('.001')))
        item['code_PB'] = float(Decimal(dataDir['sh' + str(item['uuid'])][0]/ item['code_mgjzc']).quantize(Decimal('.001')))
        return item