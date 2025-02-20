
# # Вказуємо шляхи до файлів
pdf_path = 'output/ДМКТ  лекція 1 презентація 2024 ч  1 .pdf'
csv_path = 'data_folder/лекція.csv'


import PyPDF2
import csv

# Функція для витягнення тексту з PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)  # Зберігаємо текст без змін
    return "\n".join(text)  # Об'єднуємо текст з усіх сторінок

# Перетворення тексту в CSV
def convert_text_to_csv(text, csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # Текст у лапках
        writer.writerow(['text'])  # Заголовок
        writer.writerow([text])  # Записуємо весь текст у одну клітинку

# Вказуємо шляхи до файлів

# Виконання процесу
text = extract_text_from_pdf(pdf_path)
convert_text_to_csv(text, csv_path)

print(f"✅ Конвертація завершена! Дані збережені в {csv_path}")


# import fitz  # PyMuPDF
# import csv
# import os

# # Функція для перевірки наявності директорії та створення, якщо вона відсутня
# def ensure_directory_exists(directory):
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#         print(f"✅ Директорію '{directory}' було створено.")
#     else:
#         print(f"✅ Директорія '{directory}' вже існує.")

# # Функція для витягнення тексту з PDF
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with fitz.open(pdf_path) as pdf:
#         for page in pdf:
#             text += page.get_text("text")
#     return text

# # Функція для конвертації тексту в CSV
# def convert_text_to_csv(text, csv_path):
#     lines = text.split('\n')
#     # Перевіряємо наявність директорії для CSV файлу
#     directory = os.path.dirname(csv_path)
#     ensure_directory_exists(directory)
    
#     with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['text'])  # Додаємо заголовок колонки
#         for line in lines:
#             writer.writerow([line])

# # Шляхи до файлів


# # Виконання процесу
# text = extract_text_from_pdf(pdf_path)
# convert_text_to_csv(text, csv_path)

# print(f"✅ Текст збережено у {csv_path}")



