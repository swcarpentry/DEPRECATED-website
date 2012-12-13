def fahr_to_kelvin(temp):
    return ((temp - 32.0) * 5.0/9.0) + 273.15

print 'water freezes at', fahr_to_kelvin(32)
print 'water boils at', fahr_to_kelvin(212)
