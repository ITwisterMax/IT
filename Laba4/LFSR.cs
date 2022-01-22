using System;
using System.IO;
using System.Windows;

namespace Laba4
{
    class LFSR
    {
        // Размер буфера для чтения
        private const int BUFFER_SIZE = 4096;
        // Количество бит в слове
        private const int BITS_NUM = 8;
        // Регистр сдвига
        public static ulong register;               

        // Шифрование
        public static void Encrypt(string src, string dest)
        {
            // Исходный файл
            BinaryReader reader = new BinaryReader(File.Open(src, FileMode.Open));
            // Новый файл
            BinaryWriter writer = new BinaryWriter(File.Open(dest, FileMode.Create));

            // Буфер
            byte[] buffer = new byte[BUFFER_SIZE];
            // Количество прочитанных байт
            int readBytes;

            try
            {
                do
                {   
                    // Считывание байтов из файла в буфер
                    readBytes = reader.Read(buffer, 0, BUFFER_SIZE);

                    // Шифрование считанной части
                    for (int i = 0; i < BUFFER_SIZE; i++)
                    {
                        for (int j = 0; j < BITS_NUM; j++)
                        {
                            buffer[i] = (byte)(buffer[i] ^ (CreateKey() << (8 - j)));
                        }
                    }

                    // Запись зашифрованной части
                    writer.Write(buffer, 0, readBytes);
                } while (readBytes > 0);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
            finally
            {
                reader.Close();
                writer.Close();
            }
        }

        // Получение очередного бита в зависимости от входного ключа (x^25 + x^3 + 1)
        private static ulong CreateKey()
        {
            register = ((((register >> 0) ^ (register >> 3)) & 0x1) << 24) | (register >> 1);
            return register & 0x1;
        }
    }
}
