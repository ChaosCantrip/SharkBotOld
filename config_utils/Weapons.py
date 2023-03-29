import json

in_data = [
    {
        "hash": "3863516258",
        "name": "Come to Pass",
        "sub_type": "Auto Rifle",
        "type": "Primary"
    },
    {
        "hash": "1701593813",
        "name": "Sweet Sorrow",
        "sub_type": "Auto Rifle",
        "type": "Primary"
    },
    {
        "hash": "2511032639",
        "name": "Firefright",
        "sub_type": "Auto Rifle",
        "type": "Primary"
    },
    {
        "hash": "122415725",
        "name": "Ammit AR2",
        "sub_type": "Auto Rifle",
        "type": "Primary"
    },
    {
        "hash": "3743137436",
        "name": "Rufus's Fury",
        "sub_type": "Auto Rifle",
        "type": "Primary"
    },
    {
        "hash": "2514059564",
        "name": "Perpetualis",
        "sub_type": "Auto Rifle",
        "type": "Primary"
    },
    {
        "hash": "3907981638",
        "name": "Fel Taradiddle",
        "sub_type": "Bow",
        "type": "Primary"
    },
    {
        "hash": "930979915",
        "name": "Under Your Skin",
        "sub_type": "Bow",
        "type": "Primary"
    },
    {
        "hash": "204031420",
        "name": "Tripwire Canary",
        "sub_type": "Bow",
        "type": "Primary"
    },
    {
        "hash": "3845305795",
        "name": "Raconteur",
        "sub_type": "Bow",
        "type": "Primary"
    },
    {
        "hash": "1444412985",
        "name": "Austringer",
        "sub_type": "Hand Cannon",
        "type": "Primary"
    },
    {
        "hash": "437884069",
        "name": "Zaouli's Bane",
        "sub_type": "Hand Cannon",
        "type": "Primary"
    },
    {
        "hash": "200612470",
        "name": "Posterity",
        "sub_type": "Hand Cannon",
        "type": "Primary"
    },
    {
        "hash": "4070327399",
        "name": "IKELOS_HC_v1.0.3",
        "sub_type": "Hand Cannon",
        "type": "Primary"
    },
    {
        "hash": "2839479882",
        "name": "Round Robin",
        "sub_type": "Hand Cannon",
        "type": "Primary"
    },
    {
        "hash": "3868889639",
        "name": "Insidious",
        "sub_type": "Pulse Rifle",
        "type": "Primary"
    },
    {
        "hash": "3343946430",
        "name": "Piece of Mind",
        "sub_type": "Pulse Rifle",
        "type": "Primary"
    },
    {
        "hash": "953028525",
        "name": "Syncopation-53",
        "sub_type": "Pulse Rifle",
        "type": "Primary"
    },
    {
        "hash": "385553757",
        "name": "BxR-55 Battler",
        "sub_type": "Pulse Rifle",
        "type": "Primary"
    },
    {
        "hash": "2069837521",
        "name": "Smite of Merain",
        "sub_type": "Pulse Rifle",
        "type": "Primary"
    },
    {
        "hash": "929449757",
        "name": "Revision Zero",
        "sub_type": "Pulse Rifle",
        "type": "Primary"
    },
    {
        "hash": "3835559140",
        "name": "Disparity",
        "sub_type": "Pulse Rifle",
        "type": "Primary"
    },
    {
        "hash": "1167176444",
        "name": "Phyllotactic Spiral",
        "sub_type": "Pulse Rifle",
        "type": "Primary"
    },
    {
        "hash": "689439417",
        "name": "Pointed Inquiry",
        "sub_type": "Scout Rifle",
        "type": "Primary"
    },
    {
        "hash": "3693097974",
        "name": "Tears of Contrition",
        "sub_type": "Scout Rifle",
        "type": "Primary"
    },
    {
        "hash": "3650227809",
        "name": "Doom of Chelchis",
        "sub_type": "Scout Rifle",
        "type": "Primary"
    },
    {
        "hash": "146759633",
        "name": "Tarnished Mettle",
        "sub_type": "Scout Rifle",
        "type": "Primary"
    },
    {
        "hash": "3370786210",
        "name": "Trustee",
        "sub_type": "Scout Rifle",
        "type": "Primary"
    },
    {
        "hash": "4205772441",
        "name": "Empirical Evidence",
        "sub_type": "Sidearm",
        "type": "Primary"
    },
    {
        "hash": "826543773",
        "name": "Drang (Baroque)",
        "sub_type": "Sidearm",
        "type": "Primary"
    },
    {
        "hash": "1544481626",
        "name": "Brigand's Law",
        "sub_type": "Sidearm",
        "type": "Primary"
    },
    {
        "hash": "1164396532",
        "name": "Mykel's Reverence",
        "sub_type": "Sidearm",
        "type": "Primary"
    },
    {
        "hash": "403175710",
        "name": "Osteo Striga",
        "sub_type": "Submachine Gun",
        "type": "Primary"
    },
    {
        "hash": "1057921323",
        "name": "Submission",
        "sub_type": "Submachine Gun",
        "type": "Primary"
    },
    {
        "hash": "1615038969",
        "name": "Forensic Nightmare",
        "sub_type": "Submachine Gun",
        "type": "Primary"
    },
    {
        "hash": "2258742229",
        "name": "CALUS Mini-Tool",
        "sub_type": "Submachine Gun",
        "type": "Primary"
    },
    {
        "hash": "2158979729",
        "name": "Blood Feud",
        "sub_type": "Submachine Gun",
        "type": "Primary"
    },
    {
        "hash": "692035983",
        "name": "IKELOS_SMG_v1.0.3",
        "sub_type": "Submachine Gun",
        "type": "Primary"
    },
    {
        "hash": "2896258222",
        "name": "Deliverance",
        "sub_type": "Fusion Rifle",
        "type": "Special"
    },
    {
        "hash": "2107474614",
        "name": "Likely Suspect",
        "sub_type": "Fusion Rifle",
        "type": "Special"
    },
    {
        "hash": "1968204778",
        "name": "The Epicurean",
        "sub_type": "Fusion Rifle",
        "type": "Special"
    },
    {
        "hash": "2546821156",
        "name": "Midha's Reckoning",
        "sub_type": "Fusion Rifle",
        "type": "Special"
    },
    {
        "hash": "3393054854",
        "name": "Royal Executioner",
        "sub_type": "Fusion Rifle",
        "type": "Special"
    },
    {
        "hash": "777254375",
        "name": "Iterative Loop",
        "sub_type": "Fusion Rifle",
        "type": "Special"
    },
    {
        "hash": "3296489718",
        "name": "Edge of Concurrence",
        "sub_type": "Glaive",
        "type": "Special"
    },
    {
        "hash": "1955149226",
        "name": "Edge of Action",
        "sub_type": "Glaive",
        "type": "Special"
    },
    {
        "hash": "96042291",
        "name": "Edge of Intent",
        "sub_type": "Glaive",
        "type": "Special"
    },
    {
        "hash": "1446423643",
        "name": "The Enigma",
        "sub_type": "Glaive",
        "type": "Special"
    },
    {
        "hash": "876397380",
        "name": "Lubrae's Ruin",
        "sub_type": "Glaive",
        "type": "Special"
    },
    {
        "hash": "1691359215",
        "name": "Nezarec's Whisper",
        "sub_type": "Glaive",
        "type": "Special"
    },
    {
        "hash": "1778902326",
        "name": "Judgment of Kelgorath",
        "sub_type": "Glaive",
        "type": "Special"
    },
    {
        "hash": "2627701916",
        "name": "Vexcalibur",
        "sub_type": "Glaive",
        "type": "Special"
    },
    {
        "hash": "422252754",
        "name": "Forbearance",
        "sub_type": "Grenade Launcher",
        "type": "Special"
    },
    {
        "hash": "2115207174",
        "name": "Explosive Personality",
        "sub_type": "Grenade Launcher",
        "type": "Special"
    },
    {
        "hash": "834963888",
        "name": "Pardon Our Dust",
        "sub_type": "Grenade Launcher",
        "type": "Special"
    },
    {
        "hash": "2324218515",
        "name": "Prodigal Return",
        "sub_type": "Grenade Launcher",
        "type": "Special"
    },
    {
        "hash": "220342896",
        "name": "Ragnhild-D",
        "sub_type": "Shotgun",
        "type": "Special"
    },
    {
        "hash": "2126241222",
        "name": "Without Remorse",
        "sub_type": "Shotgun",
        "type": "Special"
    },
    {
        "hash": "631089354",
        "name": "Wastelander M5",
        "sub_type": "Shotgun",
        "type": "Special"
    },
    {
        "hash": "1388873285",
        "name": "Imperial Decree",
        "sub_type": "Shotgun",
        "type": "Special"
    },
    {
        "hash": "3587005520",
        "name": "No Reprieve",
        "sub_type": "Shotgun",
        "type": "Special"
    },
    {
        "hash": "4170453731",
        "name": "Heritage",
        "sub_type": "Shotgun",
        "type": "Special"
    },
    {
        "hash": "1366529950",
        "name": "IKELOS_SG_v1.0.3",
        "sub_type": "Shotgun",
        "type": "Special"
    },
    {
        "hash": "700218081",
        "name": "Nessa's Oblation",
        "sub_type": "Shotgun",
        "type": "Special"
    },
    {
        "hash": "311360599",
        "name": "Father's Sins",
        "sub_type": "Sniper Rifle",
        "type": "Special"
    },
    {
        "hash": "3842442685",
        "name": "Thoughtless",
        "sub_type": "Sniper Rifle",
        "type": "Special"
    },
    {
        "hash": "662547074",
        "name": "Beloved",
        "sub_type": "Sniper Rifle",
        "type": "Special"
    },
    {
        "hash": "3255215894",
        "name": "Defiance of Yasmin",
        "sub_type": "Sniper Rifle",
        "type": "Special"
    },
    {
        "hash": "924334687",
        "name": "Succession",
        "sub_type": "Sniper Rifle",
        "type": "Special"
    },
    {
        "hash": "622035212",
        "name": "IKELOS_SR_v1.0.3",
        "sub_type": "Sniper Rifle",
        "type": "Special"
    },
    {
        "hash": "1517724383",
        "name": "Volta Bracket",
        "sub_type": "Sniper Rifle",
        "type": "Special"
    },
    {
        "hash": "2177815995",
        "name": "Hollow Denial",
        "sub_type": "Trace Rifle",
        "type": "Special"
    },
    {
        "hash": "1254331510",
        "name": "Retraced Path",
        "sub_type": "Trace Rifle",
        "type": "Special"
    },
    {
        "hash": "1506999309",
        "name": "Path of Least Resistance",
        "sub_type": "Trace Rifle",
        "type": "Special"
    },
    {
        "hash": "3838502045",
        "name": "Acasia's Dejection",
        "sub_type": "Trace Rifle",
        "type": "Special"
    },
    {
        "hash": "1507884969",
        "name": "Tarnation",
        "sub_type": "Grenade Launcher",
        "type": "Heavy"
    },
    {
        "hash": "2742412203",
        "name": "Koraxis's Distress",
        "sub_type": "Grenade Launcher",
        "type": "Heavy"
    },
    {
        "hash": "752104278",
        "name": "Regnant",
        "sub_type": "Grenade Launcher",
        "type": "Heavy"
    },
    {
        "hash": "170523067",
        "name": "Dimensional Hypotrochoid",
        "sub_type": "Grenade Launcher",
        "type": "Heavy"
    },
    {
        "hash": "2292557505",
        "name": "Marsilion-C",
        "sub_type": "Grenade Launcher",
        "type": "Heavy"
    },
    {
        "hash": "989023188",
        "name": "Cataclysmic",
        "sub_type": "Linear Fusion Rifle",
        "type": "Heavy"
    },
    {
        "hash": "4013775975",
        "name": "Taipan-4fr",
        "sub_type": "Linear Fusion Rifle",
        "type": "Heavy"
    },
    {
        "hash": "1389390726",
        "name": "Sailspy Pitchglass",
        "sub_type": "Linear Fusion Rifle",
        "type": "Heavy"
    },
    {
        "hash": "3172595571",
        "name": "Fire and Forget",
        "sub_type": "Linear Fusion Rifle",
        "type": "Heavy"
    },
    {
        "hash": "417302779",
        "name": "Briar's Contempt",
        "sub_type": "Linear Fusion Rifle",
        "type": "Heavy"
    },
    {
        "hash": "3357460834",
        "name": "Recurrent Impact",
        "sub_type": "Machine Gun",
        "type": "Heavy"
    },
    {
        "hash": "2547048326",
        "name": "Fixed Odds",
        "sub_type": "Machine Gun",
        "type": "Heavy"
    },
    {
        "hash": "750389420",
        "name": "Qullim's Terminus",
        "sub_type": "Machine Gun",
        "type": "Heavy"
    },
    {
        "hash": "3257403871",
        "name": "Planck's Stride",
        "sub_type": "Machine Gun",
        "type": "Heavy"
    },
    {
        "hash": "633869177",
        "name": "Commemoration",
        "sub_type": "Machine Gun",
        "type": "Heavy"
    },
    {
        "hash": "3862297426",
        "name": "Retrofit Escapade",
        "sub_type": "Machine Gun",
        "type": "Heavy"
    },
    {
        "hash": "3770251030",
        "name": "Red Herring",
        "sub_type": "Rocket Launcher",
        "type": "Heavy"
    },
    {
        "hash": "292832740",
        "name": "Palmyra-B",
        "sub_type": "Rocket Launcher",
        "type": "Heavy"
    },
    {
        "hash": "2330294643",
        "name": "Bump in the Night",
        "sub_type": "Rocket Launcher",
        "type": "Heavy"
    },
    {
        "hash": "3735490332",
        "name": "Half-Truths",
        "sub_type": "Sword",
        "type": "Heavy"
    },
    {
        "hash": "3735490333",
        "name": "The Other Half",
        "sub_type": "Sword",
        "type": "Heavy"
    },
    {
        "hash": "3091520691",
        "name": "Goldtusk",
        "sub_type": "Sword",
        "type": "Heavy"
    },
    {
        "hash": "3091520690",
        "name": "Death's Razor",
        "sub_type": "Sword",
        "type": "Heavy"
    },
    {
        "hash": "3091520689",
        "name": "Throne-Cleaver",
        "sub_type": "Sword",
        "type": "Heavy"
    },
    {
        "hash": "399865831",
        "name": "Bequest",
        "sub_type": "Sword",
        "type": "Heavy"
    },
    {
        "hash": "3171877617",
        "name": "Caretaker",
        "sub_type": "Sword",
        "type": "Heavy"
    }
]

for weapon in in_data:
    print(f"\n\n{weapon['name']} - {weapon['type']} {weapon['sub_type']}")
    sources = input("Sources: ").split(",")
    weapon["sources"] = [source.strip() for source in sources]

with open("input.json", "w") as f:
    json.dump(in_data, f, indent=4)