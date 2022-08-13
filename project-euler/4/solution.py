# Problem 4
# Largest palindrome product
# https://projecteuler.net/problem=4
# Answer: 906609

def is_palindrome(n):
    n_str = str(n)

    mid = len(n_str)//2

    f_h = n_str[:mid]

    mid += 1 if len(n_str)%2==1 else 0
    f_l = n_str[:mid-1:-1]
    return f_h == f_l
    
def first_sol(a_max, b_max):
    largest = 0
    for i in range(a_max, 0, -1):
        for j in range(b_max, 0, -1):
            m =i*j
            if is_palindrome(m):
                if m>largest:
                    largest = m                 
    return largest
print(first_sol(999, 999))




    
