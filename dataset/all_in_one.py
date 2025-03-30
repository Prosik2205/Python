############################################################################_PDF_######################################################################
import fitz  # PyMuPDF
import json
import os

# Функція для витягнення тексту з PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text("text")
    return text

# Функція для очищення тексту: видаляє порожні рядки та зайві пробіли
def clean_text(text):
    # Розділяємо на рядки
    lines = text.split('\\n')
    cleaned_lines = []
    
    # Проходимо кожен рядок і фільтруємо порожні та непотрібні рядки
    for line in lines:
        cleaned_line = line.strip()  # Видалити зайві пробіли з початку і кінця рядка
        if cleaned_line and len(cleaned_line.split()) > 1:  # Якщо рядок не порожній і має більше одного слова
            cleaned_lines.append(cleaned_line)
    
    # Об'єднуємо очищені рядки назад в один текст, кожен рядок знову розділений \\n
    return "\\n".join(cleaned_lines)

# Функція для конвертації очищеного тексту в JSON
def convert_text_to_json(text, json_path):
    # Розділяємо текст на речення за допомогою символу крапки
    sentences = text.split('. ')
    data = []
    
    for sentence in sentences:
        if sentence:  # Якщо речення не порожнє
            data.append({"text": sentence.strip()})  # Додаємо в список з форматуванням
    
    # Записуємо дані в JSON файл
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    print(f"✅ Текст збережено у {json_path}")

# Функція для обробки всіх PDF файлів у папці
def process_pdfs_in_folder(input_folder, output_folder):
    # Перевіряємо, чи існує папка для збереження результатів
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Перебираємо всі файли в папці
    for file_name in os.listdir(input_folder):
        # Перевіряємо, чи це PDF файл
        if file_name.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_folder, file_name)
            # Формуємо ім'я для JSON файлу (змінюємо розширення)
            json_file_name = file_name.replace('.pdf', '.json')
            json_path = os.path.join(output_folder, json_file_name)
            
            # Витягуємо текст з PDF та конвертуємо в JSON
            text = extract_text_from_pdf(pdf_path)
            cleaned_text = clean_text(text)  # Очищаємо текст
            convert_text_to_json(cleaned_text, json_path)  # Конвертуємо в JSON

# Шляхи до папок
input_folder = 'C:\\Users\\prosi\\Desktop\\VNS Data\\3 Курс\\1 Семестр\\Критичне мислення\\PDF'  # Папка з PDF файлами
output_folder = 'C:\\Users\\prosi\\Desktop\\json\\Критичне мислення'  # Папка для збереження JSON файлів

# Виконання процесу
process_pdfs_in_folder(input_folder, output_folder)

############################################################################_FORMAt_######################################################################

INPUT_FOLDER = "C:\Users\prosi\Desktop\Нова папка\\Нова папка"  # Вхідна папка з JSON файлами
OUTPUT_FOLDER = "C:\\Users\\prosi\\Desktop\\Нова папка\\Нова папка (2)"  # Папка для відформатованих файлів

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

import os
import json

# Налаштування
INPUT_FOLDER = "C:\\Users\\prosi\\Desktop\\Json_format"  # Вхідна папка з підпапками
OUTPUT_FILE = "C:\\Users\\prosi\\Desktop\\All_in.json"  # Фінальний вихідний файл

all_texts = []  # Список для всього тексту

# Проходження по всіх папках та файлах
for root, _, files in os.walk(INPUT_FOLDER):
    for filename in files:
        if filename.endswith(".json"):
            file_path = os.path.join(root, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    all_texts.extend(entry["text"] for entry in data if "text" in entry)
                except json.JSONDecodeError:
                    print(f"Помилка читання JSON: {file_path}")

# Запис у великий об'єднаний JSON-файл
merged_data = [{"text": text} for text in all_texts]

with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

print(f"✅ Успішно об'єднано {len(all_texts)} записів у {OUTPUT_FILE}")        


import json
from deep_translator import GoogleTranslator

# Функція для перекладу тексту
def translate_text(text, source_lang="uk", target_lang="en"):
    return GoogleTranslator(source=source_lang, target=target_lang).translate(text)

# Функція для перекладу JSON-файлу
def translate_json(input_json_path, output_json_path):
    with open(input_json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Завантаження JSON

    translated_data = []
    
    for item in data:
        if "text" in item:
            translated_text = translate_text(item["text"])
            translated_data.append({"text": translated_text})  # Додаємо перекладений текст
    
    # Записуємо перекладений JSON
    with open(output_json_path, 'w', encoding='utf-8') as file:
        json.dump(translated_data, file, ensure_ascii=False, indent=4)

    print(f"✅ Переклад завершено. Результат у {output_json_path}")

# Вказати шляхи до файлів
input_json_path = "C:\\Users\\prosi\\Desktop\\Json_format\\All_in.json"
output_json_path = "C:\\Users\\prosi\\Desktop\\Json_format\\All_in_eng.json"

# Виконати переклад
translate_json(input_json_path, output_json_path)