import glob
import json

cols = ['id', 'title', 'type', 'brewery', 'current_price', 'normal_price', 'untapped_id', 'untapped_rating']
print("|".join(cols))

for b_fn in glob.glob('./data/*.beer'):
    with open(b_fn) as b_file:
        #print(b_fn)
        beer = json.load(b_file)
        if 'untapped_id' not in beer:
            continue
        if 1.5 <= beer['current_price'] <= 4:
            print("|".join([str(beer[c]).replace("|", "") for c in cols]))

