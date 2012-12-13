base = 17
value = 6
for i in range(20):
    value = (3 * value + 5) % base
    print value,
