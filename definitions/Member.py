class Member():
    pass

def get(member_id):
    try:
        return Member(member_id)
    except MemberNotFoundError:
        create(member_id)
        return Member(member_id)