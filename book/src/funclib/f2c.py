def fahr_to_kelvin(temp):
    return ((temp - 32.0) * 5.0/9.0) + 273.15

def kelvin_to_celsius(temp):
    return temp - 273.15

def fahr_to_celsius(temp):
    degrees_k = fahr_to_kelvin(temp)
    return kelvin_to_celsius(degrees_k)

temp_f = 32.0
temp_c = fahr_to_celsius(temp_f)
print 'water freezes at', temp_c
