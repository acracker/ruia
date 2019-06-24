#!/usr/bin/env python

from ruia import AttrField, Item, Request, Spider, TextField


class DoubanItem(Item):
    target_item = TextField(css_select='div.item')
    title = TextField(css_select='span.title')
    cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq')

    async def clean_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


class DoubanSpider(Spider):
    start_urls = ['https://movie.douban.com/top250']
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 10

    # proxy config
    # kwargs = {"proxy": "http://0.0.0.0:8118"}
    kwargs = {}

    def __init__(self, middleware=None, loop=None, is_async_start=False):
        super().__init__(middleware, loop, is_async_start)
        self.data = []

    async def parse(self, res):
        etree = res.html_etree
        pages = ['?start=0&filter='] + [i.get('href') for i in etree.cssselect('.paginator>a')]
        for index, page in enumerate(pages):
            url = self.start_urls[0] + page
            yield Request(
                url,
                callback=self.parse_item,
                meta={'index': index},
                request_config=self.request_config,
                **self.kwargs
            )

    async def parse_item(self, res):
        items_data = await DoubanItem.get_items(html=res.text)
        for item in items_data:
            print(item.title)
            self.data.append(item.title)


async def before_stop(spider):
    return 1


async def after_start(spider):
    return 1


async def main():
    await DoubanSpider.async_start(before_stop=before_stop, after_start=after_start)


if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())
    # DoubanSpider.start()

