# -*- coding: utf-8 -*-

import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy.selector import Selector

from CookBot.items import CookpadRecipe, Ingredient


class CookpadSpider(CrawlSpider):
    name = 'cookpad'
    allowed_domains = ['cookpad.com']
    download_delay = 1

    start_urls = [
        # きょうの料理
        'https://cookpad.com/search/%E6%8A%B9%E8%8C%B6',   # 抹茶
        
    ]
    rules = (
        # Follow pagination
        Rule(LinkExtractor(allow=(r'/search/%E6%8A%B9%E8%8C%B6\?page=\d+',)), follow=True),

        # Extract recipes
        Rule(LinkExtractor(allow=(r'recipe/\d+',)), callback='parse_recipe')
    )

    def parse_recipe(self, response):
        hxs = Selector(response)
        recipe = CookpadRecipe()

        # id
        recipe['id'] = int(re.findall(r'recipe/(\d+)', response.url)[0])

        # name
        recipe['name'] = hxs.xpath("//div[@id='recipe-title']/h1/text()")[0] \
                            .extract().strip()

        # author
        recipe['author'] = int(
            hxs.xpath("//a[@id='recipe_author_name']/@href").re('(\d+)')[0]
        )

        # description
        recipe['description'] = ''.join(hxs.xpath("//div[@id='description']/div[@class='description_text']/text()") \
                                           .extract()).strip()

        # ingredients
        ingredients = []
        ingredient_basepath = ("//div[@id='ingredients']/div[@id='ingredients_list']/div[@class='ingredient_row']")
        ingredient_nodes = hxs.xpath(ingredient_basepath)
        for ingredient_node in ingredient_nodes:
            try:
                if ingredient_node.xpath('div/span/a'):
                    # keyword ingredient
                    name = ingredient_node.xpath('div[1]/span/a/text()').extract()[0].strip()
                else:
                    # normal ingredient
                    name = ingredient_node.xpath('div[1]/span/text()').extract()[0].strip()
                quantity = ingredient_node.xpath('div[2]/text()').extract()[0].strip()
            except:
                continue

            ingredient = Ingredient()
            ingredient['name'] = name
            ingredient['quantity'] = quantity
            ingredients.append(ingredient)
        recipe['ingredients'] = ingredients

        # instructions
        tempInstruction = hxs.xpath(
            "//dd[@class='instruction']/p/text()"
        ).extract()
        
        recipe['instructions'] = [s.strip() for s in tempInstruction];
        # report count
        try:
            recipe['report_count'] = int(
                ''.join(hxs.xpath("//li[@id='tsukurepo_tab']/a/span/text()").re('(\d+)'))
            )
        except:
            recipe['report_count'] = 0

        # published date
        recipe['published_date'] = hxs.xpath(
            "//div[@id='recipe_id_and_published_date']/span[2]/text()").re('\d{2}/\d{2}/\d{2}')[0]

        # udpated date
        recipe['updated_date'] = hxs.xpath(
            "//div[@id='recipe_id_and_published_date']/span[3]/text()").re('\d{2}/\d{2}/\d{2}')[0]

        return recipe