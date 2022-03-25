
class SharkError(Exception):
    pass

class MemberFileNotFoundError(SharkError):
    pass

class AccountAlreadyLinkedError(SharkError):
    pass

class AccountNotLinkedError(SharkError):
    pass