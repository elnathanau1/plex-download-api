import re

import string
digs = string.digits + string.ascii_letters

def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)

def unpack(p, a, c, k, e=None, d=None):
    ''' unpack
    Unpacker for the popular Javascript compression algorithm.

    @param  p  template code
    @param  a  radix for variables in p
    @param  c  number of variables in p
    @param  k  list of c variable substitutions
    @param  e  not used
    @param  d  not used
    @return p  decompressed string
    '''
    # Paul Koppen, 2011
    for i in range(c - 1, -1, -1):
        if k[i]:
            p = re.sub('\\b' + int2base(i, a) + '\\b', k[i], p)
    return p

def utility_health():
    return "Found utility package"

def contains_none(*argv):
    for arg in argv:
        if arg is None:
            return True
    return False


# https://stackoverflow.com/questions/14996453/python-libraries-to-calculate-human-readable-filesize-from-bytes
suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
