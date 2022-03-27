from definitions import SharkErrors, Item
import json

class Member():
    
    def __init__(self, member_data):
        
        self.id = member_data["id"]
        self.balance = member_data["balance"]
        self.inventory = member_data["inventory"]
        self.collection = member_data["collection"]
        self.linked_account = member_data["email"]

    def write_data(self):
        member_data = {}
        member_data["id"] = self.id
        member_data["balance"] = self.balance
        member_data["inventory"] = self.inventory
        member_data["collection"] = self.collection
        member_data["email"] = self.linked_account

        update_json_file(self.id, member_data)

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

    def get_balance(self):
        return self.balance

    def add_balance(self, amount):
        self.balance += amount
        self.write_data()

    def set_balance(self, amount):
        self.balance = amount
        self.write_data()

    def link_account(self, account):
        account = account.lower()
        if self.linked_account != None:
            raise SharkErrors.AccountAlreadyLinkedError
        
        usedAccounts = get_used_accounts()
        if account in usedAccounts:
            raise SharkErrors.AccountAlreadyInUseError

        usedAccounts.append(account)
        write_used_accounts(usedAccounts)
        
        self.linked_account = account
        self.write_data()

    def unlink_account(self):
        if self.linked_account == None:
            raise SharkErrors.AccountNotLinkedError
        
        usedAccounts = get_used_accounts()
        usedAccounts.remove(self.linked_account)
        write_used_accounts(usedAccounts)

        self.linked_account = None
        self.write_data()

    def __del__(self):
        pass
        ##self.write_data()




class BlankMember(Member):
    
    def __init__(self, member_id):
        self.id = int(member_id)
        self.balance = 0
        self.inventory = []
        self.collection = []
        self.linked_account = None

def get(member_id):
    with open("data/memberdata.json", "r") as infile:
        data = json.load(infile)

    if str(member_id) in data:
        member = Member(data[str(member_id)])
    else:
        member = BlankMember(member_id)
        member.write_data()
    return member

def update_json_file(member_id, member_data):
    with open("data/memberdata.json", "r") as infile:
        json_data = json.load(infile)
    json_data[str(member_id)] = member_data
    with open("data/memberdata.json", "w") as outfile:
        json.dump(json_data, outfile)

def get_used_accounts():
    r = open(f"data/usedaccounts.txt", "r")
    rawFileData = r.read()
    if rawFileData == "":
        fileData = []
    else:
        fileData = rawFileData.split("\n")
    r.close()
    return fileData

def write_used_accounts(accountList):
    w = open(f"data/usedaccounts.txt", "w")
    w.write("\n".join(accountList))
    w.close()
