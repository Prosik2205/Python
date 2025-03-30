from fastapi import FastAPI, File, UploadFile, HTTPException
import fitz  # PyMuPDF
import json
import os
import shutil
import zipfile
from deep_translator import GoogleTranslator
from uuid import uuid4

app = FastAPI()

# Директорія для збереження JSON-файлів
STORAGE_FOLDER = "./storage"
os.makedirs(STORAGE_FOLDER, exist_ok=True)

# === Функція витягнення тексту з PDF ===
def extract_text_from_pdf(pdf_bytes):
    text = ""
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in pdf_document:
        text += page.get_text("text")
    return text

# === Функція очищення тексту ===
def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip() and len(line.split()) > 1]
    return "\n".join(cleaned_lines)

# === Функція конвертації тексту в JSON ===
def convert_text_to_json(text):
    sentences = text.split('. ')
    return [{"text": sentence.strip()} for sentence in sentences if sentence]

# === Функція перекладу JSON ===
def translate_json(data):
    return [{"text": GoogleTranslator(source="uk", target="en").translate(item["text"])} for item in data]

# === Функція обробки PDF-файлу ===
def process_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_bytes = file.read()
    text = extract_text_from_pdf(pdf_bytes)
    cleaned_text = clean_text(text)
    json_data = convert_text_to_json(cleaned_text)
    translated_data = translate_json(json_data)
    return translated_data

# === API для завантаження ZIP з папкою PDF-файлів ===
@app.post("/upload")
async def upload_zip(file: UploadFile = File(alias="Json_format")):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Тільки ZIP-файли підтримуються")
    
    zip_id = str(uuid4())
    zip_path = os.path.join(STORAGE_FOLDER, f"{zip_id}.zip")
    extract_folder = os.path.join(STORAGE_FOLDER, zip_id)
    os.makedirs(extract_folder, exist_ok=True)
    
    with open(zip_path, "wb") as buffer:
        buffer.write(await file.read())
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    
    results = {}
    for root, _, files in os.walk(extract_folder):
        for filename in files:
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(root, filename)
                processed_data = process_pdf(pdf_path)
                results[filename] = processed_data
    
    json_path = os.path.join(STORAGE_FOLDER, f"{zip_id}.json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)
    
    shutil.rmtree(extract_folder)  # Видаляємо тимчасову папку
    os.remove(zip_path)  # Видаляємо ZIP-файл
    
    return {"zip_id": zip_id, "message": "Файли успішно оброблені та збережені"}

# === API для отримання оброблених JSON-файлів ===
@app.get("/data/{zip_id}")
async def get_processed_data(zip_id: str):
    json_path = os.path.join(STORAGE_FOLDER, f"{zip_id}.json")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="Файл не знайдено")
    
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    
    return {"zip_id": zip_id, "data": data}