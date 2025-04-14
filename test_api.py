from fastapi import FastAPI, File, UploadFile, HTTPException
import pymupdf as fitz  # PyMuPDF
import json
import os
import shutil
import zipfile
from deep_translator import GoogleTranslator
from uuid import uuid4
from typing import List

app = FastAPI()

# Директорія для збереження JSON-файлів
STORAGE_FOLDER = "./storage"
os.makedirs(STORAGE_FOLDER, exist_ok=True)

MAX_LENGTH = 1000  # Довжина одного текстового фрагмента

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

# === Функція розбиття тексту на рівні частини ===
def size_row(data, max_length=MAX_LENGTH):
    def split_text_into_chunks(text, max_length):
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

    full_text = " ".join(entry["text"] for entry in data if "text" in entry)
    formatted_chunks = split_text_into_chunks(full_text, max_length)
    return [{"text": chunk} for chunk in formatted_chunks]

# === Функція обробки PDF-файлу ===
def process_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_bytes = file.read()
    text = extract_text_from_pdf(pdf_bytes)
    cleaned_text = clean_text(text)
    json_data = convert_text_to_json(cleaned_text)
    translated_data = translate_json(json_data)
    formatted_data = size_row(translated_data)
    return formatted_data

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(alias="Json_format")):
    all_results = {}

    for file in files:
        file_ext = file.filename.lower().split(".")[-1]

        if file_ext == "zip":
            zip_id = str(uuid4())
            zip_path = os.path.join(STORAGE_FOLDER, f"{zip_id}.zip")
            extract_folder = os.path.join(STORAGE_FOLDER, zip_id)
            os.makedirs(extract_folder, exist_ok=True)

            with open(zip_path, "wb") as buffer:
                buffer.write(await file.read())

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)

            for root, _, inner_files in os.walk(extract_folder):
                for filename in inner_files:
                    if filename.endswith(".pdf"):
                        pdf_path = os.path.join(root, filename)
                        processed_data = process_pdf(pdf_path)
                        all_results[filename] = processed_data

            shutil.rmtree(extract_folder)
            os.remove(zip_path)

        elif file_ext == "pdf":
            file_id = str(uuid4())
            temp_pdf_path = os.path.join(STORAGE_FOLDER, f"{file_id}.pdf")

            with open(temp_pdf_path, "wb") as buffer:
                buffer.write(await file.read())

            processed_data = process_pdf(temp_pdf_path)
            all_results[file.filename] = processed_data

            os.remove(temp_pdf_path)

        else:
            raise HTTPException(status_code=400, detail=f"File {file.filename} has an unsupported format")

    # Генеруємо один JSON для всіх файлів
    final_id = str(uuid4())
    json_path = os.path.join(STORAGE_FOLDER, f"{final_id}.json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(all_results, json_file, ensure_ascii=False, indent=4)

    return {
        "file_id": final_id,
        "message": "Files processed successfully",
        "files_processed": list(all_results.keys())
    }








# === API для отримання оброблених JSON-файлів ===
@app.get("/data/{zip_id}")
async def get_processed_data(zip_id: str):
    json_path = os.path.join(STORAGE_FOLDER, f"{zip_id}.json")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    
    return {"zip_id": zip_id, "data": data}

#uvicorn test_api:app --reload

