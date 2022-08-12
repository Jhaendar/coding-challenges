# Multiples of 3 or 5
# https://projecteuler.net/problem=1

import math

# N = 1000
N=1000
sum = 0
sum += 3 * sum(range(((N-1)//3) + 1))
sum += 5 * sum(range((N-1)//5 + 1))
sum -= 15 * sum(range((N-1)//15 + 1))

print(sum)
