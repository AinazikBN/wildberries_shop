import requests
import re
from parsing.models import Items
import csv 

# response = requests.get(url="https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%80%D1%82%D0%B0")

class ParserWB:
    def __init__(self, url):
        self.seller_id = self.get_seller_id(url)

    def get_seller_id(self, url):
        item_id = self.get_item_id(url)
        params = {
            'appType': '1',
            'curr': 'rub',
            'dest': '286',
            'spp': '30',
            'nm': item_id,
        }
        response = requests.get(url=f'https://card.wb.ru/cards/v2/detail', params=params)
        seller_id = Items.model_validate(response.json()['data'])
        return seller_id.products[0].supplierId
    

    def get_item_id(self, url):
        regex = "(?<=catalog/).+(?=/detail)"
        item_id = re.search(regex, url)[0]
        return item_id
    
    def create_csv(self):
        with open('wb_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'название',"цена", "бренд", "рейтинг", 
                             "в наличии", "id продавца", "изображения"])
            
    def save_csv(self, items):
        with open('wb_data.csv', mode='a', newline="") as file:
            writer = csv.writer(file)
            for product in items.products:
                for size in product.sizes:
                    writer.writerow([product.id, 
                                    product.name, 
                                    size.price.total, 
                                    product.brand, 
                                    product.rating, 
                                    product.volume, 
                                    product.supplierId,
                                    product.image_links])
    
    # def save_to_db(self, items):
    #     session = SessionLocal()
    #     try:
    #         for product in items.products:
    #             for size in product.sizes:
    #                 db_product = Product(
    #                     name = product.name, 
    #                     price = size.price.total, 
    #                     brand = product.brand, 
    #                     rating = product.rating, 
    #                     volume = product.volume, 
    #                     supplier_id = product.supplierId, 
    #                     image_links = product.image_links
    #                     )
    #                 session.add(db_product)
    #         session.commit()
    #     except:
    #         print('Error save to db')
    #     finally:
    #         session.close()

            

    def parse(self):
        page = 1
        # self.create_csv()

        while True:
            params = {
                'appType': '1',
                'curr': 'rub',
                'dest': '286',
                'sort': 'popular',
                'spp': '30',
                'supplier': self.seller_id,
                'page': page,
            }
            response = requests.get('https://catalog.wb.ru/sellers/v2/catalog', params=params)
            page += 1
            items_info = Items.model_validate(response.json()['data'])
            if not items_info.products:
                break
            self.get_images(items_info)
            return items_info
    

    def get_images(self, item_info):
        for product in item_info.products:
            short_id = product.id // 100_000
            if 0 <= short_id <= 143:
                basket = '01'
            elif 144 <= short_id <= 287:
                basket = '02'
            elif 288 <= short_id <= 431:
                basket = '03'
            elif 432 <= short_id <= 719:
                basket = '04'
            elif 720 <= short_id <= 1007:
                basket = '05'
            elif 1008 <= short_id <= 1061:
                basket = '06'
            elif 1062 <= short_id <= 1115:
                basket = '07'
            elif 1116 <= short_id <= 1169:
                basket = '08'
            elif 1170 <= short_id <= 1313:
                basket = '09'
            elif 1314 <= short_id <= 1601:
                basket = '10'
            elif 1602 <= short_id <= 1655:
                basket = '11'
            elif 1656 <= short_id <= 1919:
                basket = '12'
            elif 1920 <= short_id <= 2045:
                basket = '13'
            elif 2046 <= short_id <= 2189:
                basket = '14'
            elif 2190 <= short_id <= 2405:
                basket = '15'
            else:
                basket = '16'


            link_str = "".join(
                [
                    f"https://basket-{basket}.wbbasket.ru/vol{short_id}/part{product.id // 1000}/{product.id}/images/big/{i}.webp;"
                    for i in range(1, product.pics + 1)
                ]
            )
            product.image_links = link_str
            link_str = ''

    
if __name__=="__main__":
    url = 'https://www.wildberries.ru/catalog/17386348/detail.aspx'
    pars = ParserWB(url)
    pars.parse()


