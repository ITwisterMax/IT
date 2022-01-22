using Microsoft.Win32;
using System;
using System.Text;
using System.Windows;

namespace Laba4
{
    // Главное окно
    public partial class MainWindow : Window
    {
        // Путь к исходному файлу
        public static string src;
        // Путь к новому файлу
        public static string dest;

        // Конструктор
        public MainWindow()
        {
            InitializeComponent();
        }

        // Шифрование / Дешифрование
        private void encrypt_decrypt_Click(object sender, RoutedEventArgs e)
        {
            // Проверка на корректность введенных данных
            if (isDataCorrect())
            {
                // Начальное состояние регистра
                ulong inputKey = Convert.ToUInt64(key.Text);
                LFSR.register = inputKey;

                // Шифрование / Дешифрование
                LFSR.Encrypt(src, dest);
                MessageBox.Show("Файл был успешно обработан!", "Система потокового шифрования файлов");
            }
        }

        // Считывание путь к исходному файлу
        private void src_button_Click(object sender, RoutedEventArgs e)
        {
            string path = "";
            OpenFileDialog openFileDialog = new OpenFileDialog();
            if (openFileDialog.ShowDialog() == true)
            {
                path = openFileDialog.FileName;
            }
            src = path;
            srcPath.Text = src;
        }

        // Считывание путь к новому файлу
        private void dest_button_Click(object sender, RoutedEventArgs e)
        {
            string path = "";
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            if (saveFileDialog.ShowDialog() == true)
            {
                path = saveFileDialog.FileName;
            }
            dest = path;
            destPath.Text = dest;
        }

        // Проверка введенных данных
        private bool isDataCorrect()
        {
            try
            {
                ulong data = Convert.ToUInt64(key.Text);
                return true;
            }
            catch
            {
                MessageBox.Show("Ошибка... Проверьте введенные данные!", "Система потокового шифрования файлов");
                return false;
            }
        }
    }
}
