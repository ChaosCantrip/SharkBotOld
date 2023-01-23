import json
from datetime import datetime, timedelta

_FILEPATH = "../data/static/collectibles/event_calendars.json"
_DATE_FORMAT = "%d/%m/%Y"

name = input("Name: ")
start_date = datetime.strptime(input("Start Date: "), _DATE_FORMAT).date()
end_date = datetime.strptime(input("End Date: "), _DATE_FORMAT) + timedelta(days=1)
end_date = end_date.date()
rewards = {}
current_date = start_date
while current_date < end_date:
    if current_date not in rewards:
        rewards[current_date] = {}
    print(f"Date: {datetime.strftime(current_date, _DATE_FORMAT)}")
    print(f"Current Items: {[f'{num}x {item_id}' for item_id, num in rewards[current_date].items()]}")
    raw_input = input("Input: ").upper()

    if raw_input == "NEXT":
        current_date += timedelta(days=1)
        print(f"Moving to {datetime.strftime(current_date, _DATE_FORMAT)}")
    elif raw_input == "CLEAR":
        rewards[current_date] = {}
        print(f"Cleared {datetime.strftime(current_date, _DATE_FORMAT)}")
    elif raw_input == "BACK":
        current_date -= timedelta(days=1)
        print(f"Moving back to {datetime.strftime(current_date, _DATE_FORMAT)}")
    else:
        input_split = raw_input.split(" ")
        try:
            num = int(input_split[0])
            item_id = input_split[1]
            rewards[current_date][item_id] = num
        except Exception as e:
            print("Idk tf u want from me")
            print(type(e))

print("\nReached End Date")
with open(_FILEPATH, "r") as infile:
    data: list[dict] = json.load(infile)

names = [d["name"].lower() for d in data]

if name.lower() in names:
    print(f"'{name}' already exists, removing.")
    data.pop(names.index(name.lower()))

raw_rewards = []
for r in rewards.values():
    date_rewards = []
    for item_id, num in r.items():
        for i in range(num):
            date_rewards.append(item_id)
    raw_rewards.append(date_rewards)

data.append({
    "name": name,
    "start_date": datetime.strftime(start_date, _DATE_FORMAT),
    "rewards": raw_rewards
})

print(json.dumps(data[-1], indent=2))

with open(_FILEPATH, "w+") as outfile:
    json.dump(data, outfile, indent=2)
