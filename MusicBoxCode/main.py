from tkinter import *
import pygame
from tkinter import filedialog
import os
import random

root = Tk()
root.title("MusicBox")
#root.iconbitmap('')
root.geometry("800x600")
root.configure(bg='#d3c8b2')
root.resizable(False, False)

# Необходимые переменные
track_lenght = 180 #длительность трека(в секундах)

# Инициализация Pygame Mixer
pygame.mixer.init()

# Создание поля названия проигроваимого трека
playingTitle = Label(font=('8bit Wonder', 24),text='Song name', bg='#d3c8b2')
playingTitle.place(x=270, y=30, width=460, height=50)

# Функция добавить песню
def add_songs():
    global folder_selected
    folder_selected = filedialog.askdirectory()  # Открывает диалог для выбора папки
    if folder_selected:  # Если папка выбрана
        song_box.delete(0, END)  # Очищаем список перед загрузкой новых песен
        songs = [f for f in os.listdir(folder_selected) if f.endswith(('.mp3', '.wav'))]  # Фильтруем по типу файлов
        for song in songs:
            song_box.insert(END, song)  # Добавляем песни в Listbox

# Воспроизведение трека
def play():
    global paused
    # Получаем выбранный трек из списка
    if song_box.curselection():  # Проверяем, что что-то выбрано
        track = song_box.get(song_box.curselection())  # Получаем имя трека
        playingTitle.config(text=track) # Переименование поля названия трека
        track_path = os.path.join(folder_selected, track)  # Полный путь к треку

        if not paused:  # Если не на паузе
            pygame.mixer.music.load(track_path)  # Загружаем трек
            pygame.mixer.music.play()  # Воспроизводим трек
            paused = False  # Устанавливаем статус воспроизведения
        else:  # Если на паузе
            pygame.mixer.music.unpause()  # Возобновляем воспроизведение
            paused = False  # Устанавливаем статус воспроизведения

def prev_song():
    track = song_box.curselection()
    next_one = track[0]-1
    track = song_box.get(next_one) 
    playingTitle.config(text=track) # Переименование поля названия трека
    track_path = os.path.join(folder_selected, track)
    pygame.mixer.music.load(track_path)  # Загружаем трек
    pygame.mixer.music.play()  # Воспроизводим трек

    # Перемещение полосы выбора по плейлисту
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.select_set(next_one, last=None)

def next_song():
    track = song_box.curselection()
    next_one = track[0]+1
    track = song_box.get(next_one) 
    playingTitle.config(text=track) # Переименование поля названия трека
    track_path = os.path.join(folder_selected, track)
    pygame.mixer.music.load(track_path)  # Загружаем трек
    pygame.mixer.music.play()  # Воспроизводим трек

    # Перемещение полосы выбора по плейлисту
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.select_set(next_one, last=None)

paused = False

def pause(is_paused):
    global  paused
    paused = is_paused

    if paused:
        # продолжить воспроизведение
        pygame.mixer.music.unpause()
        paused = False
    else:
        # пауза
        pygame.mixer.music.pause()
        paused = True

def shuffle():
    # Проверяем, есть ли треки в списке
    if song_box.size() > 0:
        # Получаем случайный индекс
        random_index = random.randint(0, song_box.size() - 1)
        # Получаем трек по случайному индексу
        track = song_box.get(random_index)
        playingTitle.config(text=track)  # Обновляем название текущего трека
        track_path = os.path.join(folder_selected, track)  # Полный путь к треку
        pygame.mixer.music.load(track_path)  # Загружаем трек
        pygame.mixer.music.play()  # Воспроизводим трек
        # Обновляем выбор в плейлисте
        song_box.selection_clear(0, END)
        song_box.activate(random_index)
        song_box.select_set(random_index, last=None)

def change_volume(master):
    pygame.mixer.music.set_volume(volume_scale.get()/100)

# Создание Плэйлиста
box_frame = Frame(root, bg='#d56945', bd=5)
box_frame.pack(padx=100, pady=100)
box_frame.place(x=5, y=5, relwidth=0.25, relheight=0.98)
song_box = Listbox(box_frame, bg='#484745', fg='#d56945', selectbackground='#d56945', selectforeground='#484745', font=('8bit Wonder', 12))
song_box.pack(pady=0)
song_box.place(x=0, y=0, relheight=1, relwidth=0.999)

# Создание кнопок управления плеером
folder_img = PhotoImage(file='img\\folder.png')
back_img = PhotoImage(file='img\\back.png')
play_img = PhotoImage(file='img\\play.png')
pause_img = PhotoImage(file='img\\pause.png')
forward_img = PhotoImage(file='img\\forward.png')
shuffle_img = PhotoImage(file='img\\shuffle.png')

# Создание рамки 
controls_frame = Frame(root, bg='#d3c8b2')
controls_frame.pack()
controls_frame.place(x=270,y=500)

# Расположение кнопок на странице
folder_btn = Button(controls_frame, image=folder_img, borderwidth=0, bg='#d3c8b2', command=add_songs)
back_btn = Button(controls_frame, image=back_img, borderwidth=0, bg='#d3c8b2', command=prev_song)
play_btn = Button(controls_frame, image=play_img, borderwidth=0, bg='#d3c8b2', command=play)
pause_btn = Button(controls_frame, image=pause_img, borderwidth=0, bg='#d3c8b2', command=lambda: pause(paused))
forward_btn = Button(controls_frame, image=forward_img, borderwidth=0, bg='#d3c8b2', command=next_song)
shuffle_btn = Button(controls_frame, image=shuffle_img, borderwidth=0, bg='#d3c8b2', command=shuffle)

# Создание и расположение картинки альбома
album_img = PhotoImage(file='img\\album.png')
album_show = Label(image=album_img, bg='#d3c8b2')
album_show.place(x=340, y=120)

# Создание слайдера громкости
volume_scale = Scale(orient=VERTICAL, from_=100.0, to=0.0, bg='#d56945', activebackground='#dc6648', troughcolor='#4d4747', font=('8bit Wonder', 12), command=change_volume)
volume_scale.set(50)
volume_scale.place(x=700, y=200, height=200)

# row-ряды, column-колонки
folder_btn.grid(row=1, column=0, padx=10)
back_btn.grid(row=1, column=1, padx=10)
play_btn.grid(row=1, column=2, padx=10)
pause_btn.grid(row=1, column=3, padx=10)
forward_btn.grid(row=1, column=4, padx=10)
shuffle_btn.grid(row=1, column=5, padx=10)

my_menu = Menu(root)
root.config(menu=my_menu)

root.mainloop()