import scrapy
import datetime
from newsFeeds.items import NewsfeedsItem
from scrapy.http import HtmlResponse
from scrapy.mail import MailSender
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from scrapy.conf import settings
import pymongo


class newsSpider(scrapy.Spider):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MANGODB_PORT']
        db_name = settings['MANGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        self.post = db[settings['MONGODB_DOCNAME']]

    name = "newsSpider"
    allowed_domains = ["cctv.com"]
    nowTime = datetime.datetime.now()
    nowTimeStr = '%s%s%s' % (nowTime.year, nowTime.month, nowTime.day)
    start_urls = [
        "http://tv.cctv.com/lm/xwlb/day/%s.shtml" % nowTimeStr
        # "http://tv.cctv.com/lm/xwlb/day/20171109.shtml"
    ]
    itemPull = []
    htmlStr = ''
    htxs = ''

    def parse(self, response):
        htxs = HtmlResponse(url="", body=response.body.decode(
            'utf-8'), encoding='utf-8')
        self.htmlStr = response.body.decode('utf-8')
        for sel in htxs.xpath('//ul/li'):
            item = NewsfeedsItem()
            item['newsTime'] = self.nowTimeStr
            item['newsTime'] = sel.css('.title').xpath('./text()').extract()[0]
            item['link'] = sel.xpath('./a[1]/@href').extract()[0]
            yield item

    def close(self, reason):
        sel = self.post.find_one({"newsTime": self.nowTimeStr})
        if sel and len(sel['itemPull']) > 0:
            pass
        elif self.htmlStr.find('<ul>') > 0:
            self._sendMail('send')
            self.logger.info('发送邮件')
        else:
            self.logger.info('news not publish')

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def _sendMail(self, data):
        from_addr = 'zx625797912@163.com'
        password = 'zx625797912'
        to_addr = '625797912@qq.com'
        smtp_server = 'smtp.163.com'
        msg_body = '<html><body>%s</body></html>' % self.htmlStr
        msg = MIMEText(msg_body, 'html', 'utf-8')
        msg['From'] = self._format_addr('爬虫1号 <%s>' % from_addr)
        msg['To'] = self._format_addr('老大 <%s>' % to_addr)
        msg['Subject'] = Header('新闻联播摘要%s' % self.nowTimeStr, 'utf-8').encode()
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
