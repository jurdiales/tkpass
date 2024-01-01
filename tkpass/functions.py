import random
from random import randint
import math

G_NUMBER_N_SET = 10
G_LOWER_N_SET = 26
G_UPPER_N_SET = 26
G_SYMBOL_SET = [35, 36, 37, 38, 40, 41, 42, 43, 45, 46, 47, 58, 59, 61, 63, 64, 91, 92, 93, 123, 124, 125]
G_SYMBOL_N_SET = len(G_SYMBOL_SET)
G_ALL_N_SET = 94

def g_number():     return chr(randint(48, 57))
def g_lower_case(): return chr(randint(97, 122))
def g_upper_case(): return chr(randint(65, 90))
def g_symbol():     return chr(random.choice(G_SYMBOL_SET))
def g_all_printable(): return chr(randint(33, 126))

def generate_password(length: int, lowers: bool, numbers: bool, uppers: bool, symbols: bool) -> str:
    password = []
    options = []
    pool_size = 0

    # add possible generators
    if lowers: 
        options.append(g_lower_case)
        pool_size += G_LOWER_N_SET
    if numbers: 
        options.append(g_number)
        pool_size += G_NUMBER_N_SET
    if uppers: 
        options.append(g_upper_case)
        pool_size += G_UPPER_N_SET
    if symbols: 
        options.append(g_symbol)
        pool_size += G_SYMBOL_N_SET
    # only lower cases if none selected
    if len(options) == 0: 
        options.append(g_lower_case)
        pool_size += G_LOWER_N_SET

    for _ in range(length):
        password.append(random.choice(options)())
    random.shuffle(password)

    return ''.join(password), password_entropy(length, pool_size)

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n

def password_entropy(length: int, pool_size: int) -> int:
    """
    E = log2(S^L)
    Where S is the size of the pool of unique possible symbols (character set)
    and L is the password length or number of symbols in the password
    """
    return int(math.ceil( math.log2(math.pow(pool_size, length)) ))
