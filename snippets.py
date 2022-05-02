

##Decorator snippet
def decorator(func):
    def wrapper(*args, **kwargs):
        ##Do stuff before

        func(*args, **kwargs)

        ##Do stuff after
    return wrapper



##Class snippet
class class():

    def __init__(self):
        pass
