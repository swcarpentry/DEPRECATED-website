def sign(num):
    if num < 0:
        return -1
    if num == 0:
        return 0
#    return 1

print -5, '=>', sign(-5)
print 0, '=>', sign(0)
print 241, '=>', sign(241)
