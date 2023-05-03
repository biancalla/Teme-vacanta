# # HOMEWORK_C10_EX01 (for vacation): Creati un iterator similar cu PrimeIterator care sa returneze literele mici din
# # alfabet (a-z)

class AlphabetIterator:

    def __init__(self):
        self.current_letter = 'a'
        self.end_letter = 'z'

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_letter > self.end_letter:
            raise StopIteration
        letter = self.current_letter
        self.current_letter = chr(ord(self.current_letter) + 1)
        return letter

# Exemplu:
alphabet_iterator = AlphabetIterator()

for letter in alphabet_iterator:
    print(letter)


# # HOMEWORK_C10_EX02: Scrieti un generator pentru nr divizibile cu 3 din intervalul [a,b], unde a < b

# var 1 - funcție clasică
def divi_3_func(a,b):
    divi_lst = []
    for nr in range(a,b+1):
        if nr % 3 == 0:
            divi_lst.append(nr)
    print(divi_lst)

divi_3_func(20, 31)

# var 2 - generator
def divi_3_gen(a,b):
    for nr in range(a,b+1):
        if nr % 3 == 0:
            yield nr

for elem in divi_3_gen(20, 31):
    print(elem)

# # HOMEWORK_C10_EX03: Generator pentru primele n nr prime
# # def prime_generator(n):
# #     # codul aici

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def prime_generator(n):
    nr_of_prime = 0
    current_nr = 2

    while nr_of_prime < n:
        if is_prime(current_nr):
            yield current_nr
            nr_of_prime += 1
        current_nr += 1

# Exemplu:
n = 13

for nr in prime_generator(n):
    print(nr)


# HOMEWORK_C10_EX04: Scrieti 2 functii, una prin metoda clasica si una prin generatori de a obtine primele
# n numere din secventa lui Fibonacci
# secventa lui Fibonacci: 0,1,1,2,3,5,8,13,21,34
# fiecare numar din secv lui Fibo este generat ca fiind suma precedentelor 2 (incepe cu 0 si 1)
# def fibo_gen(n):
#     pass
#
# for n in fibo_gen(10):
#     print(n)
#
# # puteti returna si ca lista... ex: print(list(fibo_gen(10)))  => [0,1,1,2,3,5,8,13,21,34]

# var 1 - funcție clasică
def fibonacci_clasic(n):
    if n <= 0:
        return []

    fibonacci = [0, 1]
    while len(fibonacci) < n:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])

    return fibonacci[:n]

# Exemplu:
n = 8
print(fibonacci_clasic(n))

# var 2 - generator
def fibonacci_generator(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Exemplu:
n = 8
for numar in fibonacci_generator(n):
    print(numar)

# # HOMEWORK_C10_EX05: Scrieti un context manager care sa  printeze durata de executie a codului executat
# # sugestii: in metoda __enter__ salvati timestamp-ul curent, iar in __exit__ calculam diferenta dintre
# # momentul de iesire si cel de intrare

import time

class RunDuration:
    def __init__(self):
        pass

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        end_time = time.perf_counter()
        duration = end_time - self.start_time
        print(f"Programul a durat {duration:.5f} secunde")
        pass


with RunDuration() as run:
    time.sleep(5)

# # HOMEWORK_C10_EX06: Avand cele 2 functii, implementati tva_decorator astfel incat sa returneze pretul
# # produsului cu TVA adaugat (19%)
# @tva_decorator
# def get_phone_price(price):
#     print(f"Price of phone is: {price}RON")
#     return price
#
# @tva_decorator
# def get_laptop_price(price):
#     print(f"Price of phone is: {price}RON")
#     return price
#
# get_phone_price(3800)
# # Price of phone is: 3800
# # Price with TVA added is: 4522.0
#
# get_laptop_price(5500)
# # Price of laptop is: 5500
# # Price with TVA added is: 6545.0

def tva_decorator(func):
    def wrapper(price):
        price_with_tva = price * 1.19
        result = func(price)
        print(f"Price with TVA added is: {price_with_tva:.2f} RON")
        return result
    return wrapper

@tva_decorator
def get_phone_price(price):
    print(f"Price of phone is: {price} RON")
    return price

@tva_decorator
def get_laptop_price(price):
    print(f"Price of laptop is: {price} RON")
    return price

get_phone_price(3800)
# Price of phone is: 3800
# Price with TVA added is: 4522.0

get_laptop_price(5500)
# Price of laptop is: 5500
# Price with TVA added is: 6545.0

# # HOMEWORK_C10_EX07: Incercati sa mai adaugati un decorator celor 2 functii pentru a oferi un
# # discount (dat ca argument decoratorului) !necesita Google probabil :)

def tva_decorator(func):
    def wrapper(price):
        price_with_tva = price * 1.19
        result = func(price)
        print(f"Price with TVA added is: {price_with_tva:.2f} RON")
        return result
    return wrapper

def discount_decorator(discount):
    def decorator(func):
        def wrapper(price):
            discounted_price = price * (1 - discount)
            result = func(discounted_price)
            return result
        return wrapper
    return decorator

@discount_decorator(0.1)
@tva_decorator
def get_phone_price(price):
    print(f"Price of phone is: {price} RON")
    return price

@discount_decorator(0.15)
@tva_decorator
def get_laptop_price(price):
    print(f"Price of laptop is: {price} RON")
    return price

get_phone_price(3800)
# Price of phone is: 3420.0
# Price with TVA added is: 4070.8

get_laptop_price(5500)
# Price of laptop is: 4675.0
# Price with TVA added is: 5563.25