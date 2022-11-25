import math
import random
from sympy import jacobi_symbol
from sympy.ntheory.primetest import mr

k = 5


def generate_list_of_odd(_amount: int, _max_value: int) -> list[int]:
    result = []
    while len(result) != _amount:
        num = random.randint(3, _max_value)
        if num % 2 != 0:
            result.append(num)
    return result


def accuracy(formula):
    def actual_wrapper(func):
        def wrapper(*args, **kwargs):
            if args[0] % 2 == 0:
                raise ValueError("Число четное!")
            for i in range(k):
                if func(*args, **kwargs) == True:
                    return f"Истина вероятностью {round(formula, 3)}"
                else:
                    return "Ложно"

        return wrapper

    return actual_wrapper


@accuracy(formula=1 - pow(2, -k))
def is_prime_ferma(_n: int) -> bool:
    a = random.randint(2, _n - 1)
    if math.gcd(a, _n) == 1:
        if pow(a, _n - 1, _n) == 1:
            return True
    else:
        return False


@accuracy(formula=1 - pow(2, -k))
def solovei_shtrassen_is_prime(_n: int) -> bool:
    a = random.randint(2, _n - 1)
    if math.gcd(a, _n) > 1:
        return False
    x = jacobi_symbol(a, _n) % _n
    if x == 0 or pow(a, (_n - 1) // 2, _n) != x % _n:
        return False
    return True


def s_t_calculate(_n: int) -> tuple[int, int]:
    s = 0
    t = _n - 1
    while t % 2 == 0:
        s += 1
        t //= 2
    return s, t


@accuracy(formula=1 - pow(4, -k))
def miller_rabbin_is_prime(_n: int, s: int, t: int) -> bool:
    a = random.randint(2, _n - 1)
    x = pow(a, t, _n)
    if x == 1 or x == _n - 1:
        return True
    else:
        for i in range(1, s):
            x = pow(x, 2, _n)
            if x == 1:
                return False
            if x == _n - 1:
                return True
    return False


if __name__ == '__main__':
    nums_to_test = generate_list_of_odd(10, pow(10, 200))
    print(f"Параметр точности = {k}")
    for i in nums_to_test:
        args = s_t_calculate(i)
        print(f"{i} простое - {miller_rabbin_is_prime(i, *args)}")
