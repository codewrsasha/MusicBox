from tkinter import *
import pygame
from tkinter import filedialog
import os
import random

root = Tk()
root.title("MusicBox")
root.geometry("800x600")
root.configure(bg='#d3c8b2')
root.resizable(False, False)

# Инициализация Pygame Mixer
pygame.mixer.init()

# Темы проекта
themes = {
    "default": {
        "bg": "#d3c8b2",
        "fg": "#d56945",
        "font": ('8bit Wonder', 24),
        "box_frame_bg": "#d56945",
        "song_box_bg": '#484745',
        "select_bg": '#d56945',
        "select_fg": '#484745',
        "song_box_font": ('8bit Wonder', 12),
        "scale_bg": '#d56945',
        "active_bg": '#dc6648',
        "troughcolor": '#4d4747',
        "folder_img": "img\\folder.png",
        "back_img": "img\\back.png",
        "play_img": "img\\play.png",
        "pause_img": "img\\pause.png",
        "forward_img": "img\\forward.png",
        "shuffle_img": "img\\shuffle.png",
        "settings_img": "img\\settings.png",
        "album_img": "img\\album.png",
    },
    "blue":{
        "bg": "#3282F6",
        "fg": "#ffffff",
        "font": ('Monocraft', 24),
        "box_frame_bg": "#ffffff",
        "song_box_bg": '#000c7b',
        "select_bg": '#ffffff',
        "select_fg": '#000c7b',
        "song_box_font": ('Monocraft', 12),
        "scale_bg": '#ffffff',
        "active_bg": '#3282F6',
        "troughcolor": '#000c7b',
        "folder_img": "img\\folder2.png",
        "back_img": "img\\back2.png",
        "play_img": "img\\play2.png",
        "pause_img": "img\\pause2.png",
        "forward_img": "img\\forward2.png",
        "shuffle_img": "img\\shuffle2.png",
        "settings_img": "img\\settings2.png",
        "album_img": "img\\album2.png",
    },
    "pink":{
        "bg": "#efb6e9",
        "fg": "#ea3680",
        "font": ('Keleti', 24),
        "box_frame_bg": "#ea3680",
        "song_box_bg": '#3a073f',
        "select_bg": '#ea3680',
        "select_fg": '#3a073f',
        "song_box_font": ('Keleti', 12),
        "scale_bg": '#ea3680',
        "active_bg": '#efb6e9',
        "troughcolor": '#3a073f',
        "folder_img": "img\\folder3.png",
        "back_img": "img\\back3.png",
        "play_img": "img\\play3.png",
        "pause_img": "img\\pause3.png",
        "forward_img": "img\\forward3.png",
        "shuffle_img": "img\\shuffle3.png",
        "settings_img": "img\\settings3.png",
        "album_img": "img\\album3.png",
    },
    "green":{
        "bg": "#7bfaba",
        "fg": "#09735c",
        "font": ('Oxygene 1 [RUS by KanycTa]', 24),
        "box_frame_bg": "#09735c",
        "song_box_bg": '#173e61',
        "select_bg": '#09735c',
        "select_fg": '#173e61',
        "song_box_font": ('Oxygene 1 [RUS by KanycTa]', 12),
        "scale_bg": '#09735c',
        "active_bg": '#7bfaba',
        "troughcolor": '#173e61',
        "folder_img": "img\\folder4.png",
        "back_img": "img\\back4.png",
        "play_img": "img\\play4.png",
        "pause_img": "img\\pause4.png",
        "forward_img": "img\\forward4.png",
        "shuffle_img": "img\\shuffle4.png",
        "settings_img": "img\\settings4.png",
        "album_img": "img\\album4.png",
    }
}

# Переменная для хранения текущей темы
current_theme = "default"
theme = themes[current_theme]

# Функция для смены темы
def change_theme():
    pass
    global current_theme
    # Переключение темы
    if current_theme == "default":
        current_theme = "blue"
    elif current_theme == "blue":
        current_theme = "pink"
    elif current_theme == "pink":
        current_theme = "green"
    else:
        current_theme = "default"
    
    # Применение новой темы
    theme = themes[current_theme]
    
    root.configure(bg=theme["bg"])
    playingTitle.configure(bg=theme["bg"], fg=theme["fg"], font=theme["font"])
    box_frame.configure(bg=theme["box_frame_bg"])
    song_box.configure(bg=theme["song_box_bg"], fg=theme["fg"], selectbackground=theme["select_bg"], selectforeground=theme["select_fg"], font=theme["song_box_font"])
    controls_frame.configure(bg=theme["bg"])
    folder_img.configure(file=theme["folder_img"])
    back_img.configure(file=theme["back_img"])
    play_img.configure(file=theme["play_img"])
    pause_img.configure(file=theme["pause_img"])
    forward_img.configure(file=theme["forward_img"])
    shuffle_img.configure(file=theme["shuffle_img"])
    settings_img.configure(file=theme["settings_img"])
    album_img.configure(file=theme["album_img"])
    for button in [folder_btn, back_btn, play_btn, pause_btn, forward_btn, shuffle_btn, settings_btn]:
        button.configure(bg=theme["bg"])
    album_show.configure(bg=theme["bg"])
    volume_scale.configure(bg=theme["scale_bg"], activebackground=theme["active_bg"], troughcolor=theme["troughcolor"], font=theme["song_box_font"])


# Создание поля названия проигроваимого трека
playingTitle = Label(bg="#d3c8b2", fg="#d56945", font=('8bit Wonder', 24), text="Song name")
playingTitle.place(x=270, y=30, width=460, height=50)

# Функция - Добавить песню
def add_songs():
    global folder_selected
    folder_selected = filedialog.askdirectory()  # Открывает диалог для выбора папки
    if folder_selected:  # Если папка выбрана
        song_box.delete(0, END)  # Очищаем список перед загрузкой новых песен
        songs = [f for f in os.listdir(folder_selected) if f.endswith(('.mp3', '.wav'))]  # Фильтруем по типу файлов
        for song in songs:
            song_box.insert(END, song)  # Добавляем песни в Listbox

# Функция - Воспроизведение трека
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

# Функция - Предидущая песня
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

# Функция - Следующая песня
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

# Функция - Пауза
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

# Функция - Рандомный трек
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

# Функция - Изменение громкости
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
settings_img = PhotoImage(file='img\\settings.png')


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
settings_btn = Button(image=settings_img, borderwidth=0, bg='#d3c8b2', command=change_theme)
settings_btn.place(x=700, y=30)

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