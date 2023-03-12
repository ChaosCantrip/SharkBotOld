import json
data = {
    "name": (name:=input("Name: ")),
    "destination": input("Destination: "),
    "burn": input("Burn: "),
    "embed_url": f"https://kyber3000.com/LS-{''.join(name.split(' '))}",
    "legend": {
        "champions": {
            "Barrier": 100,
            "Overload": 100,
            "Unstoppable": 100
        },
        "shields": {
            "Arc": 100,
            "Solar": 100,
            "Void": 100,
            "Strand": 100
        }
    },
    "master": {
        "champions": {
            "Barrier": 100,
            "Overload": 100,
            "Unstoppable": 100
        },
        "shields": {
            "Arc": 100,
            "Solar": 100,
            "Void": 100,
            "Strand": 100
        }
    }
}

with open("../data/static/destiny/lost_sectors/lost_sectors.json", "r") as infile:
    before = json.load(infile)

before.append(data)

with open("../data/static/destiny/lost_sectors/lost_sectors.json", "w") as outfile:
    json.dump(before, outfile, indent=2)
