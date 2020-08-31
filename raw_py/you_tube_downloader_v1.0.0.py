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


# -------------------------------------------
# define functions
# -------------------------------
# GUI
# -------------
# dropdown menu - cpu
def set_up_cpu_drop_down_menu():
    # set default drop_down_value for cpu count as int
    cpu_drop_down_value = IntVar()
    cpu_drop_down_value.set(get_core_count_list()[0])
    cpu_drop_down_label = Label(frame_1, text="Anzahl der CPU-Threads:", font=font_normal()) # create label for drop down menu
    # set up drop down menu with options
    cpu_drop_down_menu = OptionMenu(frame_1, cpu_drop_down_value, *get_core_count_list())
    cpu_drop_down_menu.config(font=font_normal())
    return cpu_drop_down_menu, cpu_drop_down_label, cpu_drop_down_value


# -------------
# sleep timer input
def set_up_leep_time_input_box():
    sleep_time_label = Label(frame_1, text="Verzögerung beim Download", font=font_normal(())) # create label for sleep_time_input_box
    #spacer(widget=sleep_time_label, x=0, y=10) # space
    sleep_time_deafult_value = IntVar(frame_1, 10) # set default installation_check_box_value for sleep_time_input_box
    sleep_time_input_box = Entry(frame_1, width=5, font=font_normal(), textvariable=sleep_time_deafult_value)  # set up sleep_time_input_box
    sleep_time_input_box.bind("<Button-1>", clear_on_click) # clear on click
    return sleep_time_input_box, sleep_time_label


# -------------
# url input
def set_up_url_input():
    url_input_label = Label(frame_2, text="URL der Playlist/ des Videos:", font=font_bold())
    #spacer(widget=url_input_label, x=0, y=20) # space
    url_input_box_value = StringVar(frame_2, 'URL einfügen') # set default url_input_box_value for url_input_box
    url_input_box = Entry(frame_2, width=input_box_width, font=font_normal(), textvariable=url_input_box_value) # set up url_input_box
    url_input_box.bind("<Button-1>", clear_on_click) # clear on click
    return url_input_box, url_input_label


# -------------
# download_path
def set_up_download_path_input():
    download_path_label = Label(frame_2, text="Download-Pfad für die Videos:", font=font_bold(())) # create label for download_path_input_box
    #spacer(widget=download_path_label, x=0, y=10) # space
    download_input_box_deafult_value = StringVar(frame_2, download_path) # set default installation_check_box_value for download_input_box
    download_input_box = Entry(frame_2, width=input_box_width, font=font_normal(), textvariable=download_input_box_deafult_value)  # set up download_input_box
    return download_input_box, download_path_label


# -------------
# check box for converting
def set_up_convert_check_box():
    # set default installation_check_box_value for installation status
    convert_check_box_value = BooleanVar()
    convert_check_box_value.set(True)
    convert_check_box = Checkbutton(frame_2, text="Konvertiere gedownloadete Videos in MP3", variable=convert_check_box_value, font=font_normal()) # create check box for installation status
    return convert_check_box, convert_check_box_value


# -------------
# mp3_path
def set_up_mp3_path_input():
    mp3_label = Label(frame_2, text="Speicherort für die MP3's:", font=font_bold()) # create label for mp3_path
    #spacer(widget=mp3_label, x=0, y=5) # space
    mp3_input_box_value = StringVar(frame_2, mp3_path)  # set default mp3_input_box_value for mp3_path
    mp3_input_box = Entry(frame_2, width=input_box_width, font=font_normal(), textvariable=mp3_input_box_value) # set up mp3_path
    return mp3_label, mp3_input_box


# -------------
# save bottom for settings
def set_up_settings_save_buttom():
    settings_save_buttom = Button(frame_2, text="Einstellungen übernehmen", font=font_normal(),  command=save_buttom_on_click)  # set up settings_save_buttom
    return settings_save_buttom


# -------------
# set up start_bottom
def set_up_start_bottom():
    start_bottom = Button(frame_2, text="Prozess starten", font=font_bold(), command=start_main_process_thread)  # set up set_up_start_bottom
    return start_bottom


# -------------
# output window
def set_up_scrollbar():
    scrollbar = Scrollbar(frame_2)
    scrollbar_text = Text(frame_2, height=scrollbar_height, width=(input_box_width + 6))
    scrollbar.config(command=scrollbar_text.yview)
    #scrollbar.pack(side=RIGHT, fill=Y, anchor='center') # set up scroll bar
    return scrollbar, scrollbar_text


# ----------------------
# function that determine usable cpu cores for multiprocessing
def get_core_count_list():
    core_count = cpu_count() # get cpu core count
    options = [1] # set default value
    # pass if core count is below 3
    if core_count <= 3: pass
    # else add extra options for usable cpu cores
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
#def spacer(widget, x=0, y=10):
#    widget.pack(padx=x, pady=y)


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
    blank = str('#' + '-' * blank_size + '#\n') # define blank
    text_update = str(text_update) + '\n' # define text update
    # make scrollbar editable insert text and lock
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
    _, new_download_path, new_mp3_path, _ = get_runtime_settings() # get values from input and check boxes
    # open acutal config file and update configs
    acutal_config_values = read_file(file)
    with open(file, 'w') as f:
        for i, line in enumerate(acutal_config_values, 0):
            if i == 0: f.writelines(str(new_download_path) + '\n')  # download path
            elif i == 1: f.writelines(str(new_mp3_path) + '\n')  # mp3 path
    # print to scrollbar
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
    url_type = check_url_type(url) # check url type
    # define search_target and search_tag and get links
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
    # try to use firefox
    try:
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver_choice = 'Firefox'
    # try to use chrome
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver_choice = 'Chrome'
    update_scrollbar_text(text_update='[ACHTUNG] {} hat sich geöffnet.\n[ACHTUNG] Nicht schließen!'.format(driver_choice))
    return driver


# -------------
# define function that scraps links from page_source
def start_driver(url, url_type, time_sleep, search_target, search_tag):
    driver = set_up_driver()  # set up driver
    driver.set_window_size(800, 600) # open driver window
    driver.get(url)
    for second in range(time_sleep, 0, -1):
        update_scrollbar_text(text_update='[INFO] Der Prozess startet in {} Sekunden...'.format(second))
        sleep(1) # wait some seconds
    soup = bs(driver.page_source, 'html.parser') # get page_source from url
    target = soup.find_all(search_target)
    # check if there is page_source
    try:
        driver.quit()
        update_scrollbar_text(text_update='[INFO] Der Browser wurde ordnungsgemäß geschlossen.')
    except:
        update_scrollbar_text(text_update='[FEHLER] Der Browser konnte nicht ordnungsgemäß geschlossen werden.\nDas Broswerfenster kann dennoch jetzt geschlossen werden.')
    if len(target) > 0:
        urls = findall(search_tag, str(target))
        links = generate_links(urls=urls, url_type=url_type)
    # if there is no information return empy list
    else: update_scrollbar_text(text_update='[FEHLER] Es konnten keine Informationen aus dem Browser gewonnen werden.')
    return links


# -------------------------------
# INPUT AND PATHS
# -------------
# define function that determines local_path
def get_local_path():
    local_path = getcwd() # get acutal path
    local_path = local_path + '\\'
    return local_path


# -------------
# define function that makes directory
def make_dir(_path):
    # Create target directory if don't exist
    if not path.exists(_path):
        try:
            mkdir(_path)
            update_scrollbar_text(text_update='[INFO] Der Pfad "{}" wurde erstellt.'.format(_path))
        except: update_scrollbar_text(text_update='[FEHLER] Der Pfad "{}" konnte nicht erstellt werden.'.format(_path))
    else: pass


# -------------
# function that generates config.txt when missing
def initialize_config_file(file='config.txt'):
    # get local path and determine download_path, mp3_path
    local_path = get_local_path()
    download_path = local_path + 'video_download\\'
    mp3_path = local_path + 'mp3\\'
    # create config.txt and insert values
    with open(file, 'w+') as f:
        for i in range(3):
            if i == 0: f.writelines(download_path + '\n') # download path
            elif i == 1: f.writelines(mp3_path + '\n') # mp3 path


# -------------
# function that reads file and returns values
def read_file(file='config.txt'):
    file = open(file, 'r') # open file
    values = file.readlines() # read values
    updated_values = [value.replace('\n','') for value in values] # replace line break
    file.close() # close file
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
    if 'https://www.youtube.com/playlist?list=' in url and 'playnext=' in url: url_type = 'watch_playlist'  # watch list which is playing
    elif 'https://www.youtube.com/watch?v=' in url and '&list=' in url: url_type = 'watch_playlist'  # watch list which is playing 2
    elif 'https://www.youtube.com/playlist?list=' in url: url_type = 'overview_playlist'  # watch list in overview mode
    elif 'https://www.youtube.com/' in url and '/videos' in url: url_type = 'channel_videos'  # you tube channel video
    elif 'https://www.youtube.com/watch?v=' in url: url_type = 'single_video'  # single video
    else: update_scrollbar_text(text_update='[FEHLER] Der URL-Typ wurde nicht erkannt.\nIst der folgende Link korrekt?\n"{}"'.format(url))
    return url_type


# -------------
# define function that generate downloadable links
########################################################################################################################
# FIX silencing when web scrap is more accurate
########################################################################################################################
def generate_links(urls, url_type):
    main_url = 'https://www.youtube.com/watch?v='
    if url_type == 'watch_playlist': links = [main_url + str(video_id[8:-9]) for video_id in urls[::2]] # watch list which is playing
    elif url_type == 'overview_playlist': links = [main_url + str(video_id[8:-9]) for video_id in urls[::2]]  # watch list in overview mode
    elif url_type == 'channel_videos': links = [main_url + str(video_id[9:]) for video_id in urls[::2]]  # you tube channel video
    elif url_type == 'single_video': links = main_url + str(urls[8:]) # single video
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
            # try to download videos
            try: video_titels = try_download(link=link, video_titels=video_titels, download_path=download_path)
             # if failure print statement and pass
            except: failed_downloads = except_download(link=link, failed_downloads=failed_downloads)
    else:
        link = links[0][0]
        # try to download video
        try: video_titels = try_download(link=link, video_titels=video_titels, download_path=download_path)
        # if failure print statement
        except: failed_downloads = except_download(link=link, failed_downloads=failed_downloads)
    return failed_downloads, video_titels


# -------------
# convert all videos in list
def convert_videos(videos, download_path, mp3_path, que):
    failed_convert = []
    for file in videos:
        # try to convert
        try:
            video_file = VideoFileClip(path.join(download_path + '\\' + str(file)))
            video_file.audio.write_audiofile(path.join(mp3_path + '\\' + str(file[:-4]) + '.mp3'))
            update_scrollbar_text(text_update='[INFO] Die Konvertierung von {} war erfolgreich.'.format(file))
        # if failure print statement and pass
        except:
            update_scrollbar_text(text_update='[FEHLER]  Die Konvertierung von {} war nicht erfolgreich.'.format(file))
            failed_convert.append(str(file))
    que.put(failed_convert)


# -------------------------------
# PROCESS HANDLING
# -------------
# define function that starts main prozess on separate thread
def main_process(sleep_time, current_url, current_download_path, current_mp3_path):
    video_urls = get_video_urls(url=current_url, time_sleep=sleep_time) # get video urls
    failed_downloads, video_titels = dowload_videos(links=video_urls, download_path=current_download_path) # download videos
    # get convert state and convert/ not convert videos to mp3
    convert_state = convert_check_box_value.get()
    # convert videos
    if convert_state is True:
        update_scrollbar_text(text_update='[INFO] Beginne mit dem konvertieren der Videos...')
        video_list = generate_convert_list(video_titels=video_titels) # get titels to convert (downloaded in actual session)
        cpu_cores_to_use = cpu_drop_down_value.get() # get number of cpu cores to use
        splitted_video_list = split_list(list_to_split=video_list, cpu_threads=cpu_cores_to_use) # split video_list into chunks
        failed_convert = set_up_processes(splitted_list=splitted_video_list, current_download_path=current_download_path, current_mp3_path=current_mp3_path) # convert videos
    else: failed_convert = []
    end_message(failed_downloads, failed_convert)  # print end message


# -------------------------------
# MULTIPROCESSING
# -------------
# define function that manages list splitting depending on url and cpu count
def split_list(list_to_split, cpu_threads):
    len_urls = len(list_to_split) # determine len of jobs
    num_cpu_threads = cpu_threads # get cpu cores to use
    chunks = min(num_cpu_threads, len_urls) # set count of chunks to min of cores to use or jobs
    splitted_list = [list_to_split[start::chunks] for start in range(chunks)]
    return splitted_list


# -------------
# define function that handels multiprocessing video converter function
########################################################################################################################
# FIX possible AssertionError: attempt to release recursive lock not owned by thread
########################################################################################################################
def set_up_processes(splitted_list, current_download_path, current_mp3_path):
    que = Queue() # set up queue
    full_failed_convert, processes = [], []
    counter = 0
    # start a thread for every job in splitted_list
    for item in splitted_list:
        thread_ = Thread(target=convert_videos, args=(item, current_download_path, current_mp3_path, que, )) # define thread
        thread_.name = 'convert_thread_' + str(counter) # name thread
        thread_.start() # start thread
        processes.append(thread_)
        sleep(0.05)
        counter += 1
    # join processes for clean exit
    for thread_ in processes:
        thread_.join()
        failed_convert = que.get() # get function return
        full_failed_convert += failed_convert
        sleep(0.05)
    return full_failed_convert


# -------------------------------------------
# PROGRAMM SET UP
if __name__ == '__main__':
    # ---------------------------
    # main definition of gui
    root = Tk() # main
    root.title('Pylo You-Tube-Downloader und Konverter v_1.0.0') # title
    icon_path = get_local_path()
    root.iconbitmap(icon_path + 'icon.ico') # icon
    root.geometry("650x580") # window size
    root.resizable(width=False, height=False) # resizable is forbidden


    # ---------------------------
    # call initial functions and set inital values
    input_box_width = 68
    scrollbar_height = 10
    download_path, mp3_path = get_configs()


    # ---------------------------
    # PLACE WIDGETS
    # -------------
    # frame_1
    frame_1 = Frame()
    frame_1.grid(row=0, column=0, sticky='NSWE')

    # -------------
    # sleep time input box
    sleep_time_input_box, sleep_time_label = set_up_leep_time_input_box()
    sleep_time_label.grid(row=1, column=0, padx=5, pady=5, sticky='W')
    sleep_time_input_box.grid(row=1, column=1, padx=5, pady=5, sticky='W')
    # -------------
    # dropdown menu - cpu
    cpu_drop_down_menu, cpu_drop_down_label, cpu_drop_down_value = set_up_cpu_drop_down_menu()
    cpu_drop_down_label.grid(row=1, column=2, padx=5, pady=5, sticky='E')
    cpu_drop_down_menu.grid(row=1, column=3, padx=5, pady=5, sticky='E')

    # -------------
    # frame_2
    frame_2 = Frame()
    frame_2.grid(row=1, column=0, sticky='NSWE')
    # -------------
    # url input
    url_input_box, url_input_label = set_up_url_input()
    url_input_label.grid(row=3, column=0, padx=5, pady=5, sticky='WE')
    url_input_box.grid(row=4, column=0, padx=5, pady=5, sticky='W')
    # -------------
    # download_path
    download_input_box, download_path_label = set_up_download_path_input()
    download_path_label.grid(row=5, column=0, padx=5, pady=5, sticky='WE')
    download_input_box.grid(row=6, column=0, padx=5, pady=5, sticky='W')
    # -------------
    # check box for converting
    convert_check_box, convert_check_box_value = set_up_convert_check_box()
    convert_check_box.grid(row=7, column=0, padx=5, pady=5, sticky='WE')
    # -------------
    # mp3_path
    mp3_label, mp3_input_box = set_up_mp3_path_input()
    mp3_label.grid(row=8, column=0, padx=5, pady=5, sticky='WE')
    mp3_input_box.grid(row=9, column=0, padx=5, pady=5, sticky='W')
    # -------------
    # save bottom for settings
    settings_save_buttom = set_up_settings_save_buttom()
    settings_save_buttom.grid(row=10, column=0, padx=5, pady=5, sticky='WE')
    # -------------
    # set up start_bottom
    start_bottom = set_up_start_bottom()
    start_bottom.grid(row=11, column=0, padx=5, pady=5, sticky='WE')
    # -------------
    # output window
    scrollbar, scrollbar_text = set_up_scrollbar()
    scrollbar.grid(row=12, column=1, padx=5, pady=5, sticky='NSWE')
    scrollbar_text.grid(row=12, column=0, padx=5, pady=5, sticky='NSWE')
    # -------------
    # source code
    source_label = Label(frame_2, text=r"https://github.com/trh0ly/youtube_downloader_converter", fg="blue", cursor="hand2")
    source_label.grid(row=13, column=0, padx=5, pady=5, sticky='WE')
    # -------------------------------------------
    # MAINLOOP
    root.mainloop()