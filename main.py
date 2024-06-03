import tkinter as tk
from tkinter import ttk
import pandas as pd

def cyclic_shift_left(value, shift):
    # Выполняем циклический сдвиг влево
    shift %= 8  # Защита от сдвига на большее количество битов, чем в байте
    return ((value << shift) | (value >> (8 - shift))) & 0xFF

def process_text(input_text, shift):
    data = []
    for char in input_text:
        original_code = ord(char)
        shifted_code = cyclic_shift_left(original_code, shift)
        data.append({
            "Символ": char,
            "Код (десятичное)": original_code,
            "Побитовое представление": f"{original_code:08b}",
            "Сдвиг на {shift} бит": f"{shifted_code:08b}",
            "Преобразованный символ": chr(shifted_code),
            "Код преобразованного символа": shifted_code
        })
    return data

def update_table():
    input_text = input_text_var.get()
    shift = int(shift_var.get())
    data = process_text(input_text, shift)
    df = pd.DataFrame(data)
    for row in tree.get_children():
        tree.delete(row)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# Создаем основное окно
root = tk.Tk()
root.title("Побитовые операции")

# Ввод исходного текста
tk.Label(root, text="Исходная строка:").grid(row=0, column=0)
input_text_var = tk.StringVar()
input_text_entry = tk.Entry(root, textvariable=input_text_var)
input_text_entry.grid(row=0, column=1)

# Ввод количества битов для сдвига
tk.Label(root, text="Количество битов для сдвига:").grid(row=1, column=0)
shift_var = tk.StringVar()
shift_entry = tk.Entry(root, textvariable=shift_var)
shift_entry.grid(row=1, column=1)

# Кнопка для обновления таблицы
update_button = tk.Button(root, text="Обновить", command=update_table)
update_button.grid(row=2, column=0, columnspan=2)

# Таблица для отображения результатов
columns = ["Символ", "Код", "Побитовое представление", "Сдвиг", "Преобр. символ", "Код преобр. символа"]
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.grid(row=3, column=0, columnspan=2)

root.mainloop()
