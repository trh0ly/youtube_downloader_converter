# -------------------------------------------
# module import
from moviepy.video.io.VideoFileClip import VideoFileClip
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import cpu_count
from bs4 import BeautifulSoup as bs
from os import getcwd, path, mkdir
from selenium import webdriver
from threading import Thread
from re import findall, sub
from pytube import YouTube
from queue import Queue
from tkinter import ttk
from time import sleep
from tkinter import *
from sys import exit


# -------------------------------------------
# define functions
# -------------------------------
# GUI
# -------------
# dropdown menu - cpu
def set_up_cpu_drop_down_menu():
    cpu_drop_down_value = IntVar()
    cpu_drop_down_value.set(get_core_count_list()[0])
    cpu_drop_down_label = Label(root, text="Anzahl der CPU-Threads:", font=font_normal())
    cpu_drop_down_menu = OptionMenu(root, cpu_drop_down_value, *get_core_count_list())
    cpu_drop_down_menu.config(font=font_normal())
    return cpu_drop_down_menu, cpu_drop_down_label, cpu_drop_down_value


# -------------
# sleep timer input
def set_up_leep_time_input_box():
    sleep_time_label = Label(root, text="Verzögerung beim Download", font=font_normal(()))
    spacer(widget=sleep_time_label, x=0, y=10) 
    sleep_time_deafult_value = IntVar(root, 10)
    sleep_time_input_box = Entry(root, width=5, font=font_normal(), textvariable=sleep_time_deafult_value)
    sleep_time_input_box.bind("<Button-1>", clear_on_click)
    return sleep_time_input_box, sleep_time_label


# -------------
# url input
def set_up_url_input():
    url_input_label = Label(root, text="URL der Playlist/ des Videos:", font=font_bold())
    spacer(widget=url_input_label, x=0, y=20)
    url_input_box_value = StringVar(root, 'URL einfügen')
    url_input_box = Entry(root, width=input_box_width, font=font_normal(), textvariable=url_input_box_value)
    url_input_box.bind("<Button-1>", clear_on_click)
    return url_input_box, url_input_label


# -------------
# download_path
def set_up_download_path_input():
    download_path_label = Label(root, text="Download-Pfad für die Videos:", font=font_bold(()))x
    spacer(widget=download_path_label, x=0, y=10)
    download_input_box_deafult_value = StringVar(root, download_path)
    download_input_box = Entry(root, width=input_box_width, font=font_normal(), textvariable=download_input_box_deafult_value)
    return download_input_box, download_path_label


# -------------
# check box for converting
def set_up_convert_check_box():
    convert_check_box_value = BooleanVar()
    convert_check_box_value.set(True)
    convert_check_box = Checkbutton(root, text="Konvertiere gedownloadete Videos in MP3", variable=convert_check_box_value, font=font_normal())
    return convert_check_box, convert_check_box_value


# -------------
# mp3_path
def set_up_mp3_path_input():
    mp3_label = Label(root, text="Speicherort für die MP3's:", font=font_bold())
    spacer(widget=mp3_label, x=0, y=5)
    mp3_input_box_value = StringVar(root, mp3_path)
    mp3_input_box = Entry(root, width=input_box_width, font=font_normal(), textvariable=mp3_input_box_value)
    return mp3_label, mp3_input_box


# -------------
# save bottom for settings
def set_up_settings_save_buttom():
    settings_save_buttom = Button(root, text="Einstellungen übernehmen", font=font_normal(),  command=save_buttom_on_click)
    return settings_save_buttom


# -------------
# set up start_bottom
def set_up_start_bottom():
    start_bottom = Button(root, text="Prozess starten", font=font_bold(), command=start_main_process_thread)
    return start_bottom


# -------------
# output window
def set_up_scrollbar():
    scrollbar = Scrollbar(root)
    scrollbar_text = Text(root, height=scrollbar_height, width=(input_box_width + 6))
    scrollbar.config(command=scrollbar_text.yview)
    scrollbar.pack(side=RIGHT, fill=Y, anchor='center')
    return scrollbar, scrollbar_text


# ----------------------
# function that determine usable cpu cores for multiprocessing
def get_core_count_list():
    core_count = cpu_count()
    options = [1]
    if core_count <= 3: pass
    else: options += [i for i in range(2, int(core_count - 1))][::2]
    return options


# -------------------------------
# APPEARANCE
# -------------
# functions that sets up font settings
def font_normal(font='Helvetica', size=12):
    return (font, size)


# -------------
# functions that sets up font settings
def font_bold(font='Helvetica', size=12):
    return (font, size, 'bold')


# -------------
# function that makes spaces
def spacer(widget, x=0, y=10):
    widget.pack(padx=x, pady=y)


# -------------
# function that creates a separator
def separator(x=0, y=125, width=1):
    return ttk.Separator(root).place(x=x, y=y, relwidth=width)


# -------------
# ON CLICK / GIU INTERACTIVE
# ------------------------
# function that that starts new thread on start bottom click
def start_main_process_thread():
    main_process_thread = Thread(target=start_buttom_on_click)
    main_process_thread.name = 'main_process'
    main_process_thread.start()


# ------------------------
# function that that clears input box on click
def clear_on_click(event):
    event.widget.delete(0, END)


# -------------
# function that print statements to scrollbar
def update_scrollbar_text(text_update, blank_size=72):
    blank = str('#' + '-' * blank_size + '#\n')
    text_update = str(text_update) + '\n'
    scrollbar_text.config(yscrollcommand=scrollbar.set, state='normal')
    scrollbar_text.insert(END, blank)
    scrollbar_text.insert(END, text_update)
    scrollbar_text.config(yscrollcommand=scrollbar.set, state='disabled')
    scrollbar_text.see("end")


# -------------
# define function that determins actual settings
def get_runtime_settings():
    current_url = str(url_input_box.get())
    current_download_path = str(download_input_box.get())
    current_mp3_path = str(mp3_input_box.get())
    current_sleep_time = int(sleep_time_input_box.get())
    return current_url, current_download_path, current_mp3_path, current_sleep_time


# -------------
# function that starts the process
def start_buttom_on_click():
    current_url, current_download_path, current_mp3_path, current_sleep_time = get_runtime_settings()
    make_dir(current_download_path)
    make_dir(current_mp3_path)
    main_process(sleep_time=current_sleep_time, current_url=current_url, current_download_path=current_download_path, current_mp3_path=current_mp3_path)


# -------------
# function that saves settings to config file
def save_buttom_on_click(file='config.txt'):
    _, new_download_path, new_mp3_path, _ = get_runtime_settings()
    acutal_config_values = read_file(file)
    with open(file, 'w') as f:
        for i, line in enumerate(acutal_config_values, 0):
            if i == 0: f.writelines(str(new_download_path) + '\n')
            elif i == 1: f.writelines(str(new_mp3_path) + '\n')
    update_scrollbar_text(text_update='[ÜBERNEHME] Der Download-Pfad lautet: {}'.format(new_download_path))
    update_scrollbar_text(text_update='[ÜBERNEHME] Der MP3-Pfad lautet: {}'.format(new_mp3_path))


# -------------
# print information about errors
def end_message(failed_downloads, failed_convert):
    if len(failed_downloads) < 1: update_scrollbar_text(text_update='[INFO] Der Prozess wurde ohne Downloadfehler abgeschlossen.')
    else: update_scrollbar_text(text_update='[INFO] Der Prozess wurde mit Downloadfehler(n) abgeschlossen.\nFolgende Titel konnten nicht gedownloaded werden:\n{}'.format(failed_downloads))
    if len(failed_convert) < 1: update_scrollbar_text(text_update='[INFO] Der Prozess wurde ohne Konvertierungsfehler abgeschlossen.')
    else: update_scrollbar_text(text_update='[INFO] Der Prozess wurde mit Konvertierungsfehler(n) abgeschlossen.\nFolgende Titel konnten nicht konvertiert werden:\n{}'.format(failed_convert))


# -------------------------------
# WEBSCRAPE
# -------------
# define function that manages search_target and search_tag for webscrape
########################################################################################################################
# FIX web scrape presicion
########################################################################################################################
def get_video_urls(url, time_sleep):
    url_type = check_url_type(url)
    if url_type == 'watch_playlist':
        search_target = 'ytd-playlist-panel-video-renderer'
        search_tag = 'watch.*list'
        links = start_driver(url, url_type, time_sleep, search_target, search_tag)
    elif url_type == 'overview_playlist':
        search_target = 'ytd-playlist-video-renderer'
        search_tag = 'watch.*list'
        links = start_driver(url, url_type, time_sleep, search_target, search_tag)
    elif url_type == 'channel_videos':
        search_target = 'ytd-grid-video-renderer'
        search_tag = 'href=[\'"]?([^\'" >]+)'
        links = start_driver(url, url_type, time_sleep, search_target, search_tag)
    elif url_type == 'single_video': links = [[url]]
    else: update_scrollbar_text(text_update='[FEHLER] Es konnten keine gültigen Links erzeugt werden.\nIst der folgende Link korrekt?\n"{}"'.format(url))
    return links


# -------------
# define function that sets up web driver
def set_up_driver():
    update_scrollbar_text(text_update='[ACHTUNG] Ein Browser öffnet sich automatisch!\n[ACHTUNG] Nicht schließen!')
    try:
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver_choice = 'Firefox'
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver_choice = 'Chrome'
    update_scrollbar_text(text_update='[ACHTUNG] {} hat sich geöffnet.\n[ACHTUNG] Nicht schließen!'.format(driver_choice))
    return driver


# -------------
# define function that scraps links from page_source
def start_driver(url, url_type, time_sleep, search_target, search_tag):
    driver = set_up_driver()
    driver.set_window_size(800, 600)
    driver.get(url)
    for second in range(time_sleep, 0, -1):
        update_scrollbar_text(text_update='[INFO] Der Prozess startet in {} Sekunden...'.format(second))
        sleep(1)
    soup = bs(driver.page_source, 'html.parser')
    target = soup.find_all(search_target)
    try:
        driver.quit()
        update_scrollbar_text(text_update='[INFO] Der Browser wurde ordnungsgemäß geschlossen.')
    except:
        update_scrollbar_text(text_update='[FEHLER] Der Browser konnte nicht ordnungsgemäß geschlossen werden.\nDas Broswerfenster kann dennoch jetzt geschlossen werden.')
    if len(target) > 0:
        urls = findall(search_tag, str(target))
        links = generate_links(urls=urls, url_type=url_type)
    else: update_scrollbar_text(text_update='[FEHLER] Es konnten keine Informationen aus dem Browser gewonnen werden.')
    return links


# -------------------------------
# INPUT AND PATHS
# -------------
# define function that determines local_path
def get_local_path():
    local_path = getcwd()
    local_path = local_path + '\\'
    return local_path


# -------------
# define function that makes directory
def make_dir(_path):
    if not path.exists(_path):
        try:
            mkdir(_path)
            update_scrollbar_text(text_update='[INFO] Der Pfad "{}" wurde erstellt.'.format(_path))
        except: update_scrollbar_text(text_update='[FEHLER] Der Pfad "{}" konnte nicht erstellt werden.'.format(_path))
    else: pass


# -------------
# function that generates config.txt when missing
def initialize_config_file(file='config.txt'):
    local_path = get_local_path()
    download_path = local_path + 'video_download\\'
    mp3_path = local_path + 'mp3\\'
    with open(file, 'w+') as f:
        for i in range(3):
            if i == 0: f.writelines(download_path + '\n')
            elif i == 1: f.writelines(mp3_path + '\n')


# -------------
# function that reads file and returns values
def read_file(file='config.txt'):
    file = open(file, 'r') 
    values = file.readlines()
    updated_values = [value.replace('\n','') for value in values] 
    file.close()
    return updated_values


# -------------
# function that reads config.txt and returns configuration
def get_configs():
    try: values = read_file()
    except:
        initialize_config_file()
        values = read_file()
    download_path = str(values[0])
    mp3_path = str(values[1])
    return download_path, mp3_path


# ---------------------------------
# define function that generates list of videos to convert
def generate_convert_list(video_titels):
    convert_list = [(title + '.mp4') for title in video_titels]
    return convert_list


# -------------------------------
# LINK CHECK AND TRANSFORMATION
# -------------
# define function that determines type of url
########################################################################################################################
# FIX precsision of url_type detection
########################################################################################################################
def check_url_type(url):
    if 'https://www.youtube.com/playlist?list=' in url and 'playnext=' in url: url_type = 'watch_playlist'
    elif 'https://www.youtube.com/playlist?list=' in url: url_type = 'overview_playlist'
    elif 'https://www.youtube.com/' in url and '/videos' in url: url_type = 'channel_videos'
    elif 'https://www.youtube.com/watch?v=' in url: url_type = 'single_video'
    else: update_scrollbar_text(text_update='[FEHLER] Der URL-Typ wurde nicht erkannt.\nIst der folgende Link korrekt?\n"{}"'.format(url))
    return url_type


# -------------
# define function that generate downloadable links
########################################################################################################################
# FIX silencing when web scrap is more accurate
########################################################################################################################
def generate_links(urls, url_type):
    main_url = 'https://www.youtube.com/watch?v='
    if url_type == 'watch_playlist': links = [main_url + str(video_id[8:-9]) for video_id in urls[::2]]
    elif url_type == 'overview_playlist': links = [main_url + str(video_id[8:-9]) for video_id in urls[::2]]
    elif url_type == 'channel_videos': links = [main_url + str(video_id[9:]) for video_id in urls[::2]]
    elif url_type == 'single_video': links = main_url + str(urls[8:])
    else: update_scrollbar_text(text_update='[FEHLER] Es konnte kein Link erstellt werden.')
    return links


# -------------------------------
# DOWNLOAD AND CONVERT
# -------------
# function that cleans video title to legal characters
def clean_video_title(title):
    clean_title = sub('\W|^(?=\d)','_', title)
    return clean_title


# -------------
# case try of download
def try_download(link, video_titels, download_path):
    yt = YouTube(link)
    stream = yt.streams.first()
    title = yt.title
    cleaned_title = clean_video_title(title=title)
    video = stream.download(download_path, filename=cleaned_title)
    update_scrollbar_text(text_update='[INFO] Der Download von {} ist abgeschlossen.\nLink: {}'.format(cleaned_title, link))
    video_titels.append(cleaned_title)
    return video_titels

# -------------
# case exception of download
def except_download(link, failed_downloads):
    update_scrollbar_text(text_update='[FEHLER] Der Download von {} ist fehlgeschlagen.'.format(link))
    failed_downloads.append(link)
    return failed_downloads


# -------------
# download all videos from list
def dowload_videos(links, download_path):
    update_scrollbar_text(text_update='[INFO] Beginne mit dem Video-Download...')
    failed_downloads, video_titels = [], []
    if len(links) > 1:
        for link in links:
            try: video_titels = try_download(link=link, video_titels=video_titels, download_path=download_path)
            except: failed_downloads = except_download(link=link, failed_downloads=failed_downloads)
    else:
        link = links[0][0]
        try: video_titels = try_download(link=link, video_titels=video_titels, download_path=download_path)
        except: failed_downloads = except_download(link=link, failed_downloads=failed_downloads)
    return failed_downloads, video_titels


# -------------
# convert all videos in list
def convert_videos(videos, download_path, mp3_path, que):
    failed_convert = []
    for file in videos:
        try:
            video_file = VideoFileClip(path.join(download_path + '\\' + str(file)))
            video_file.audio.write_audiofile(path.join(mp3_path + '\\' + str(file[:-4]) + '.mp3'))
            update_scrollbar_text(text_update='[INFO] Die Konvertierung von {} war erfolgreich.'.format(file))
        except:
            update_scrollbar_text(text_update='[FEHLER]  Die Konvertierung von {} war nicht erfolgreich.'.format(file))
            failed_convert.append(str(file))
    que.put(failed_convert)


# -------------------------------
# PROCESS HANDLING
# -------------
# define function that starts main prozess on separate thread
def main_process(sleep_time, current_url, current_download_path, current_mp3_path):
    video_urls = get_video_urls(url=current_url, time_sleep=sleep_time)
    failed_downloads, video_titels = dowload_videos(links=video_urls, download_path=current_download_path)
    convert_state = convert_check_box_value.get()
    if convert_state is True:
        update_scrollbar_text(text_update='[INFO] Beginne mit dem konvertieren der Videos...')
        video_list = generate_convert_list(video_titels=video_titels)
        cpu_cores_to_use = cpu_drop_down_value.get() 
        splitted_video_list = split_list(list_to_split=video_list, cpu_threads=cpu_cores_to_use)
        failed_convert = set_up_processes(splitted_list=splitted_video_list, current_download_path=current_download_path, current_mp3_path=current_mp3_path) 
    else: failed_convert = []
    end_message(failed_downloads, failed_convert)


# -------------------------------
# MULTIPROCESSING
# -------------
# define function that manages list splitting depending on url and cpu count
def split_list(list_to_split, cpu_threads):
    len_urls = len(list_to_split) 
    num_cpu_threads = cpu_threads 
    chunks = min(num_cpu_threads, len_urls)
    splitted_list = [list_to_split[start::chunks] for start in range(chunks)]
    return splitted_list


# -------------
# define function that handels multiprocessing video converter function
########################################################################################################################
# FIX possible AssertionError: attempt to release recursive lock not owned by thread
########################################################################################################################
def set_up_processes(splitted_list, current_download_path, current_mp3_path):
    que = Queue()
    full_failed_convert, processes = [], []
    counter = 0
    for item in splitted_list:
        thread_ = Thread(target=convert_videos, args=(item, current_download_path, current_mp3_path, que, ))
        thread_.name = 'convert_thread_' + str(counter)
        thread_.start()
        processes.append(thread_)
        sleep(0.05)
        counter += 1
    for thread_ in processes:
        thread_.join()
        failed_convert = que.get()
        full_failed_convert += failed_convert
        sleep(0.05)
    return full_failed_convert


# -------------------------------------------
# PROGRAMM SET UP
if __name__ == '__main__':
    # ---------------------------
    # main definition of gui
    root = Tk() 
    root.title('Pylo - You-Tube-Downloader und Konverter v_b0.9.9') 
    icon_path = get_local_path()
    root.iconbitmap(icon_path + 'icon.ico') 
    root.geometry("650x765") 
    root.resizable(width=False, height=False) 


    # ---------------------------
    # call initial functions and set inital values
    input_box_width = 68
    scrollbar_height = 10
    download_path, mp3_path = get_configs()


    # ---------------------------
    # PLACE WIDGETS
    # -------------
    # sleep time input box
    sleep_time_input_box, sleep_time_label = set_up_leep_time_input_box()
    sleep_time_label.pack()
    sleep_time_input_box.pack()
    # -------------
    # space
    spacer(widget=sleep_time_input_box, x=0, y=10)
    # -------------
    # dropdown menu - cpu
    cpu_drop_down_menu, cpu_drop_down_label, cpu_drop_down_value = set_up_cpu_drop_down_menu()
    cpu_drop_down_label.pack()
    cpu_drop_down_menu.pack()
    # -------------
    # separator
    separator(x=0, y=155, width=1)
    # -------------
    # url input
    url_input_box, url_input_label = set_up_url_input()
    url_input_label.pack()
    url_input_box.pack()
    # -------------
    # download_path
    download_input_box, download_path_label = set_up_download_path_input()
    download_path_label.pack()
    download_input_box.pack()
    # -------------
    # space
    spacer(widget=download_input_box, x=0, y=10)
    # -------------
    # check box for converting
    convert_check_box, convert_check_box_value = set_up_convert_check_box()
    convert_check_box.pack()
    # -------------
    # space
    spacer(widget=convert_check_box, x=0, y=10)
    # -------------
    # mp3_path
    mp3_label, mp3_input_box = set_up_mp3_path_input()
    mp3_label.pack()
    mp3_input_box.pack()
    # -------------
    # space
    spacer(widget=mp3_input_box, x=0, y=15)
    # -------------
    # save bottom for settings
    settings_save_buttom = set_up_settings_save_buttom()
    settings_save_buttom.pack()
    # -------------
    # space
    spacer(widget=settings_save_buttom, x=0, y=5)
    # -------------
    # set up start_bottom
    start_bottom = set_up_start_bottom()
    start_bottom.pack()
    # -------------
    # space
    spacer(widget=start_bottom, x=0, y=20)
    # -------------
    # output window
    scrollbar, scrollbar_text = set_up_scrollbar()
    scrollbar_text.pack(anchor='center')
    # -------------
    # space
    spacer(widget=start_bottom, x=0, y=25)
    # -------------
    # source code
    source_label = Label(root, text=r"https://github.com/trh0ly/youtube_downloader_converter", fg="blue", cursor="hand2")
    source_label.pack()


    # -------------------------------------------
    # MAINLOOP
    root.mainloop()
