import pandas as pd

# Завантажуємо дані з файлу
file_path = "Варіант10.txt"  # Замініть на свій шлях
df = pd.read_csv(file_path, sep="\\s+")

# Обчислюємо y1 та y2
df["y1"] = round(2.3 * df["x1"] * df["x2"] - 0.5 * df["x1"]**2 + 1.8 * df["x2"], 2)

df["y2"] = round(df["y1"]**2,2)


# Зберігаємо оновлений файл
output_path = "output_data.txt"
df.to_csv(output_path, sep="\t", index=False)

print(f"Файл збережено як {output_path}")

# import pandas as pd

# file_path = "Варіант10.txt"  # Вкажіть правильний шлях
# df = pd.read_csv(file_path, sep="\\s+")  # Використовуємо регулярний вираз для кількох пробілів

# print(df.head())  # Подивимося, чи правильно зчитані стовпці
# print(df.columns)  # Перевіримо назви стовпців
