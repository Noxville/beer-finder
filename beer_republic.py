import requests
import pprint
import json

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/35.0.1916.47 Safari/537.36'

pp = pprint.PrettyPrinter(indent=4)


def get_beers(page=0):
    headers = {'user-agent': USER_AGENT}
    base_url = f"https://beerrepublic.eu/collections/all-beers/products.json?page={page}"
    print(f"Collecting {base_url}")

    beer_data = requests.get(base_url, headers=headers).json()['products']
    for b in beer_data:
        yield extract_props(b)

    if len(beer_data) == 30:
        yield from get_beers(1 + page)
    else:
        return


def extract_props(beer):
    if len(beer['variants']) != 1:
        return None
    variant = sorted([b for b in beer['variants'] if b['available']], key=lambda v: v['position'])[0]
    price = float(variant['price'])

    return {
        'id': beer['id'],
        'title': beer['title'],
        'type': beer.get('product_type'),
        'brewery': beer['vendor'],
        'current_price': price,
        'normal_price': float(variant['compare_at_price']) if ('compare_at_price' in variant and
                                                               variant['compare_at_price']) else price
    }


with open('beer_republic.catalogue', 'w') as fout:
    beers = [b for b in get_beers()]
    json.dump(beers, fout)





