#!/bin/sh


scrapy crawl telex_crawl -a url=www.telex.hu -a tag=kulfold &
scrapy crawl telex_crawl -a url=www.telex.hu -a tag=belfold&
#scrapy crawl mw_crawl -a url=www.szon.hu -a tag=leny
scrapy crawl mw_crawl -a url=www.borsonline.hu -a tag=tolvai-reni&
scrapy crawl mw_crawl -a url=www.borsonline.hu -a tag=veszely&

wait
cp -f out.jsonl ../out.jsonl
