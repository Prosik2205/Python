import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Завантажуємо .tsv файл
file_path = './data_folder/2k.csv'  # вказуєте шлях до вашого файлу
df = pd.read_csv(file_path)

# 1. Завантаження моделі Sentence-BERT
model = SentenceTransformer('all-MiniLM-L6-v2')  # Модель, яка добре підходить для задач подібності

# 2. Перетворення текстів в вектори за допомогою моделі Sentence-BERT
sentence1_embeddings = model.encode(df['user_answer'].tolist())
sentence2_embeddings = model.encode(df['right_answer'].tolist())

# 3. Обчислення косинусної подібності між кожною парою рядків
similarity_scores = cosine_similarity(sentence1_embeddings, sentence2_embeddings)

# 4. Додавання нового стовпця "Similarly" зі значеннями відсотків
df['Similarly'] = similarity_scores.diagonal() * 100  # Перетворюємо значення на відсотки

# 5. Збереження результату назад в файл
df.to_csv(file_path, index=False)

print("Колонка 'Similarly' успішно додана.")



# import pandas as pd

# # Зчитуємо .tsv файл у DataFrame
# file_path = './data_folder/Text_Similarity_Dataset.csv'  # вказуєте шлях до вашого файлу
# df = pd.read_csv(file_path)

# # Перевіряємо перші кілька рядків, щоб побачити наявні колонки
# print(df.head())

# # Видаляємо колонку (наприклад, "column_to_remove")
# df = df.drop(columns=['Unique_ID'])

# # Записуємо DataFrame назад в .tsv файл, без вказаної колонки
# df.to_csv(file_path, index=False)

# print("Колонка успішно видалена.")






























# import pandas as pd
# from datasets import Dataset

# # Завантажуємо ваш .tsv файл
# file_path = './data_folder/test_2k.tsv'  # вказуєте шлях до вашого файлу
# df = pd.read_csv(file_path, sep='\t')

# # Перевірка даних
# print(df.head())

# # Перетворення DataFrame у формат Hugging Face Dataset
# dataset = Dataset.from_pandas(df)

# # Перевіряємо, як виглядає перший запис
# print(dataset[0])

# # Тепер 'dataset' містить ваші дані у форматі Hugging Face








