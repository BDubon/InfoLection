def get_sum(t):
    sum = 0
    i = len(t)
    while i > 0:
        i = i - 1
        sum = sum + t[i]
    return sum
print(get_sum([1,2,3]))


