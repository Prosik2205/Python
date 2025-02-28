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
input_json_path = "C:\\Users\\prosi\\Desktop\\json\\Нова папка\\укр\\Лекція 1. Числові множини. Комплексні числа та дії над ними..json"
output_json_path = "C:\\Users\\prosi\\Desktop\\json\\Нова папка\\інгліш\\Лекція 1. Числові множини. Комплексні числа та дії над ними..json"

# Виконати переклад
translate_json(input_json_path, output_json_path)
