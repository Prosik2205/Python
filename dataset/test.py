import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Завантажуємо .tsv файл
file_path = './data_folder/test.tsv'  # вказуєте шлях до вашого файлу
df = pd.read_csv(file_path, sep='\t')

# Перевіряємо, як виглядають перші рядки
print(df.head())

# 1. Завантаження моделі Sentence-BERT
model = SentenceTransformer('all-MiniLM-L6-v2')  # Модель, яка добре підходить для задач подібності

# 2. Перетворення текстів в вектори за допомогою моделі Sentence-BERT
sentence1_embeddings = model.encode(df['sentence1'].tolist())
sentence2_embeddings = model.encode(df['sentence2'].tolist())

# 3. Обчислення косинусної подібності між кожною парою рядків
similarity_scores = cosine_similarity(sentence1_embeddings, sentence2_embeddings)

# 4. Додавання нового стовпця "Similarly" зі значеннями відсотків
df['Similarly'] = similarity_scores.diagonal() * 100  # Перетворюємо значення на відсотки

# 5. Збереження результату назад в файл
df.to_csv(file_path, sep='\t', index=False)

print("Колонка 'Similarly' успішно додана.")
