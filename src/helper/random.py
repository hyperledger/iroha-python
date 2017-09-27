import random
source_str = 'abcdefghijklmnopqrstuvwxyz'

def uuid(num): #疑似
    return "".join([random.choice(source_str) for x in range(num)])