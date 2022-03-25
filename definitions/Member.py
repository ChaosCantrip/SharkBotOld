from definitions import SharkErrors

class Member():
    
    def __init__(self, member_id):
        try:
            r = open(f"collectibles/{member_id}.txt", "r")
            rawFileData = r.read()
            fileData = rawFileData.split("\n")
            r.close()
        except FileNotFoundError:
            raise SharkErrors.MemberFileNotFoundError

        self.id = int(fileData[0])
        self.balance = int(fileData[1])
        self.inventory = fileData[2].split(",")
        self.collection = fileData[3].split(",")



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