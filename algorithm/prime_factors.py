# -*- coding: utf-8 -*-


def prime_factors(n):
    f = 2
    while f * f <= n:
        while not n % f:
            yield f
            n //= f
        f += 1
    if n > 1:
        yield n

print list(prime_factors(600851475143))
