from string import ascii_letters
import unicodedata
import re
#import math

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

def delete_accents(s):
    return ''.join(c for c in s
        if c in ascii_letters)

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')

class MWCrawlSpider(CrawlSpider):
    name = "mw_crawl"

    allowed_domains = [
        "borsonline.hu","vg.hu","origo.hu"
        "szon.hu","veol.hu","zaol.hu","kemma.hu",
        "baon.hu","beol.hu","bama.hu","delmagyar.hu",
        "nool.hu","boon.hu","haon.hu","feol.hu",
        "duol.hu","heol.hu","kisalfold.hu",
    ]

    start_urls = []

    tag = ""

    rules = []

    def __init__(self, url, tag, *a, **kw):
        super().__init__(*a, **kw)
        self.start_urls.append(f"https://{url}/cimke/{tag}")
        self.tag = tag
        self.rules.append(Rule(LinkExtractor(allow=(f"/cimke/{tag}",), deny=(r"/[\d]+/[\d]+/", "/szerzo/"))))
        self.rules.append(Rule(LinkExtractor(allow=(r"/[\d]+/[\d]+/",), deny=("/cimke/", "/szerzo/") ), callback="parse"))
        self._compile_rules()

    def parse_start_url(self, response, **kwargs):
        clist = response.css("div.result-count-container").css("*::text").getall()
        yield response.follow(f"{self.start_urls[0]}?page={0}")
        yield response.follow(f"{self.start_urls[0]}?page={1}")
        if clist:
            filt = clist[1]
            reg = re.compile(r"[\d]+")
            num = reg.findall(filt)[0]
            num = int(num)
            num = (num // 10) + 2
            #num = math.floor(num / 10) + 2
            for i in range(2, num):
                yield response.follow(f"{self.start_urls[0]}?page={i}")



    def parse(self, response, **kwargs):
        requests = ["section.article", "section.article-page"]
        head_text=''
        for rq in requests:
            head = response.css(f"{rq}")
            h1 = head.css("h1::text").get()
            if h1 is not None:
                head_text += h1 + " "
                tags_rqs = ["div.tags-block", "div.tags", "div.article-tag-wrapper", "div.article-tags"]
                tags_text = ""
                for trq in tags_rqs:
                    tags_list = head.css(f"{trq}").css("a::text").getall()
                    if tags_list:
                        for e in tags_list:
                            tag = str.casefold(e)
                            tag = str.replace(tag,' ','-')
                            tag_s = strip_accents(tag)
                            tag_d = delete_accents(tag)
                            tags_text += (tag_s + " " + tag_d + " ")
        print(tags_text)

        lead_rqs = ["p.lead", "div.article-page-lead"]
        lead_text=''
        for rq in lead_rqs:
            lead_list = response.css(f"{rq}").css("*::text").getall()
            for e in lead_list:
                lead_text += e + ' '

        body = response.css("div.block-content")
        body_list = body.css("*::text").getall()
        body_text = ""
        if lead_text is not None:
            body_text += lead_text + "\n"
        for e in body_list:
            body_text += (e + " ")
        if self.tag in tags_text:
            yield {
                    "title": head_text,
                    "body": body_text,
                    "site": self.start_urls[0]
            }
        else:
            
            yield {}
