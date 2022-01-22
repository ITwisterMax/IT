from ciphers import *
from kivy.app import App
from kivy.config import Config

# Настройки окна
Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 800)
Config.set("graphics", "height", 600)

from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput


class CiphersApp(App):
    """Основной класс"""

    def start_encrypt(self, instance):
        """Функция шифрования текста"""
        if self.method_input.text == "Метод железнодорожной изгороди":
            tmp = Rail_fence(self.key_input.text)
            output = tmp.encrypt(self.etext_input.text)
            self.dtext_input.text = output
        elif self.method_input.text == "Столбцовый метод":
            tmp = Column(self.key_input.text)
            output = tmp.encrypt(self.etext_input.text)
            self.dtext_input.text = output
        elif self.method_input.text == "Метод поворачивающейся решетки":
            tmp = Trailing_grille(self.key_input.text)
            output = tmp.encrypt(self.etext_input.text)
            self.dtext_input.text = output
        elif self.method_input.text == "Метод Плейфейра":
            tmp = Playfair(self.key_input.text)
            output = tmp.encrypt(self.etext_input.text)
            self.dtext_input.text = output

    def start_decrypt(self, instance):
        """Функция дешифровки текста"""
        if self.method_input.text == "Метод железнодорожной изгороди":
            tmp = Rail_fence(self.key_input.text)
            output = tmp.decrypt(self.etext_input.text)
            self.dtext_input.text = output
        elif self.method_input.text == "Столбцовый метод":
            tmp = Column(self.key_input.text)
            output = tmp.decrypt(self.etext_input.text)
            self.dtext_input.text = output
        elif self.method_input.text == "Метод поворачивающейся решетки":
            tmp = Trailing_grille(self.key_input.text)
            output = tmp.decrypt(self.etext_input.text)
            self.dtext_input.text = output
        elif self.method_input.text == "Метод Плейфейра":
            tmp = Playfair(self.key_input.text)
            output = tmp.decrypt(self.etext_input.text)
            self.dtext_input.text = output

    def build(self):
        """Функция отображенияя элементов"""
        layout = FloatLayout()
        method_list = DropDown()
        btn1 = Button(
            text="Метод железнодорожной изгороди",
            size_hint_y=None,
            height=60,
            font_size=30,
        )
        btn2 = Button(
            text="Столбцовый метод", size_hint_y=None, height=60, font_size=30
        )
        btn3 = Button(
            text="Метод поворачивающейся решетки",
            size_hint_y=None,
            height=60,
            font_size=30,
        )
        btn4 = Button(text="Метод Плейфейра", size_hint_y=None, height=60, font_size=30)
        for i in (btn1, btn2, btn3, btn4):
            i.bind(on_release=lambda i: method_list.select(i.text))
            method_list.add_widget(i)
        method_input = Button(
            text="Выберите метод...",
            font_size=30,
            size_hint=(0.9, 0.1),
            pos_hint={"x": 0.05, "y": 0.85},
        )
        method_input.bind(on_release=method_list.open)
        method_list.bind(on_select=lambda instance, x: setattr(method_input, "text", x))
        key_input = TextInput(
            text="Поле для ключа",
            font_size=30,
            size_hint=(0.9, 0.1),
            pos_hint={"x": 0.05, "y": 0.65},
        )
        etext_input = TextInput(
            text="Поле для ввода",
            font_size=30,
            size_hint=(0.9, 0.1),
            pos_hint={"x": 0.05, "y": 0.45},
        )
        dtext_input = TextInput(
            text="Поле для вывода",
            font_size=30,
            size_hint=(0.9, 0.1),
            pos_hint={"x": 0.05, "y": 0.25},
        )
        encrypt_btn = Button(
            text="Шифровать",
            font_size=30,
            size_hint=(0.4, 0.1),
            pos_hint={"x": 0.05, "y": 0.05},
            on_press=self.start_encrypt,
        )
        decrypt_btn = Button(
            text="Дешифровать",
            font_size=30,
            size_hint=(0.4, 0.1),
            pos_hint={"x": 0.55, "y": 0.05},
            on_press=self.start_decrypt,
        )
        # Добавление элементов
        layout.add_widget(method_input)
        layout.add_widget(key_input)
        layout.add_widget(etext_input)
        layout.add_widget(dtext_input)
        layout.add_widget(encrypt_btn)
        layout.add_widget(decrypt_btn)
        # Сохранение значений
        self.method_input = method_input
        self.key_input = key_input
        self.etext_input = etext_input
        self.dtext_input = dtext_input
        return layout


if __name__ == "__main__":
    CiphersApp().run()
