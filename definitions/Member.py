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
        return Member(member_id)
    except MemberNotFoundError:
        create(member_id)
        return Member(member_id)