import tkinter as tk
from tkinter import messagebox
import math


# Функция для поиска индекса вершины с минимальным весом, которая еще не была просмотрена
def arg_min(T, S):
    amin = -1
    m = math.inf  # Максимальное значение для начальной инициализации
    for i, t in enumerate(T):
        if t < m and i not in S:
            m = t
            amin = i
    return amin


# Функция для реализации алгоритма Дейкстры
def dijkstra(D, start, end):
    N = len(D)
    T = [math.inf] * N  # Последняя строка таблицы весов
    v = start  # Стартовая вершина
    S = {v}  # Множество просмотренных вершин
    T[v] = 0  # Вес стартовой вершины равен нулю
    M = [0] * N  # Оптимальные связи между вершинами

    # Основной цикл алгоритма Дейкстры
    while v != -1:
        for j, dw in enumerate(D[v]):  # Перебор всех связанных вершин с вершиной v
            if j not in S:  # Если вершина еще не просмотрена
                w = T[v] + dw
                if w < T[j]:
                    T[j] = w
                    M[j] = v  # Связываем вершину j с вершиной v

        v = arg_min(T, S)  # Выбираем следующий узел с наименьшим весом
        if v >= 0:
            S.add(v)  # Добавляем новую вершину в множество просмотренных

    # Формирование кратчайшего пути
    P = [end]
    while end != start:
        end = M[P[-1]]
        P.append(end)

    P.reverse()  # Путь был построен в обратном порядке, поэтому его нужно перевернуть
    return T, M, P


# Функция для запуска алгоритма Дейкстры
def run_dijkstra():
    try:
        start = int(start_entry.get())  # Получение стартовой вершины
        end = int(end_entry.get())  # Получение конечной вершины

        # Обновление значений матрицы смежности из введенных данных
        for i in range(N):
            for j in range(N):
                val = entries[i][j].get()
                D[i][j] = math.inf if val == '∞' else int(val)

        # Запуск алгоритма Дейкстры
        _, _, P = dijkstra(D, start, end)
        result_label.config(text=f"Shortest Path: {' -> '.join(map(str, P))}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Функция для обновления матрицы смежности при изменении количества вершин
def update_matrix():
    global N, D, entries
    try:
        N = int(vertex_entry.get())  # Получение нового количества вершин
        D = [[math.inf] * N for _ in range(N)]
        for i in range(N):
            D[i][i] = 0  # Установка нулевого веса для диагональных элементов

        # Удаление старых виджетов матрицы
        for widget in matrix_frame.winfo_children():
            widget.destroy()

        entries = []
        # Создание новых виджетов для ввода значений матрицы
        for i in range(N):
            row = []
            for j in range(N):
                entry = tk.Entry(matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(tk.END, '∞' if D[i][j] == math.inf else str(D[i][j]))
                row.append(entry)
            entries.append(row)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of vertices.")


# Настройка основного окна приложения
root = tk.Tk()
root.title("Dijkstra Algorithm")
root.geometry("800x600")

N = 0  # Начальное количество вершин
D = [[math.inf] * N for _ in range(N)]
for i in range(N):
    D[i][i] = 0  # Установка нулевого веса для диагональных элементов

# Создание фрейма для управления
controls_frame = tk.Frame(root)
controls_frame.pack()

# Виджеты для ввода количества вершин
vertex_label = tk.Label(controls_frame, text="Number of vertices:")
vertex_label.grid(row=0, column=0, padx=5, pady=5)
vertex_entry = tk.Entry(controls_frame, width=5)
vertex_entry.grid(row=0, column=1, padx=5, pady=5)
vertex_entry.insert(tk.END, '6')

# Кнопка для обновления матрицы смежности
update_button = tk.Button(controls_frame, text="Update Matrix", command=update_matrix)
update_button.grid(row=0, column=2, padx=5, pady=5)

# Виджеты для ввода стартовой и конечной вершин
start_label = tk.Label(controls_frame, text="Start:")
start_label.grid(row=1, column=0, padx=5, pady=5)
start_entry = tk.Entry(controls_frame, width=5)
start_entry.grid(row=1, column=1, padx=5, pady=5)
start_entry.insert(tk.END, '0')

end_label = tk.Label(controls_frame, text="End:")
end_label.grid(row=1, column=2, padx=5, pady=5)
end_entry = tk.Entry(controls_frame, width=5)
end_entry.grid(row=1, column=3, padx=5, pady=5)
end_entry.insert(tk.END, '5')

# Кнопка для запуска алгоритма Дейкстры
run_button = tk.Button(controls_frame, text="Run Dijkstra", command=run_dijkstra)
run_button.grid(row=2, columnspan=4, pady=10)

# Фрейм для ввода значений матрицы смежности
matrix_frame = tk.Frame(root)
matrix_frame.pack()

# Создание виджетов для ввода значений матрицы
entries = []
for i in range(N):
    row = []
    for j in range(N):
        entry = tk.Entry(matrix_frame, width=5)
        entry.grid(row=i, column=j, padx=5, pady=5)
        entry.insert(tk.END, '∞' if D[i][j] == math.inf else str(D[i][j]))
        row.append(entry)
    entries.append(row)

# Метка для отображения результата
result_label = tk.Label(root, text="")
result_label.pack()

# Запуск основного цикла приложения
root.mainloop()
