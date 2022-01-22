from abc import ABC, abstractmethod


class Abstract(ABC):
    """Общий класс для всех методов шифрования"""

    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя()!?., "

    @staticmethod
    def check_language(text: str, alph: str):
        """Проверка языка текста. Параметры: text - исходный текст, alph - алфавит"""
        for i in text:
            if i not in alph:
                return False
        return True

    @abstractmethod
    def encrypt(self, etext: str):
        """Функция шифрования"""
        pass

    @abstractmethod
    def decrypt(self, dtext: str):
        """Функция дешифровки"""
        pass


class Rail_fence(Abstract):
    """Шифрование методом железнодорожной изгороди. Параметр: key - ключ"""

    def __init__(self, key: str):
        key = key.strip()
        if (not key) or (not key.isdigit()) or (int(key) < 2):
            self.key = "ValueError!"
        else:
            self.key = int(key)

    def __create_array(self, size: int):
        """Создание 'карты' шифрования. Параметр: size - количество элементов текста"""
        period = 2 * (self.key - 1)
        array = [[] for i in range(self.key)]
        # Формирование карты основано на взятии остатка
        for i in range(size):
            mod = i % period
            j = mod if mod < self.key - 1 else period - mod
            array[j].append(i)
        return array

    def encrypt(self, rf_etext: str):
        """Шифрование текста. Параметр: rf_etext - входная строка"""
        if not rf_etext.strip():
            return ""
        rf_etext = rf_etext.lower()
        if (self.key == "ValueError!") or (
            not self.check_language(rf_etext, self.alphabet)
        ):
            return "ValueError!"
        tmp = self.__create_array(len(rf_etext))
        rf_eres = ""
        for row in tmp:
            for element in row:
                rf_eres += rf_etext[element]
        return rf_eres

    def decrypt(self, rf_dtext: str):
        """Дешифровка текста. Параметр: rf_dtext - входная строка"""
        if not rf_dtext.strip():
            return ""
        rf_dtext = rf_dtext.lower()
        if (self.key == "ValueError!") or (
            not self.check_language(rf_dtext, self.alphabet)
        ):
            return "ValueError!"
        tmp = self.__create_array(len(rf_dtext))
        rf_dres = [""] * len(rf_dtext)
        i = 0
        for row in tmp:
            for element in row:
                rf_dres[element] = rf_dtext[i]
                i += 1
        return "".join(rf_dres)


class Column(Abstract):
    """Шифрование столбцовым методом. Параметр: key - ключ"""

    @staticmethod
    def __create_key(key: list):
        """Преобразование ключа в порядок чтения столбцов. Параметр: key - ключ"""
        tmp = [(key[i], i) for i in range(len(key))]
        tmp.sort(key=lambda i: i[0])
        res = [0] * len(tmp)
        for i in range(len(tmp)):
            res[tmp[i][1]] = i
        return res

    def __init__(self, key: str):
        key = key.replace(" ", "").lower()
        if (
            (not key)
            or (len(key) < 2)
            or (not self.check_language(key, self.alphabet[:33]))
        ):
            self.key = "ValueError!"
        else:
            self.key = self.__create_key(key)

    def __create_array(self, size: int):
        """Создание 'карты' шифрования. Параметр: size - количество элементов текста"""
        width = len(self.key)
        height = size // width + 1
        array = [[-1] * width for i in range(height)]
        position = step = 0
        # Формирование карты основано на поочередном заполнении столбцов в соответствии с ключом
        for step in range(width):
            i = 0
            j = self.key.index(step)
            while i < height and (i * width + j < size):
                array[i][j] = position
                position += 1
                i += 1
        return array

    def encrypt(self, c_etext: str):
        """Шифрование текста. Параметр: c_etext - входная строка"""
        if not c_etext.strip():
            return ""
        c_etext = c_etext.lower()
        if (self.key == "ValueError!") or (
            not self.check_language(c_etext, self.alphabet)
        ):
            return "ValueError!"
        tmp = self.__create_array(len(c_etext))
        c_eres = [""] * len(c_etext)
        i = 0
        for row in tmp:
            for element in row:
                if element != -1:
                    c_eres[element] = c_etext[i]
                    i += 1
        return "".join(c_eres)

    def decrypt(self, c_dtext: str):
        """Дешифровка текста. Параметр: c_dtext - входная строка"""
        if not c_dtext.strip():
            return ""
        c_dtext = c_dtext.lower()
        if (self.key == "ValueError!") or (
            not self.check_language(c_dtext, self.alphabet)
        ):
            return "ValueError!"
        tmp = self.__create_array(len(c_dtext))
        c_dres = ""
        for row in tmp:
            for element in row:
                if element != -1:
                    c_dres += c_dtext[element]
        return c_dres


class Trailing_grille(Abstract):
    """Шифрование методом поворачивающейся решетки. Параметр: key - ключ"""

    alph = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    @staticmethod
    def __create_key(key: str):
        """Проверка и создание ключа. Параметр: key - ключ"""
        if (not key.replace(" ", "")) or (not key.replace(" ", "").isdigit()):
            return "ValueError!"
        key = key.split()
        if len(key) < 2:
            return "ValueError!"
        for i in range(len(key)):
            key[i] = int(key[i])
            if key[i] not in range(5):
                return "ValueError!"
        return key

    @staticmethod
    def __create_n(size: int):
        """Проверка и создание размерности. Параметр: size - размер ключа"""
        if int((size * 4) ** 0.5) == ((size * 4) ** 0.5):
            return int((size * 4) ** 0.5)
        elif int((size * 4 - 3) ** 0.5) == ((size * 4 - 3) ** 0.5):
            return int((size * 4 - 3) ** 0.5)
        else:
            return 0

    @staticmethod
    def __create_input_matrix(size: int):
        """Создание матрицы позиций. Параметр: size - размер матрицы"""
        res = [[0] * size for i in range(size)]
        max_counter = 1
        # Заполняем по границе нужными числами и уменьшаем границу на 1
        for k in range(size // 2):
            for step in range(5):
                counter = max_counter
                if step == 1:
                    for j in range(k, size - k - 1):
                        res[k][j] = counter
                        counter += 1
                elif step == 2:
                    for i in range(k, size - k - 1):
                        res[i][size - k - 1] = counter
                        counter += 1
                elif step == 3:
                    for j in range(size - k - 1, k, -1):
                        res[size - k - 1][j] = counter
                        counter += 1
                elif step == 4:
                    for i in range(size - k - 1, k, -1):
                        res[i][k] = counter
                        counter += 1
                    max_counter = counter
        # Если нужно, ставим центральный элемент
        if size % 2:
            res[size // 2][size // 2] = max_counter
        return res

    @staticmethod
    def __create_template(n: int, size: int, key: list, matrix: list):
        """Создание матрицы-трафарета. Параметры: n - размер матрицы,
        size - размер ключа, key - ключ, matrix - матрица позиций"""
        res = [[0] * n for i in range(n)]
        curr_i = curr_j = 0
        # Ищем нужную позицию и ставим в результирующей матрице 1
        for k in range(1, size + 1):
            is_found = False
            for i in range(n):
                for j in range(n):
                    if matrix[i][j] == k:
                        curr_i = i
                        curr_j = j
                        is_found = True
                        break
                if is_found:
                    break
            if key[k - 1] == 1:
                res[curr_i][curr_j] = 1
            elif key[k - 1] == 2:
                res[curr_j][n - curr_i - 1] = 1
            elif key[k - 1] == 3:
                res[n - curr_i - 1][n - curr_j - 1] = 1
            elif key[k - 1] == 4:
                res[n - curr_j - 1][curr_i] = 1
        return res

    def __init__(self, key: str):
        self.key = self.__create_key(key)
        if self.key != "ValueError!":
            self.n = self.__create_n(len(self.key))
        else:
            self.n = 0
        if self.key != "ValueError!" and self.n != 0:
            self.input_matrix = self.__create_input_matrix(self.n)
            self.template = self.__create_template(
                self.n, len(self.key), self.key, self.input_matrix
            )

    def encrypt(self, tg_etext: str):
        """Шифрование текста. Параметр: tg_etext - входная строка"""
        if not tg_etext.strip():
            return ""
        tg_etext = tg_etext.lower()
        if (
            (self.key == "ValueError!")
            or (self.n == 0)
            or (not self.check_language(tg_etext, self.alphabet))
        ):
            return "ValueError!"
        out = ""
        inalph = 0
        tmp = curr = tg_etext
        while len(tmp):
            res = [[0] * self.n for i in range(self.n)]
            # Разбиение текста на блоки и его дополнение прочими символами
            if len(tmp) > self.n ** 2:
                curr = curr[: self.n ** 2]
                tmp = tmp[self.n ** 2 :]
            else:
                curr = tmp
                while len(curr) < self.n ** 2:
                    curr += self.alph[inalph]
                    inalph += 1
                tmp = ""
            count = 0
            # Шифрование основано на повороте трафарета вправо 4 раза
            for step in range(1, 5):
                if step == 1:
                    for i in range(self.n):
                        for j in range(self.n):
                            if self.template[i][j]:
                                res[i][j] = curr[count]
                                count += 1
                elif step == 2:
                    for i in range(self.n):
                        for j in range(self.n):
                            if self.template[self.n - j - 1][i] and not (
                                (i == self.n // 2)
                                and (j == self.n // 2)
                                and (self.n % 2)
                            ):
                                res[i][j] = curr[count]
                                count += 1
                elif step == 3:
                    for i in range(self.n):
                        for j in range(self.n):
                            if self.template[self.n - i - 1][self.n - j - 1] and not (
                                (i == self.n // 2)
                                and (j == self.n // 2)
                                and (self.n % 2)
                            ):
                                res[i][j] = curr[count]
                                count += 1
                elif step == 4:
                    for i in range(self.n):
                        for j in range(self.n):
                            if self.template[j][self.n - i - 1] and not (
                                (i == self.n // 2)
                                and (j == self.n // 2)
                                and (self.n % 2)
                            ):
                                res[i][j] = curr[count]
                                count += 1
            out += "".join("".join(x) for x in res)
        return out

    def decrypt(self, tg_dtext: str):
        """Дешифровка текста. Параметр: tg_dtext - входная строка"""
        if not tg_dtext.strip():
            return ""
        if (
            (self.key == "ValueError!")
            or (self.n == 0)
            or (not self.check_language(tg_dtext.lower(), self.alphabet))
        ):
            return "ValueError!"
        out = ""
        inalph = 0
        tmp = curr = tg_dtext
        while len(tmp):
            res = [[0] * self.n for i in range(self.n)]
            # Разбиение текста на блоки и его дополнение прочими символами
            count = 0
            if len(tmp) > self.n ** 2:
                curr = curr[: self.n ** 2]
                for i in range(self.n):
                    for j in range(self.n):
                        res[i][j] = curr[count]
                        count += 1
                tmp = tmp[self.n ** 2 :]
            else:
                curr = tmp
                while len(curr) < self.n ** 2:
                    curr += self.alph[inalph]
                    inalph += 1
                for i in range(self.n):
                    for j in range(self.n):
                        res[i][j] = curr[count]
                        count += 1
                tmp = ""
            count = 0
            # Дешифровка основана на повороте трафарета вправо 4 раза
            for step in range(1, 5):
                if step == 1:
                    for i in range(self.n):
                        for j in range(self.n):
                            if self.template[i][j]:
                                out += res[i][j]
                                count += 1
                elif step == 2:
                    for i in range(self.n):
                        for j in range(self.n):
                            if self.template[self.n - j - 1][i] and not (
                                (i == self.n // 2)
                                and (j == self.n // 2)
                                and (self.n % 2)
                            ):
                                out += res[i][j]
                                count += 1
                elif step == 3:
                    for i in range(self.n):
                        for j in range(self.n):
                            if self.template[self.n - i - 1][self.n - j - 1] and not (
                                (i == self.n // 2)
                                and (j == self.n // 2)
                                and (self.n % 2)
                            ):
                                out += res[i][j]
                                count += 1
                elif step == 4:
                    for i in range(self.n):
                        for j in range(self.n):
                            if self.template[j][self.n - i - 1] and not (
                                (i == self.n // 2)
                                and (j == self.n // 2)
                                and (self.n % 2)
                            ):
                                out += res[i][j]
                                count += 1
        # Удаление лишних символов
        for i in out:
            if i in self.alph:
                out = out.replace(i, "")
        return out


class Playfair(Abstract):
    """Шифрование методом Плейфейра. Параметр: key - ключ"""

    @staticmethod
    def __edit_key(key: str):
        """Исключение из ключа повторяющихся символов. Параметр: key - ключ"""
        newkey = ""
        for sym in key:
            if sym not in newkey:
                newkey += sym
        return newkey

    def __make_alphabet(self, key: str):
        """Создание закрытого алфавита. Параметр: key - ключ"""
        alph = key
        for sym in self.alphabet:
            if sym not in alph:
                alph += sym
        return alph

    def __init__(self, key: str):
        key = key.lower()
        if (not key.strip()) or (not self.check_language(key, self.alphabet)):
            self.key = "ValueError!"
        else:
            key = self.__edit_key(key)
            self.key = self.__make_alphabet(key)

    def __encrypt_b(self, p_ebigr: str):
        """Шифрование биграмм. Параметр p_ebigr - биграмма"""
        first_x, first_y = (
            self.key.index(p_ebigr[0]) % 5,
            self.key.index(p_ebigr[0]) // 5,
        )
        second_x, second_y = (
            self.key.index(p_ebigr[1]) % 5,
            self.key.index(p_ebigr[1]) // 5,
        )
        # Проверка на совпадение строк
        if first_y == second_y:
            first_x = (first_x + 1) % 5
            second_x = (second_x + 1) % 5
        # Проверка на совпадение столбцов
        elif first_x == second_x:
            first_y = (first_y + 1) % 8
            second_y = (second_y + 1) % 8
        # Замена столбцов
        else:
            first_x, second_x = second_x, first_x
        return self.key[first_y * 5 + first_x] + self.key[second_y * 5 + second_x]

    def __decrypt_b(self, p_dbigr: str):
        """Дешифровка биграмм. Параметр dbigr - биграмма"""
        first_x, first_y = (
            self.key.index(p_dbigr[0]) % 5,
            self.key.index(p_dbigr[0]) // 5,
        )
        second_x, second_y = (
            self.key.index(p_dbigr[1]) % 5,
            self.key.index(p_dbigr[1]) // 5,
        )
        # Проверка на совпадение строк
        if first_y == second_y:
            first_x = (first_x - 1) % 5
            second_x = (second_x - 1) % 5
        # Проверка на совпадение столбцов
        elif first_x == second_x:
            first_y = (first_y - 1) % 8
            second_y = (second_y - 1) % 8
        # Замена столбцов
        else:
            first_y, second_y = second_y, first_y
        return self.key[first_y * 5 + first_x] + self.key[second_y * 5 + second_x]

    def encrypt(self, p_etext: str):
        """Шифрование текста. Параметр: p_etext - входная строка"""
        if not p_etext.strip():
            return ""
        p_etext = p_etext.lower()
        if (self.key == "ValueError!") or (
            not self.check_language(p_etext, self.alphabet)
        ):
            return "ValueError!"
        # Разбиваем на биграммы и шифруем их
        if len(p_etext) % 2 == 1:
            p_etext += "ь"
        p_eres = ""
        length = len(p_eres)
        while length < len(p_etext) - 1:
            if p_etext[length] == p_etext[length + 1]:
                p_etext = p_etext[: length + 1] + "ьь" + p_etext[length + 1 :]
            p_eres += self.__encrypt_b(p_etext[length : length + 2])
            length = len(p_eres)
        return p_eres

    def decrypt(self, p_dtext: str):
        """Дешифровка текста. Параметр: p_dtext - входная строка"""
        if not p_dtext.strip():
            return ""
        p_dtext = p_dtext.lower()
        if (self.key == "ValueError!") or (
            not self.check_language(p_dtext, self.alphabet)
        ):
            return "ValueError!"
        # Разбиваем на биграммы и дешифруем их
        p_dres = ""
        length = len(p_dres)
        while length < len(p_dtext) - 1:
            p_dres += self.__decrypt_b(p_dtext[length : length + 2])
            length = len(p_dres)
        p_dres = p_dres.replace("ьь", "")
        return p_dres if p_dres[len(p_dres) - 1] != "ь" else p_dres[: len(p_dres) - 1]