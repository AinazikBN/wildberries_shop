from typing import Any
import requests
from django.core.management import BaseCommand
from parsing.parser_1 import ParserWB
from shop.models import Product, Category
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

class Command(BaseCommand):
    help = 'Run the Wildberries parser'

    def handle(self, *args: Any, **options):
        self.stdout.write(self.style.SUCCESS('Starting the Wildberries'))
        try:
            count = 1
            parser = ParserWB(
                'https://www.wildberries.ru/catalog/208331798/detail.aspx'
            ).parse()
            for product_info in parser.products:
                for size in product_info.sizes:
                    slug = Product.generate_slug(product_info.name)
                    image_links = product_info.image_links.split(';')
                    if image_links:
                        image_url = image_links[0]
                        img_name = f'{slug}-main.jpg'
                        response = requests.get(image_url)
                        response.raise_for_status()
                        img_temp = NamedTemporaryFile()
                        img_temp.write(response.content)
                        img_temp.flush()

                        category = Category.objects.get(id=4)
                        db_product = Product.objects.create(
                            category=category, 
                            title=product_info.name, 
                            brand=product_info.brand, 
                            description='', 
                            price=size.price.total, 

                        )
                        db_product.image.save(img_name, File(img_temp), save=True)
                        self.stdout.write(self.style.SUCCESS(f'PARSER compeleted {count}'))
                        count += 1 
                        if count > 30:
                            break 

            self.stdout.write(self.style.SUCCESS('Parser completed successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))




