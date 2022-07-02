from bs4 import BeautifulSoup
import os.path
import urllib.parse
import requests
import json

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/35.0.1916.47 Safari/537.36'

# Tuple representing (ignore, mapped search string)
mappings = {
    6629886492844: (False, 'Firestone Walker Brewing Company DBA (Double Barrel Ale)'),
    4368413917255: (False, 'Bierbrouwerij De Koningshoeven La Trappe Isid\'or'),
    1709805764679: (False, 'Destihl Dosvidanya Rye Barrel'),
    6152271069356: (False, 'Collective Arts Brewing Origin of Darkness w/ Marshmallows, Cocoa, Cinnamon, & Lactose'),
    4368443441223: (False, 'Bierbrouwerij De Koningshoeven La Trappe Tripel'),
    4368408641607: (False, 'Bierbrouwerij De Koningshoeven La Trappe Dubbel'),
    4368437510215: (False, 'Bierbrouwerij De Koningshoeven La Trappe Quadrupel'),
    7222531555500: (False, 'New Belgium Brewing Company Voodoo Ranger Agent 77'),
    10494442316: (False, 'Jolly Pumpkin Artisan Ales Oro De Calabaza With Blackberry And Lime'),
    7149029228716: (False, 'Evil Twin brewing hey dad did you change the password'),
    222641684505: (False, 'LTM - Les Trois Mousquetaires Ceci N\'est Pas Une Gueuze'),
    4594346033223: (False, 'Crux Better Off Red'),
    6640205529260: (False, 'Modern Times Pharaoh Ascendant Pharaoh Ascendant: Chocolate Cake Edition W/ Cocoa & Vanilla'),
    6640203366572: (False, 'Modern Times Pharaoh Ascendant: Chocolate Cake Edition W/ Cocoa & Coconut'),
    7058303189164: (False, 'Hidden Springs Zero Fucks Given'),
    4594375688263: (False, 'ONE-OFF [BANISHED] Freakcake #2 - Aged On Dates'),
    6640201728172: (False, 'Pharaoh Ascendant: Chocolate Cake Edition W/ Cocoa & Pecans'),
    6640203923628: (False, 'Pharaoh Ascendant: Chocolate Cake Edition W/ Cocoa, Raspberry, & Vanilla'),
    1845993701447: (False, 'Blurred Sb (2019)'),
    6913236500652: (False, 'Enrico Palazzo (Bourbon Barrel Aged)'),
    4797064708167: (False, 'New Belgium Brewing Company Fat Tire'),
    4797055172679: (False, 'New Belgium 1554'),
    4594379292743: (False, 'Crux ONE-OFF [BANISHED] Freakcake #5 Aged On Zante Currants'),
    7209459744940: (False, 'Local Craft Beer (LCB) Meet Me In the Red Room'),
    7251923304620: (False, 'Evil Twin Brewing Retro IPA'),
    7206496534700: (False, 'Equilibrium Brewery - Austin'),
    7275499126956: (False, 'El Segundo fremont'),
    6911544885420: (True, None),
    7105889697964: (True, None),
    7289040699564: (True, None),
    6120704704684: (True, None),
    1902227914823: (True, None),
    6812758016172: (True, None),
    4894592139335: (True, None),
    7166011965612: (True, None),
    6812740616364: (True, None),
    6814354833580: (True, None),
    7194689634476: (True, None),
    7142669844652: (True, None),
    7195916140716: (True, None),
    7137203191980: (True, None),
    6993219223724: (True, None),
    4678542786631: (True, None),
    6911542984876: (True, None),
    1902236467271: (True, None),
    1902231781447: (True, None),
    6911525748908: (True, None),
    7092254933164: (True, None),
    6263560962220: (True, None),
    9018127564: (True, None),
    6929645797548: (True, None),
    4764178841671: (True, None),
    7217510875308: (True, None),
    7076696653996: (True, None),
    4781600342087: (True, None),
    6038781853868: (True, None),
    7194962722988: (True, None),
    1902343323719: (True, None),
    7142663717036: (True, None),
    1867224776775: (True, None),
    6616063344812: (True, None),
    1732577361991: (True, None),
    11037657228: (True, None),
    7139177267372: (True, None),
    4781655326791: (True, None),
    6969284853932: (True, None),
    6954249683116: (True, None),
    4814179270727: (True, None),
    1845924659271: (True, None),
    4797063462983: (True, None),
    6827761893548: (True, None),
    6874633928876: (True, None),
    4797455925319: (True, None),
    10343660172: (True, None),
    4663590027335: (True, None),
    7126998581420: (True, None),
    6906397458604: (True, None),
    175090106393: (True, None),
    175088599065: (True, None),
    9319334668: (True, None),
    6189537427628: (True, None),
    6243318759596: (True, None),
    6189517209772: (True, None),
    1902336606279: (True, None),
    7215313387692: (True, None),
    4360822423623: (True, None),
    7215323545772: (True, None),
    7278163656876: (True, None),
    6867445186732: (True, None),
    6874674004140: (True, None),
    7285267366060: (True, None),
    7357607346348: (True, None),
    6874654277804: (True, None),
    4360811184199: (True, None),
    6766602584236: (True, None),
    196569333785: (True, None),
    196568907801: (True, None),
    6911539937452: (True, None),
    4829818945607: (True, None),
    1725193912391: (True, None),
    7286712697004: (True, None)
}


def handle_map(beer):
    return mappings.get(beer['id'],
                        (False, beer['brewery'] + ' ' + beer['title']))


def untappd(beer):
    print(beer)
    ignore, mapped = handle_map(beer)
    if ignore:
        return beer

    query = urllib.parse.quote_plus(mapped)
    headers = {'user-agent': USER_AGENT}
    page = requests.get(f"https://untappd.com/search?q={query}&type=beer&sort=all", headers=headers)
    print(page.url)

    soup = BeautifulSoup(page.text, 'html.parser')
    best_guess = soup.select_one("div.results-container").select_one("div.beer-item")
    untapped_id = best_guess.select_one("a.label")['href'].replace('/beer/', '')
    untapped_rating = best_guess.select_one("div.rating").select_one("div.caps")['data-rating']

    beer['untapped_id'] = int(untapped_id)
    beer['untapped_rating'] = float(untapped_rating)
    return beer


with open('beer_republic.catalogue') as fin:
    beers = json.load(fin)

    for idx, b in enumerate(beers):
        print(f"{1 + idx}/{len(beers)}")
        f_name = f"./data/{b['id']}.beer"

        if os.path.exists(f_name) and os.stat(f_name).st_size:
            continue

        with open(f_name, 'w') as fout:
            enriched = untappd(b)
            json.dump(enriched, fout)
