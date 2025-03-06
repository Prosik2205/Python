# import fitz  # PyMuPDF
# import json
# import os

# # Функція для витягнення тексту з PDF
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with fitz.open(pdf_path) as pdf:
#         for page in pdf:
#             text += page.get_text("text")
#     return text

# # Функція для очищення тексту: видаляє порожні рядки та зайві пробіли
# def clean_text(text):
#     # Розділяємо на рядки
#     lines = text.split('\\n')
#     cleaned_lines = []
    
#     # Проходимо кожен рядок і фільтруємо порожні та непотрібні рядки
#     for line in lines:
#         cleaned_line = line.strip()  # Видалити зайві пробіли з початку і кінця рядка
#         if cleaned_line and len(cleaned_line.split()) > 1:  # Якщо рядок не порожній і має більше одного слова
#             cleaned_lines.append(cleaned_line)
    
#     # Об'єднуємо очищені рядки назад в один текст, кожен рядок знову розділений \\n
#     return "\\n".join(cleaned_lines)

# # Функція для конвертації очищеного тексту в JSON
# def convert_text_to_json(text, json_path):
#     # Розділяємо текст на речення за допомогою символу крапки
#     sentences = text.split('. ')
#     data = []
    
#     for sentence in sentences:
#         if sentence:  # Якщо речення не порожнє
#             data.append({"text": sentence.strip()})  # Додаємо в список з форматуванням
    
#     # Записуємо дані в JSON файл
#     with open(json_path, 'w', encoding='utf-8') as json_file:
#         json.dump(data, json_file, ensure_ascii=False, indent=4)
    
#     print(f"✅ Текст збережено у {json_path}")

# # Функція для обробки всіх PDF файлів у папці
# def process_pdfs_in_folder(input_folder, output_folder):
#     # Перевіряємо, чи існує папка для збереження результатів
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     # Перебираємо всі файли в папці
#     for file_name in os.listdir(input_folder):
#         # Перевіряємо, чи це PDF файл
#         if file_name.lower().endswith('.pdf'):
#             pdf_path = os.path.join(input_folder, file_name)
#             # Формуємо ім'я для JSON файлу (змінюємо розширення)
#             json_file_name = file_name.replace('.pdf', '.json')
#             json_path = os.path.join(output_folder, json_file_name)
            
#             # Витягуємо текст з PDF та конвертуємо в JSON
#             text = extract_text_from_pdf(pdf_path)
#             cleaned_text = clean_text(text)  # Очищаємо текст
#             convert_text_to_json(cleaned_text, json_path)  # Конвертуємо в JSON

# # Шляхи до папок
# input_folder = 'C:\\Users\\prosi\\Desktop\\VNS Data\\3 Курс\\1 Семестр\\Критичне мислення\\PDF'  # Папка з PDF файлами
# output_folder = 'C:\\Users\\prosi\\Desktop\\json\\Критичне мислення'  # Папка для збереження JSON файлів

# # Виконання процесу
# process_pdfs_in_folder(input_folder, output_folder)

# import json
# import os
# from docx import Document

# # Функція для витягнення тексту з DOCX
# def extract_text_from_docx(docx_path):
#     doc = Document(docx_path)
#     text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
#     return text

# # Функція для очищення тексту
# def clean_text(text):
#     lines = text.split('\n')
#     cleaned_lines = [line.strip() for line in lines if line.strip()]
#     return "\n".join(cleaned_lines)

# # Функція для конвертації тексту в JSON
# def convert_text_to_json(text, json_path):
#     sentences = text.split('\n')  # Розбиваємо текст по рядках
#     data = [{"text": sentence.strip()} for sentence in sentences if sentence.strip()]

#     # Запис у JSON
#     with open(json_path, 'w', encoding='utf-8') as json_file:
#         json.dump(data, json_file, ensure_ascii=False, indent=4)
    
#     print(f"✅ Текст збережено у {json_path}")

# # Шлях до вхідної папки з DOCX файлами
# input_folder = "C:\\Users\\prosi\\Desktop\\VNS Data\\2 Курс\\1 Семестр\\С++\\DOCX"
# output_folder = "C:\\Users\\prosi\\Desktop\\json\\С++"

# # Переконуємося, що вихідна папка існує
# os.makedirs(output_folder, exist_ok=True)

# # Проходження по всіх файлах у вхідній папці
# for filename in os.listdir(input_folder):
#     if filename.endswith(".docx"):
#         docx_path = os.path.join(input_folder, filename)
#         json_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.json")

#         text = extract_text_from_docx(docx_path)
#         cleaned_text = clean_text(text)
#         convert_text_to_json(cleaned_text, json_path)



INPUT_FOLDER = "C:\\Users\\prosi\\Desktop\\test\\ТІМС(R)"  # Вхідна папка з JSON файлами
OUTPUT_FOLDER = "C:\\Users\\prosi\\Desktop\\test\\test"  # Папка для відформатованих файлів

import os
import json


MAX_LENGTH = 1000  # Довжина одного текстового фрагмента

os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # Створюємо папку, якщо її немає

def split_text_into_chunks(text, max_length=MAX_LENGTH):
    """Розбиває текст на рівні частини (~100 символів), не рвучи слова."""
    words = text.split()
    result = []
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) + 1 <= max_length:
            current_chunk += " " + word if current_chunk else word
        else:
            result.append(current_chunk.strip())
            current_chunk = word

    if current_chunk:
        result.append(current_chunk.strip())

    return result

# Обробка всіх JSON-файлів у папці
for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".json"):
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        with open(input_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Об'єднуємо всі текстові дані в один великий рядок
        full_text = " ".join(entry["text"] for entry in data if "text" in entry)

        # Ділимо на рівномірні частини
        formatted_chunks = split_text_into_chunks(full_text)

        # Записуємо у новий JSON
        formatted_data = [{"text": chunk} for chunk in formatted_chunks]

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(formatted_data, file, ensure_ascii=False, indent=4)

        print(f"✅ Оброблено: {filename} -> {output_path}")




