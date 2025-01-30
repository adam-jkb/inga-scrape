from string import ascii_letters
import unicodedata
import re
import math

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

def delete_accents(s):
    return ''.join(c for c in s
        if c in ascii_letters)

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')

class TelexCrawlSpider(CrawlSpider):
    name = "telex_crawl"

    custom_settings = {
        "DEPTH_LIMIT": 15
    }


    allowed_domains = [
        "telex.hu"
    ]

    start_urls = []

    tag = ""

    rules = []

    def __init__(self, tag, *a, **kw):
        super().__init__(*a, **kw)
        self.start_urls.append(f"https://telex.hu/rovat/{tag}")
        self.tag = tag
        self.rules.append(Rule(LinkExtractor(allow=(f"/rovat/{tag}",), deny=(r"/[\d]+/[\d]+/", "/szerzo/"))))
        self.rules.append(Rule(LinkExtractor(allow=(r"/[\d]+/[\d]+/",), deny=("/rovat/", "/szerzo/") ), callback="parse"))
        self._compile_rules()


    def parse(self, response, **kwargs):
        requests = ["section.article", "section.article-page", "div.title-section"]
        head_text=''
        tags_text = ''
        for rq in requests:
            head = response.css(f"{rq}")
            h1 = head.css("h1::text").get()
            if h1 is not None:
                head_text += h1 + " "
                tags_rqs = ["div.tags-block", "div.tags", "div.article-tag-wrapper", "div.article-tags", "div.title-section__tags"]
                for trq in tags_rqs:
                    tags_list = head.css(f"{trq}").css("a::text").getall()
                    if tags_list:
                        for e in tags_list:
                            tag = str.casefold(e)
                            tag = str.replace(tag,' ','-')
                            tag_s = strip_accents(tag)
                            tag_d = delete_accents(tag)
                            tags_text += (tag_s + " " + tag_d + " ")

        lead_rqs = ["p.lead", "div.article-page-lead", "p.article__lead"]
        lead_text=''
        for rq in lead_rqs:
            lead_list = response.css(f"{rq}").css("*::text").getall()
            for e in lead_list:
                lead_text += e + ' '

        body_rqs = ["div.block-content", "div.article-html-content"]
        for rq in body_rqs:
            body_list = response.css(f"{rq}").css("*::text").getall()
            body_text = ""
            if body_list:
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
