

def contains_none(*argv):
    for arg in argv:
        if arg is None:
            return True
    return False
