# # import nltk
# # from nltk.corpus import wordnet
# # import pandas as pd
# # import random
# # from sentence_transformers import SentenceTransformer
# # from sklearn.metrics.pairwise import cosine_similarity

# # # Завантажуємо ресурс wordnet
# # nltk.download("wordnet")

# # # Завантажуємо модель SentenceTransformer
# # model = SentenceTransformer("all-MiniLM-L6-v2")

# # # Функція для зміни тексту
# # def modify_text(text):
# #     words = text.split()
# #     for i in range(len(words)):
# #         synonyms = wordnet.synsets(words[i])
# #         if synonyms:
# #             synonyms_list = [lemma.name().replace("_", " ") for syn in synonyms for lemma in syn.lemmas()]
# #             if synonyms_list:
# #                 words[i] = random.choice(synonyms_list)  # Випадкова заміна слова
# #     return " ".join(words)

# # # Завантажуємо дані
# # file_path = "./data_folder/test_t.tsv"  # Вкажи правильний шлях
# # df = pd.read_csv(file_path, sep="\t")

# # # Обробляємо колонку user_answer
# # df["user_answer"] = df["user_answer"].apply(modify_text)

# # # Перевірка similarity
# # sentence1_embeddings = model.encode(df["user_answer"].tolist(), convert_to_tensor=True)
# # sentence2_embeddings = model.encode(df["right_answer"].tolist(), convert_to_tensor=True)
# # similarity_scores = cosine_similarity(sentence1_embeddings.cpu(), sentence2_embeddings.cpu())

# # # Додаємо подібність у відсотках
# # df["Similarly"] = similarity_scores.diagonal() * 100

# # # Перезаписуємо файл
# # df.to_csv(file_path, sep="\t", index=False)

# # print("Файл оновлено успішно!")
# import nltk
# from nltk.corpus import wordnet
# import pandas as pd
# import random
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# # Завантажуємо ресурс wordnet
# nltk.download("wordnet")
# nltk.download("omw-1.4")

# # Завантажуємо модель SentenceTransformer
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Функція для зміни тексту зі збереженням контексту
# def modify_text(text):
#     words = text.split()
#     modified_words = []
    
#     for word in words:
#         synonyms = wordnet.synsets(word)
#         valid_synonyms = [
#             lemma.name().replace("_", " ") 
#             for syn in synonyms 
#             for lemma in syn.lemmas() 
#             if lemma.name().lower() != word.lower()  # Виключаємо саме слово
#         ]
        
#         if valid_synonyms:
#             modified_words.append(random.choice(valid_synonyms))
#         else:
#             modified_words.append(word)
    
#     return " ".join(modified_words)

# # Завантажуємо дані
# file_path = "./data_folder/test_t.tsv"  # Вкажи правильний шлях
# df = pd.read_csv(file_path, sep="\t")

# # Обробляємо колонку user_answer
# df["user_answer"] = df["user_answer"].apply(modify_text)

# # Перевірка similarity
# sentence1_embeddings = model.encode(df["user_answer"].tolist(), convert_to_tensor=True)
# sentence2_embeddings = model.encode(df["right_answer"].tolist(), convert_to_tensor=True)

# similarity_scores = cosine_similarity(sentence1_embeddings.cpu(), sentence2_embeddings.cpu())

# # Додаємо подібність у відсотках
# df["Similarly"] = similarity_scores.diagonal() * 100

# # Перезаписуємо файл
# df.to_csv(file_path, sep="\t", index=False)

# print("Файл оновлено успішно!")



from datasets import load_dataset

# Завантаження датасету
ds = load_dataset("sentence-transformers/stsb")

# Збереження кожної частини датасету в окремий CSV файл (train, validation, test)
ds['train'].to_csv('train_dataset.csv', index=False)
ds['validation'].to_csv('validation_dataset.csv', index=False)
ds['test'].to_csv('test_dataset.csv', index=False)

print("Датасет збережено у форматі CSV.")
