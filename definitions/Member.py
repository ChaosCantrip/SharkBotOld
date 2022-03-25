from definitions import SharkErrors, Item

class Member():
    
    def __init__(self, member_id):
        try:
            r = open(f"data/members/{member_id}.txt", "r")
            rawFileData = r.read()
            fileData = rawFileData.split("\n")
            r.close()
        except FileNotFoundError:
            raise SharkErrors.MemberFileNotFoundError

        self.id = int(fileData[0])
        self.balance = int(fileData[1])
        self.inventory = fileData[2].split(",")
        self.collection = fileData[3].split(",")

    def write_data(self):
        fileData = ""
        fileData += f"{self.id}\n"
        fileData += f"{self.balance}\n"
        if self.inventory == []:
            fileData += ","
        for item in self.inventory:
            fileData += f"{item},"
        fileData = fileData[:-1] + "\n"
        if self.collection == []:
            fileData += ","
        for item in self.collection:
            fileData += f"{item},"
        fileData = fileData[:-1]

        w = open(f"data/members/{self.id}.txt", "w")
        w.write(fileData)
        w.close()

    def add_to_inventory(self, item):
        if type(item) == Item.Item:
            itemid = item.id
        else:
            itemid = item

        if itemid not in self.collection:
            self.add_to_collection(itemid)
        self.inventory.append(itemid)
        self.write_data()

    def add_to_collection(self, item):
        if type(item) == Item.Item:
            itemid = item.id
        else:
            itemid = item

        if itemid not in self.collection:
            self.collection.append(itemid)
        self.write_data()

    def get_balance(self, amount):
        return self.balance

    def add_balance(self, amount):
        self.balance += amount
        self.write_data()

    def set_balance(self, amount):
        self.balance = amount
        self.write_data()

    def __del__(self):
        self.write_data()




class BlankMember(Member):
    
    def __init__(self, member_id):
        self.id = int(member_id)
        self.balance = 0
        self.inventory = []
        self.collection = []

def get(member_id):
    try:
        member = Member(member_id)
    except SharkErrors.MemberFileNotFoundError:
        member = BlankMember(member_id)
        member.write_data()
    return member