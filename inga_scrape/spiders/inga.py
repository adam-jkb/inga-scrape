#from string import ascii_letters
#import unicodedata
import re
#import math

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

#def delete_accents(s):
#    return ''.join(c for c in s
#        if c in ascii_letters)

#def strip_accents(s):
#    return ''.join(c for c in unicodedata.normalize('NFD', s)
#        if unicodedata.category(c) != 'Mn')

class IngaCrawlSpider(CrawlSpider):
    name = "inga_crawl"

    allowed_domains = [
            "ingatlan.com",
    ]

    re_categories = (
            'lakas', 'haz', 'telek', 'garazs', 'nyaralo',
            'iroda', 'uzlethelyseg', 'vendeglatas', 'raktar', 'ipari',
            'mezogazdasagi', 'fejl-terulet', 'intezmeny'
    )

    sale_categories = ('elado', 'kiado')

    #kurva sok van ugyhogy itt nem validalok meg
    #sub_categories = ('uj-epitesu', 'van-szigeteles', ...

    # https://ingatlan.com/sale_category+re_category+sub_categories?page=n
    # van mukodo cloudflare captcha, de az alap oldal elmegy js nelkul is
    # miutan seteli a captcha kitoltese utan a sutiket onnantol jo, de addigis tudnia kell js-t
    # VAGY kezzel felmegyunk, kitoltjuk a captchat es atmasoljuk a kapott sutiket ide
    # es ugyanarra seteljuk a user agentet itt mint a browserban
    start_urls = []

    rules = []

    def __init__(self, re_cat="", sale_cat="", sub_cats="", *a, **kw):
        super().__init__(*a, **kw)
        #validation off for testing
        #if re_cat not in self.re_categories or sale_cat not in self.sale_categories:
            #raise Exception("category not found")
        self.start_urls.append(f"https://ingatlan.com/lista/{sale_cat}+{re_cat}+{sub_cats}")
        self.rules.append(Rule(LinkExtractor(allow=(f"/lista/{sale_cat}+{re_cat}",))))
        self.rules.append(Rule(LinkExtractor(allow=(r"/[\d]+",), deny=("/lista/",) ), callback="parse"))
        self._compile_rules()

    def parse(self, response, **kwargs):
        print(response.css("div.card::text").getall())
        #inherited sample code
        '''
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
        '''
        yield{}
