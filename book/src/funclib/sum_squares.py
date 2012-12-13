def sum(numbers):                       #  1
    result = 0                          #  2
    for x in numbers:                   #  3
        result = result + square(x)     #  4
    return result                       #  5
                                        #  6
def square(val):                        #  7
    result = val * val                  #  8
    return result                       #  9
                                        # 10
print sum([1, 2])                       # 11
