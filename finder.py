from tkinter import *
from tkinter import messagebox as mb
from tkinter import scrolledtext
from tkinter import filedialog
import os, glob


root = Tk()
root.title("Поисковик файлов и директорий")

# Window size
width = 600
height = 350
w = (root.winfo_screenwidth()//2)
h = (root.winfo_screenheight()//2)
root.geometry(str(width) + 'x' + str(height) + '+{}+{}'.format(w - int(width/2), h - int(height/2)))

# Disable resizable
root.resizable(False, False)

def setDirectory(dir):
    entry_dir.delete(0, "end")
    entry_dir.insert(0, dir.replace('/', '\\'))

def check():
    scroll.configure(state='normal')
    scroll.delete(1.0, END)
    scroll.insert(INSERT, '# Сюда будет выгружен путь искомного файла или каталога\n')
    scroll.configure(state='disabled')
    if (os.path.exists(entry_dir.get()) == False):
        answer=mb.askyesno(
            title="Директория поиска не найдена",
            message="Выполнить поиск по системному диску?\n"
                    "Внимание! Данная операция требует времени.")
        if answer:
            entry_dir.delete(0, END)
            entry_dir.insert(INSERT, os.getenv('systemdrive') + '\\')
        else:
            mb.showerror(
                "Невозможно выполнить поиск",
                "Отсутствует директория поиска")
    if (os.path.exists(entry_dir.get())
            and ((entry_name.get() == "" and entry_format.get() != "")
                 or (entry_name.get() != "" and entry_format.get() == "")
                 or (entry_name.get() != "" and entry_format.get() != ""))):
        if len(entry_name.get()) > 0:
            name = entry_name.get()
        else:
            name = '*'
        if len(entry_format.get()) > 0:
            format = '.*' + entry_format.get().replace('.', '')
        else:
            format = '*'
        if (entry_dir.get()[-1] == "\\"):
            recursive = '**\\*'
        else:
            recursive = '\\**\\*'
        iterable = glob.glob(entry_dir.get()+ recursive + name + '*' + format + '*', recursive=True)
        for x in iterable:
            scroll.configure(state='normal')
            scroll.insert   (INSERT, "\n> " + str(x).replace('/', '\\'))
            scroll.configure(state='disabled')
        if (iterable == []):
            mb.showwarning(
                "Поиск окончен",
                "Ничего не найдено.")
        else:
            mb.showinfo(
                "Поиск окончен",
                "Операция выполнена успешно!")
    elif (os.path.exists(entry_dir.get()) == True):
        mb.showerror(
            "Невозможно выполнить поиск",
            "Отсутствуют параметры поиска")

#main
main        = Label (root)
main.pack           (expand=1)

# directory
directory   = Label     (main)
info        = Label     (directory, text='Укажите каталог в котором будет произведен поиск', font=("", 9, "normal"))
entry_dir   = Entry     (directory, width=64)
button_view = Button    (directory, text="Обзор", width=9, font=("", 9, "normal"),
                         bg="#0067C0", activebackground="#3183CA",
                         fg="#ffffff", activeforeground="#ffffff",
                         command=lambda:setDirectory(filedialog.askdirectory()))
entry_dir.insert        (INSERT, os.getcwd().replace('/', '\\'))
directory.pack          (expand=1)
info.pack               (expand=1, anchor=NW, pady=(10, 0))
entry_dir.pack          (expand=1, side=LEFT)
button_view.pack        (expand=1, side=RIGHT, padx=(10, 0))

# search
search              = Label     (main)
search_name         = Label     (search)
file_or_dir_name    = Label     (search_name)
file_format         = Label     (search_name)
label_name          = Label     (file_or_dir_name, text="Название", font=("", 9, "normal"))
entry_name          = Entry     (file_or_dir_name, width=32)
label_format        = Label     (file_format, text="Формат", font=("", 9, "normal"))
entry_format        = Entry     (file_format, width=12)
button_search       = Button    (search, text="Поиск", width=9, font=("", 9, "normal"), command=check,
                                 bg="#FBFBFB", activebackground="#F6F6F6", fg="#000000", activeforeground="#000000")
search.pack                     (expand=1, padx=(0, 4), pady=(5, 5))
search_name.pack                (expand=1, side=LEFT)
label_name.pack                 (expand=1, side=LEFT)
file_or_dir_name.pack           (expand=1, side=LEFT)
entry_name.pack                 (expand=1, side=RIGHT)
file_format.pack                (expand=1, side=RIGHT)
label_format.pack               (expand=1, side=LEFT)
entry_format.pack               (expand=1, side=RIGHT)
button_search.pack              (expand=1, side=RIGHT, padx=(6, 0))

# scrolledtext
label_scroll        = Label                     (main)
scroll              = scrolledtext.ScrolledText (label_scroll, width=60, height=12)
scroll.insert                                   (INSERT, '# Сюда будет выгружен путь искомного файла или каталога\n')
scroll.configure                                (state='disabled')
label_scroll.pack                               (expand=1, padx=(2, 0))
scroll.pack                                     (expand=1)

# credits
author              = Label (root, text='Булат Шигабутдинов', font=("", 9, "normal"))
date                = Label (root, text='Декабрь 2022', font=("", 9, "normal"))
author.pack                 (expand=1, anchor=SW, side=LEFT, pady=(0, 5), padx=(5, 0))
date.pack                   (expand=1, anchor=SE, side=RIGHT, pady=(0, 5), padx=(0, 5))

root.mainloop()