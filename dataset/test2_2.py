pdf_path = 'output/ДМКТ  лекція 1 презентація 2024 ч  1 .pdf'
json_path = 'data_folder/ле1кція.json'



import fitz  # PyMuPDF
import json

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
    lines = text.split('\n')
    cleaned_lines = []
    
    # Проходимо кожен рядок і фільтруємо порожні та непотрібні рядки
    for line in lines:
        cleaned_line = line.strip()  # Видалити зайві пробіли з початку і кінця рядка
        if cleaned_line and len(cleaned_line.split()) > 1:  # Якщо рядок не порожній і має більше одного слова
            cleaned_lines.append(cleaned_line)
    
    # Об'єднуємо очищені рядки назад в один текст, кожен рядок знову розділений \n
    return "\n".join(cleaned_lines)

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

# Шляхи до файлів

# Виконання процесу
text = extract_text_from_pdf(pdf_path)
cleaned_text = clean_text(text)  # Очищаємо текст
convert_text_to_json(cleaned_text, json_path)  # Конвертуємо в JSON



