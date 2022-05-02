

##Decorator snippet
def decorator(func):
    def wrapper(*args, **kwargs):
        ##Do stuff before

        func(*args, **kwargs)

        ##Do stuff after
    return wrapper
