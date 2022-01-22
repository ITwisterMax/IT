from cipher import *


public_key = private_key = None

def show_menu():
    """Функция отображения главного меню"""
    print("""
    1. Сгенерировать ключи случайно.
    2. Сгенерировать ключи по известным значениям. 
    3. Отобразить ключи.
    4. Шифровать сообщение.
    5. Дешифровать сообщение.
    6. Выход из программы.
        """)
    return input("Введите номер команды: ")

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

def get_randkey():
    """Функция генерации случайных ключей"""
    try:
        public, private = get_keys()
        print("\nКлючи успешно сгенерированы!")
    except:
        print("Ошибка ввода!")
    else:
        global public_key, private_key
        public_key = public
        private_key = private

def get_paramkey():
    """Функция генерации ключей по известным значениям."""
    try:
        p = int(input("\nВведите число p: "))
        q = int(input("Введите число q: "))
        e = int(input("Введите число e: "))
        d = int(input("Введите число d: "))
        public = PublicKey(p, q, e)
        private = PrivateKey(p, q, d)
        print("Ключи успешно сгенерированы!")
    except:
        print("Ошибка ввода!")
    else:
        global public_key, private_key
        public_key = public
        private_key = private

def print_keys():
    """Функция отображения ключей"""
    global public_key, private_key
    if public_key and private_key:
        print("\nОткрытый ключ:", public_key)
        print("Закрытый ключ:", private_key)
    else:
        print("\nКлючи не сгенерированы!")

def encrypt():
    """Функция шифрования"""
    global public_key, private_key
    if public_key and private_key:
        try:
            message = input("\nВведите сообщение: ")
            emessage = public_key.encrypt(message)
        except:
            print("Ошибка ввода!")
        else:
            print("Зашифрованное сообщение:", emessage)
    else:
        print("\nКлючи не сгенерированы!")

def decrypt():
    """Функция дешифрования"""
    global public_key, private_key
    if public_key and private_key:
        try:
        	message = input("\nВведите сообщение: ")
        	dmessage = private_key.decrypt(message)
        except:
            print("Ошибка ввода!")
        else:
        	print("Расшифрованное сообщение:", dmessage)
    else:
        print("\nКлючи не сгенерированы!")


if __name__ == "__main__":
    while True:
        x = show_menu()
        if x == "1":
            get_randkey()
        elif x == "2":
            get_paramkey()
        elif x == "3":
            print_keys()
        elif x == "4":
            encrypt()
        elif x == "5":
            decrypt()
        elif x == "6":
            break
        else:
            print("Ошибка, повторите ввод...")

# p = 631
# q = 839
# n = 529409
# f = 527940
# e = 457
# d = 442453
