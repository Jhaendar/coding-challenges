# Problem 2
# Evem Fibonacci numbers
# https://projecteuler.net/problem=2

# Answer
# 4613732

max = 4000000
a = 1
b = 2

# linear time
def half_sol(a, b, max):
    # increments both a and b at the same time
    # should result in half the number of loops of linear_sol()

    sums = 0
    if (a%2==0):
        sums+=a
    if (b%2==0):
        sums+=b
    
    while True:
        #STEP
        a = a+b
        if (a >= max):
            break
        if (a % 2) == 0:
            sums += a
        
        b = a+b
        if (b >= max):
            break
        if (b % 2)== 0:
            sums += b
    
    return sums

print(half_sol(a, b, max))

def linear_sol(a, b, max):
    # Just checks for the highest value
    sums = 0
    while b < max:
        if (b%2)==0:
            sums+=b
        
        #STEP
        c = b
        b += a
        a = c

    return sums

#POOR SOLUTION
def list_sol(a, b, max):
    #building the sequence in a list
    fib_seq = [a, b]
    sums = 0
    while fib_seq[-1] < max:
        fib_seq.append(fib_seq[-1]+fib_seq[-2])

    return sum([x for x in fib_seq if x%2==0])


