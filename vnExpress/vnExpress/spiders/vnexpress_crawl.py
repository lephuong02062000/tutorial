import scrapy
from datetime import datetime
import json
OUTPUT_FILENAME = 'D:/PycharmProjects/VnExpress/tutorial/vnExpress/vnExpress/spiders/Output/vnexpress/vnexpress{}.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
class VnexpressCrawlSpider(scrapy.Spider):
    name = 'vnexpress_crawl'
    allowed_domains = ['vnexpress.net']
    start_urls = [
        'https://vnexpress.net/thoi-su',
        'https://vnexpress.net/the-gioi',
        'https://vnexpress.net/kinh-doanh',
        'https://vnexpress.net/giai-tri',
        'https://vnexpress.net/the-thao',
        'https://vnexpress.net/phap-luat',
        'https://vnexpress.net/giao-duc',
        'https://vnexpress.net/suc-khoe',
        'https://vnexpress.net/doi-song',
        'https://vnexpress.net/du-lich',
        'https://vnexpress.net/khoa-hoc',
        'https://vnexpress.net/so-hoa',
        'https://vnexpress.net/oto-xe-may',
        'https://vnexpress.net/y-kien',
        'https://vnexpress.net/tam-su',
        'https://vnexpress.net/hai'
    ]
    CRAWLED_COUNT = 0
    def parse(self, response):
        links_article = response.css('h3.title-news a::attr(href)').getall()
        for link_article in links_article:
            yield scrapy.Request(link_article, callback=self.get)
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def get(self, response):
        if response.status == 200 and response.css('meta[name="tt_page_type"]::attr("content")').get() == 'article':
            print('Crawling from:', response.url)
            data = {
                'title' : response.css('h1.title-detail::text').get(),
                'category' : response.css('ul.breadcrumb li a::text').get(),
                'update' : response.css('span.date::text').get(),

                'link_article' : response.url,

                'description' : response.css('p.description::text').get(),
                'content': '\n'.join([
                    ''.join(c.css('*::text').getall())
                    for c in response.css('article.fck_detail p.Normal')
                ]),

                'image_link' : response.css('div.fig-picture img::attr(data-src)').get(),

                'image_description' : response.css('div.fig-picture img::attr(alt)').get(),

                'author' : response.css('p.author_mail strong::text').get(),

                'keywords': [
                    k.strip() for k in response.css('meta[name="keywords"]::attr("content")').get().split(',')
                ],
                'tags': [
                    k.strip() for k in response.css('meta[name="its_tag"]::attr("content")').get().split(',')
                ],

        }
            with open(OUTPUT_FILENAME, 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.CRAWLED_COUNT += 1
                self.crawler.stats.set_value('CRAWLED_COUNT', self.CRAWLED_COUNT)
                print('SUCCESS:', response.url)

















