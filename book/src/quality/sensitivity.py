def sensitivity(alpha, beta):
    if alpha:
        factor = 0
    else:
        factor = 2
        
    if beta:
        result = 2.0/factor
    else:
        result = factor/2.0
        
    return result

assert sensitivity(False, False) == 1
assert sensitivity(True, False) == 0
