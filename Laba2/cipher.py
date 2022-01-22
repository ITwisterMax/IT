import random
from collections import namedtuple
from abc import ABC, abstractmethod


class General(ABC):
    """Общий класс для ключей"""

    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ!?,.()0123456789 "

    @staticmethod
    def quick_pow(base, power, module):
        """Функция быстрого возведения в степень"""
        power = bin(power)[2:]
        res = 1
        for i in range(len(power) - 1, -1, -1):
            res = (res * base ** int(power[i])) % module
            base = (base ** 2) % module
        return res

    @abstractmethod
    def encrypt(self, x):
        """Функция шифрования"""
        pass

    @abstractmethod
    def decrypt(self, x):
        """Функция дешифрования"""
        pass


class PublicKey(General, namedtuple("PublicKey", "p q e")):
    """Открытый ключ, использующийся для шифрования сообщения"""

    def encrypt(self, x):
        for i in x:
            if i not in self.alphabet:
                raise ValueError("Error!")
        """Функция шифрования. Параметр: x - сообщение"""
        return " ".join([str(self.quick_pow(i, self.e, self.p * self.q)) for i in [self.alphabet.index(j) for j in list(x)]])


class PrivateKey(General, namedtuple("PrivateKey", "p q d")):
    """Закрытый ключ, использующийся для дешифрования сообщения"""

    def decrypt(self, x):
        for i in x:
            if i not in self.alphabet:
                raise ValueError("Error!")
        """Функция дешифрования. Параметр: x - сообщение"""
        return "".join([self.alphabet[self.quick_pow(i, self.d, self.p * self.q)] for i in [int(j) for j in x.split(" ")]])


def get_primes(start, stop):
    """Функция получения списка простых чисел"""
    # Формирование начального списка
    if start >= stop:
        return []
    primes = [2]
    # Формирование списка простых чисел до значения stop
    for i in range(3, stop + 1, 2):
        for j in primes:
            if i % j == 0:
                break
        else:
            primes.append(i)
    # Формирование списка простых чисел от значения start
    while primes and primes[0] < start:
        del primes[0]
    return primes

def gcdex(a, b):
    """Расширенный алгоритм Евклида"""
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = gcdex(b, a % b)
        return d, y, x - y * (a // b)

def get_keys():
    """Функция получения открытого и закрытого ключа"""
    # Диапазон допустимых значений для числа n
    length = 30
    n_min = 1 << (length - 1)
    n_max = (1 << length) - 1
    # Диапазон допустимых значений для чисел p и q
    start = 1 << (length // 2 - 1)
    stop = 1 << (length // 2 + 1)
    # Получение простых чисел в диапазоне от start до stop
    primes = get_primes(start, stop)
    # Получение чисел p и q из списка простых чисел
    while primes:
        p = random.choice(primes)
        primes.remove(p)
        tmp = [q for q in primes if n_min <= p * q <= n_max]
        if tmp:
            q = random.choice(tmp)
            break
    else:
        raise ValueError("Error!")
    # Получение числа f
    f = (p - 1) * (q - 1)
    # Получение числа e
    count = 0
    while count < f - 2:
        count += 1
        e = random.randrange(3, f)
        gcd, x, y = gcdex(e, f)
        if gcd == 1:
            break
    else:
        raise ValueError("Error!")
    # Получение числа d
    gcd, x, y = gcdex(e, f)
    if gcd == 1:
        d = f + x if x < 0 else x
    else:
        raise ValueError("Error!")
    # Формирование открытого и закрытого ключа
    return PublicKey(p, q, e), PrivateKey(p, q, d)
