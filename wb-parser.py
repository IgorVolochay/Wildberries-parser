import random
import json

import requests
from urllib.request import urlretrieve

def find_basket(product_id):
    vol = product_id // 100000
    if 0 <= vol <= 143:
        return "01"
    elif 144 <= vol <= 287:
        return "02"
    elif 288 <= vol <= 431:
        return "03"
    elif 432 <= vol <= 719:
        return "04"
    elif 720 <= vol <= 1007:
        return "05"
    elif 1008 <= vol <= 1061:
        return "06"
    elif 1062 <= vol <= 1115:
        return "07"
    elif 1116 <= vol <= 1169:
        return "08"
    elif 1170 <= vol <= 1313:
        return "09"
    elif 1314 <= vol <= 1601:
        return "10"
    elif 1602 <= vol <= 1655:
        return "11"
    elif 1656 <= vol <= 1919:
        return "12"
    elif 1920 <= vol <= 2045:
        return "13"
    else:
        return "14"

def get_description(product_id, basket_number):
    response = "https://basket-"+str(basket_number)+".wbbasket.ru/vol"+\
               str(product_id)[:4]+"/part"+str(product_id)[:6]+"/"+str(product_id)+"/info/ru/card.json"
    req = requests.get(response)

    if req.status_code != 200:
        return None

    req_data = json.loads(req.text)
    if "description" in req_data.keys():
        description = req_data["description"]
        return description
    else:
        return None

def get_product_list():
    get_resp = "https://recom.wb.ru/personal/ru/common/v5/search?ab_testing=false&appType=1&curr=rub&dest=-5551775&page="+\
               str(random.randint(2, 10))+\
               "&query=0&resultset=catalog&spp=30&suppressSpellcheck=false&uclusters=1&uiv=2&uv=pYuil6rQLkSmf64EMTQuYCWBqvykpiEYpNOsPS8YqYqkrq8hrf6ovav9sdyIIappJ-CxiyIFpzwujavmK8exDqmFqK8xni6WLloz_K7Irlue06ywIW4soaupsrQtNauCrNWqCy9NsPKs3Z1EmyEp9S3OpWsvNyStrl2uYh-DKNcshC6kL9ktNK-bsQcp6RhCrrevCSbksNspSK5pqTUiDy3BpFGkzSSbrFguwK5MrESiszFepsCosyTeFyUoV6xbLO4piKZEnm6pPK6LLyAcKTKqrl8weS2TpwCfGy1lrZUqQDCArLOrmy-UMFqtoS_nLvYgciDVI1qsMKEuMcYfKw"
    req = json.loads(requests.get(get_resp).text)

    return req["data"]["products"]

def get_img(product_id, basket_counter, pics_number):
    pics_names_list = list()
    for pic_index in range(1, pics_number):
        name = f"{product_id}_{pic_index}.png"

        true_path = None
        for first in [3, 4]:
            for second in [5, 6]:
                req = requests.get("https://basket-" + str(basket_counter) + ".wbbasket.ru/vol" + str(product_id)[
                    :first] + "/part" + str(product_id)[:second] + "/" + str(product_id) + "/images/big/"+str(pic_index)+".webp")
                if req.status_code == 200:
                    true_path = [first, second]
        if true_path:
            get_resp = "https://basket-" + str(basket_counter) + ".wbbasket.ru/vol" + str(product_id)[
                    :true_path[0]] + "/part" + str(product_id)[:true_path[1]] + "/" + str(product_id) + "/images/big/"+str(pic_index)+".webp"
            urlretrieve(get_resp, f"img/{name}")
            pics_names_list.append(name)
    return pics_names_list

def get_product_info(product):
    product_id = product["id"]
    basket_number = find_basket(product_id)

    name = product["name"]
    description = get_description(product_id, basket_number)
    brand = product["brand"]
    rating = product["reviewRating"]
    feedbacks = product["feedbacks"]
    price = product["sizes"][0]["price"]["product"]
    pics_number = product["pics"]

    return product_id, name, description, brand, rating, feedbacks, price, pics_number, basket_number

if __name__ == "__main__":
    prod_list = get_product_list()

    products_in_list = list()
    for product in prod_list:
        product_id, name, description, brand, rating, feedbacks, price, pics_number, basket_number = get_product_info(product)

        pics_names_list = get_img(product_id, basket_number, pics_number)

        result = {product_id: {"name": name,
                               "description": description,
                               "brand": brand,
                               "rating": rating,
                               "feedbacks": feedbacks,
                               "price": price,
                               "pics_files": pics_names_list}

                  }
        products_in_list.append(result)

    print(len(products_in_list), *products_in_list[:3], sep="\n")







