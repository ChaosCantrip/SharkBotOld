from collectibles import common, uncommon, rare, legendary, exotic

table = common.table + uncommon.table + rare.table + legendary.table + exotic.table
collection = {**common.collection, **uncommon.collection, **rare.collection, **legendary.collection, **exotic.collection}