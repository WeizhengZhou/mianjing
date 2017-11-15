
# -*- coding: utf-8 -*-
import scrapy
import time
import logging


MAX_PAGE = 10
COMPANY = 'credit karma'
SEARCH_TERM = '面'
FILE_NAME = COMPANY.replace(' ', '_') + '.txt'
URL = 'https://www.google.com/search?q=%s+%s+site:www.1point3acres.com&start=%d'


class PointSpider(scrapy.Spider):

  name = "point"

  def __init__(self):
    self.id = 0
    with open(FILE_NAME, 'w') as f:
      f.write('')

  def start_requests(self):
    for page in range(MAX_PAGE):
      url = URL % (COMPANY, SEARCH_TERM, page * 10)
      yield scrapy.Request(url=url, callback=self.parseSearch)

  def parseSearch(self, response):
    for i in range(1, 11):
      title = response.xpath('//*[@id="rso"]/div/div/div[%d]/div/div/h3/a/text()' % i).extract_first()
      link = response.xpath('//*[@id="rso"]/div/div/div[%d]/div/div/h3/a/@href' % i).extract_first()
      time.sleep(2)
      yield scrapy.Request(url=link, callback=self.parsePoint)

  def parsePoint(self, response):
    content = ''.join(
        response
        .xpath('//td[contains(@id, "postmessage")]')[0]
        .xpath('.//descendant-or-self::*[not(self::font)]/text()').extract()
    )
    content.strip()
    content = content[60:] # Remove dummy content.
    content = content.encode('utf8')


    publish_date = response.xpath('//*[contains(@id, "authorposton")]/text()').extract_first()
    publish_date = publish_date.encode('utf8')

    with open(FILE_NAME, 'a+') as f:
      f.write('-*' * 80 + '\n')
      f.write(publish_date + '\n')
      f.write('Id:' + str(self.id))
      self.id += 1
      f.write(response.request.url + '\n')
      f.write(content)
      f.write('\n')

  def spider_closed(self, spider):
    f = open(FILE_NAME)
    data = f.read()
    post_list = data.split('-*' * 80)[1:]


    post_by_date = {}
    for post in post_list:
      publish_date = re.search(r'\d{4}-\d+-\d+', post).group()
      if not post_by_date.get(publish_date):
        post_by_date[publish_date] = []
      post_by_date[publish_date].append(post)

    publish_dates = sorted(post_by_date.keys(), reverse=True)


    with open(FILE_NAME, 'w+') as f:
      f.write('')

    with open(FILE_NAME, 'a+') as f:
      for publish_date in publish_dates:
        for post in post_by_date[publish_date]:
          f.write('-*' * 80 + '\n')
          f.write(post)



