import requests
import time
import random
import pandas as pd

def get_product_ids(path = "product_id_tiki.csv"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    link = "https://tiki.vn/api/v2/products?limit=40&include=advertisement&aggregations=2&version=&trackity_id=d04c31ed-ff95-1697-e13a-8e98c7945788&q=smartphone&page={}"


    product_ids = []
    for i in range(1, 13):
        response = requests.get(link.format(i), headers = headers)
        if response.status_code == 200:
            print("Crawl page {}".format(i))
            data = response.json().get("data")
            for product in data:
                product_id = int(product['id'])
                product_ids.append(product_id)
        else:
            print(i)
        time.sleep(random.randint(5, 10))

    df = pd.DataFrame(product_ids, columns = ["product_id"])
    df.to_csv("product_id_tiki.csv", index = False)
    
    return df

