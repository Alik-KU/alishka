import tkinter as tk
from tkinter import filedialog, font, colorchooser, messagebox
from tkinter.scrolledtext import ScrolledText
import os

class DocumentFormatterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Форматирование документов")
        self.root.geometry("900x700")
        self.root.configure(bg="#f8f8f8")

        # Текущий файл
        self.current_file = None

        # Заголовок
        title = tk.Label(root, text="Программа форматирования документов", font=("Arial", 18, "bold"), bg="#f8f8f8")
        title.pack(pady=10)

        # Меню
        self.create_menu()

        # Панель инструментов
        self.create_toolbar()

        # Текстовый редактор
        self.text_area = ScrolledText(root, wrap=tk.WORD, undo=True, font=("Arial", 12), bg="#ffffff")
        self.text_area.pack(expand=1, fill=tk.BOTH, padx=10, pady=10)

        # Нижняя панель
        self.create_footer()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=self.new_file)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Сохранить как", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        tools_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Инструменты", menu=tools_menu)
        tools_menu.add_command(label="Форматировать папку", command=self.format_folder)

        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED, bg="#e0e0e0")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Шрифт
        self.font_var = tk.StringVar(value="Arial")
        font_dropdown = tk.OptionMenu(toolbar, self.font_var, *font.families(), command=self.change_font)
        font_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        # Размер шрифта
        self.size_var = tk.StringVar(value="12")
        size_spinbox = tk.Spinbox(toolbar, from_=8, to=72, textvariable=self.size_var, width=5, command=self.change_font_size)
        size_spinbox.pack(side=tk.LEFT, padx=5, pady=5)

        # Жирный текст
        bold_button = tk.Button(toolbar, text="Ж", command=self.toggle_bold, font=("Arial", 10, "bold"), bg="#d1d1d1")
        bold_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Цвет текста
        color_button = tk.Button(toolbar, text="Цвет текста", command=self.choose_text_color, bg="#d1d1d1")
        color_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Цвет фона
        bg_color_button = tk.Button(toolbar, text="Цвет фона", command=self.choose_bg_color, bg="#d1d1d1")
        bg_color_button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_footer(self):
        footer = tk.Frame(self.root, bg="#e0e0e0", height=30)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        label = tk.Label(footer, text="© 2024. Программа форматирования документов.", bg="#e0e0e0")
        label.pack()

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)
            self.current_file = file_path

    def save_file(self):
        if self.current_file:
            content = self.text_area.get(1.0, tk.END)
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(content.strip())
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Текстовые файлы", "*.txt")])
        if file_path:
            content = self.text_area.get(1.0, tk.END)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content.strip())
            self.current_file = file_path

    def change_font(self, *args):
        new_font = self.font_var.get()
        current_size = int(self.size_var.get())
        self.text_area.configure(font=(new_font, current_size))

    def change_font_size(self, *args):
        current_font = self.font_var.get()
        new_size = int(self.size_var.get())
        self.text_area.configure(font=(current_font, new_size))

    def toggle_bold(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            bold_font = font.Font(self.text_area, self.text_area.cget("font"))
            bold_font.configure(weight="bold")
            self.text_area.tag_configure("bold", font=bold_font)
            self.text_area.tag_add("bold", "sel.first", "sel.last")

    def choose_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.tag_configure("color", foreground=color)
            self.text_area.tag_add("color", "sel.first", "sel.last")

    def choose_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.configure(bg=color)

    def format_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            try:
                for file_name in os.listdir(folder_path):
                    old_path = os.path.join(folder_path, file_name)
                    if os.path.isfile(old_path):
                        new_name = file_name.replace(" ", "_").lower()  # Пример: убрать пробелы, перевести в нижний регистр
                        new_path = os.path.join(folder_path, new_name)
                        os.rename(old_path, new_path)
                messagebox.showinfo("Успех", f"Папка '{folder_path}' успешно отформатирована.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось форматировать папку: {e}")

    def show_about(self):
        messagebox.showinfo("О программе", "Программа для форматирования документов\nСоздано с помощью Python и Tkinter.")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentFormatterApp(root)
    root.mainloop()
