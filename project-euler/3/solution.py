# Problem 3
# Largest prime factor
# https://projecteuler.net/problem=3
# Answer 
# 6857
import math

N = 600851475143 

def is_prime(N):
    f_max = math.floor(math.sqrt(N))
    k_max = f_max//6

    if (N%2)==0:
        return False
    if (N%3)==0:
        return False
    k = 1
    while k <= k_max:
        if N % (6*k-1) == 0:
            return False
        if N %(6*k + 1) > f_max:
            break
        if N %(6*k + 1) == 0:
            return False

        k+=1
    return True

def sieve_down(N):
    f_max = math.floor(math.sqrt(N))
    k_max = f_max//6

    f_h = (6*k_max + 1)
    if (f_h < f_max) and is_prime(f_h) and(N % f_h) == 0 :
        return f_h
    k_max -= 1
    while k_max > 0:
        f_h = (6*k_max + 1)
        if is_prime(f_h) and (N % f_h) == 0:
            return f_h
        f_l = 6*k_max - 1
        if is_prime(f_l) and (N % f_l == 0):
            return f_l
        k_max -= 1

    print("HERE")
    if (N%3==0): return 3
    if (N%2==0): return 1

print(sieve_down(N))