class Member():
    pass

class BlankMember(Member):
    
    def __init__(self, member_id):
        self.id = int(member_id)
        self.balance = 0
        self.inventory = []
        self.collection = []

def get(member_id):
    try:
        member = Member(member_id)
    except MemberNotFoundError:
        member = BlankMember(member_id)
        member.write_data()
    return member