import ctypes, sys, os, win32serviceutil, glob
from tkinter import *
from tkinter import messagebox as mb

root = Tk()
root.title("Очиститель очереди печати")

# Window size
width = 400
height = 220
w = (root.winfo_screenwidth()//2)
h = (root.winfo_screenheight()//2)
root.geometry(str(width) + 'x' + str(height) + '+{}+{}'.format(w - int(width/2), h - int(height/2)))

# Disable resizable
root.resizable(False, False)

attention = Label(root, text='Внимание!', font=("", 12, "bold"))
warning = Label(root, text='Нажатие на кнопку "Очистка" приведет к\n'
                        'перезагрузке службы работы принтеров', font=("", 9, "normal"))
frame = Label()
clean = Button(frame, text="Очистка", font=("", 9, "normal"), width=12, height=2, bg="#0067C0", fg='#ffffff')
cancel = Button(frame, text="Выйти", font=("", 9, "normal"), width=12, height=2, bg="#FBFBFB", fg='#000000')
rule = Label(root, text='Не нажимайте "Выйти" и не закрывайте окно\n'
                        'во время выполнения очистки', font=("", 9, "normal"))
author = Label(root, text='Булат Шигабутдинов', font=("", 9, "normal"))
date = Label(root, text='Декабрь 2022', font=("", 9, "normal"))

def remove(files):
    not_removed, removed = 0, 0
    for file in files:
        try:
            os.remove(file)
            removed += 1
        except:
            not_removed += 1
    return removed, not_removed

def count():
    try:
        # Net stop spooler
        win32serviceutil.StopService('spooler')
    except:
        mb.showwarning(
            "Невозможно остановить диспетчер задач",
            "При повторном появлении данной ошибки перезагрузите компьютер или позовите специалиста")

    # Path of files
    shd = glob.glob(os.getenv('systemroot') + '\system32\spool\printers\*.shd')
    spl = glob.glob(os.getenv('systemroot') + '\system32\spool\printers\*.spl')

    # Counting files
    removed_shd, not_removed_shd = remove(shd)
    removed_spl, not_removed_spl = remove(spl)
    removed = removed_shd + removed_spl
    not_removed = not_removed_shd + not_removed_spl

    if removed == 0 and not_removed == 0:
        mb.showwarning(
            "Файлы печати отстутствуют",
            "Дополнительных действий не требуется")

    try:
        win32serviceutil.StartService('spooler')
    except:
        mb.showerror(
            "Невозможно запустить диспетчер задач",
            "Перезапустите программу и заново выполните очистку, "
            "при повторном появлении данной ошибки перезагрузите компьютер или позовите специалиста")

    return not_removed

def btn_clean():
    clean['text'] = "Очистка"
    clean['bg'] = '#0067C0'
    clean['activebackground'] = '#3183CA'
    clean['fg'] = '#ffffff'
    clean['activeforeground'] = '#ffffff'

    if count() > 0:
        mb.showerror(
            "Некоторые файлы печати не были удалены",
            "Завершите все программы или перезагрузитесь")
    else:
        mb.showinfo(
            "Все файлы печати удалены",
            "Операция выполнена успешно!")

def btn_quit():
    cancel['text'] = "Выйти"
    cancel['bg'] = '#FBFBFB'
    cancel['activebackground'] = '#F6F6F6'
    cancel['fg'] = '#000000'
    cancel['activeforeground'] = '#000000'
    root.quit()

clean.config(command=btn_clean)
cancel.config(command=btn_quit)

attention.pack(expand=1, side=TOP)
warning.pack(expand=1, side=TOP)
frame.pack(expand=1, side=TOP)
clean.pack(expand=1, side=LEFT, padx=10)
cancel.pack(expand=1, side=RIGHT, padx=10)
rule.pack(expand=1, side=TOP)
author.pack(expand=1, anchor=SW, side=LEFT)
date.pack(expand=1, anchor=SE, side=RIGHT)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    mb.showerror(
        "Невозможно запустить программу",
        "Требуется запуск от имени администратора")
    sys.exit()

root.mainloop()
