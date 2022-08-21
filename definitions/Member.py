from definitions import SharkErrors, Item
from handlers import databaseHandler
import json


class Member:

    def __init__(self, member_data):

        self.id = member_data["id"]
        self.balance = member_data["balance"]
        self.inventory = member_data["inventory"]
        self.collection = member_data["collection"]
        self.linked_account = member_data["email"]
        self.counts = member_data["counts"]
        self.discordMember = None

    def write_data(self):
        member_data = {}
        member_data["id"] = self.id
        member_data["balance"] = self.balance
        member_data["inventory"] = self.inventory
        member_data["collection"] = self.collection
        member_data["email"] = self.linked_account
        member_data["counts"] = self.counts

        update_json_file(self.id, member_data)

    def upload_data(self):
        connection = databaseHandler.create_connection()
        cursor = connection.cursor()
        databaseHandler.ensure_row_exists(cursor, self, True)
        databaseHandler.update_member_data(cursor, self)
        connection.commit()

    ##--Inventory--##

    def get_inventory(self):
        return self.inventory

    def add_to_inventory(self, item):
        if item.id not in self.collection:
            self.add_to_collection(item)
        self.inventory.append(item.id)
        self.write_data()

    def add_items_to_inventory(self, items):
        for item in items:
            if item.id not in self.collection:
                self.add_to_collection(item)
            self.inventory.append(item.id)
        self.write_data()

    def remove_from_inventory(self, item):
        if item.id not in self.inventory:
            raise SharkErrors.ItemNotInInventoryError(item.id)
        self.inventory.remove(item.id)
        self.write_data()

    ##--Collection--##

    def get_collection(self):
        return self.collection

    def add_to_collection(self, item):
        if item.id not in self.collection:
            self.collection.append(item.id)
        self.write_data()

    def remove_from_collection(self, item):
        if item.id not in self.collection:
            raise SharkErrors.ItemNotInCollectionError(item.id)
        self.collection.remove(item.id)
        self.write_data()

    ##--Balance--##

    def get_balance(self):
        return self.balance

    def add_balance(self, amount):
        self.balance += amount
        self.write_data()

    def set_balance(self, amount):
        self.balance = amount
        self.write_data()

    ##--Discord Member--##

    async def fetch_discord_member(self, bot):
        self.discordMember = bot.get_user(self.id)
        if self.discordMember is None:
            try:
                self.discordMember = await bot.fetch_user(self.id)
            except:
                self.discordMember = None

    ##--Email--##

    def link_account(self, account):
        account = account.lower()
        if self.linked_account is not None:
            raise SharkErrors.AccountAlreadyLinkedError

        usedAccounts = get_used_accounts()
        if account in usedAccounts:
            raise SharkErrors.AccountAlreadyInUseError

        usedAccounts.append(account)
        write_used_accounts(usedAccounts)

        self.linked_account = account
        self.write_data()

    def unlink_account(self):
        if self.linked_account is None:
            raise SharkErrors.AccountNotLinkedError

        usedAccounts = get_used_accounts()
        usedAccounts.remove(self.linked_account)
        write_used_accounts(usedAccounts)

        self.linked_account = None
        self.write_data()

    ##--Counts--##

    def get_counts(self):
        return self.counts

    def add_counts(self, amount: int):
        self.counts += amount
        self.write_data()

    def set_counts(self, amount: int):
        self.counts = amount
        self.write_data()

    ##--Destructor--##

    def __del__(self):
        pass
        ##self.write_data()


class BlankMember(Member):

    def __init__(self, member_id):
        self.id = int(member_id)
        self.balance = defaultvalues["balance"]
        self.inventory = defaultvalues["inventory"]
        self.collection = defaultvalues["collection"]
        self.linked_account = defaultvalues["email"]
        self.counts = defaultvalues["counts"]


def get(member_id):
    member_id = str(member_id)
    with open("data/memberdata.json", "r") as infile:
        data = json.load(infile)

    if member_id in data:
        member = convert_data_to_member(data[member_id])
    else:
        member = BlankMember(member_id)
        member.write_data()
    return member


def get_all_members():
    with open("data/memberdata.json", "r") as infile:
        data = json.load(infile)

    members = []
    for memberData in list(data.values()):
        member = convert_data_to_member(memberData)
        members.append(member)

    return members


def convert_data_to_member(data):
    updatedData = update_data(data)
    member = Member(updatedData)
    return member


def update_json_file(member_id, member_data):
    with open("data/memberdata.json", "r") as infile:
        json_data = json.load(infile)
    json_data[str(member_id)] = member_data
    with open("data/memberdata.json", "w") as outfile:
        json.dump(json_data, outfile, indent=4)


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


defaultvalues = {
    "id": 1234,
    "balance": 0,
    "inventory": [],
    "collection": [],
    "email": None,
    "counts": 0
}


def update_data(data):
    for value in defaultvalues:
        if value not in data:
            data[value] = defaultvalues[value]
    return data
