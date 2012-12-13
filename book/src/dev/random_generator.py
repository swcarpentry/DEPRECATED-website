base = 17  # a prime
value = 4  # anything in 0..base-1
for i in range(20):
    value = (3 * value + 5) % base
    print value,
