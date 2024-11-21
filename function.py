import customtkinter as ctk
import os, shutil
import random
import webbrowser
import time
import json, sys
from datetime import datetime
from themes import get_theme, THEMES


current_schedule = ""
schedule_data = [["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""]]
raw_schedule_data = [["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""],
                  ["", "", "", "", "", ""]]

def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    
def get_config_path(file_name):
    return file_name
    
config_path = get_config_path("misc/configuration.json")
config = load_config(config_path)

colors = get_theme(config["theme_using"])

def home_frame_function(frame):
    clock_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 245), fg_color="transparent", text_color=colors["text_color"])
    clock_label.grid(row=0, column=0, sticky="nsew")

    def update_time():
        current_time = time.strftime("%H:%M:%S")
        clock_label.configure(text=current_time)
        clock_label.after(1000, update_time)

    motivational_quotes = [
        {"quote": "The only way to do great work is to love what you do.", "source": "Steve Jobs", "link": "https://www.goodreads.com/quotes/772887-the-only-way-to-do-great-work-is-to-love"},
        {"quote": "Success is not the key to happiness. Happiness is the key to success.", "source": "Albert Schweitzer", "link": "https://www.brainyquote.com/quotes/albert_schweitzer_155988"},
        {"quote": "It does not matter how slowly you go as long as you do not stop.", "source": "Confucius", "link": "https://www.brainyquote.com/quotes/confucius_140908"},
        {"quote": "When something is important enough, you do it even if the odds are not in your favor.", "source": "Elon Musk", "link": "https://www.brainyquote.com/quotes/elon_musk_567219"},
        {"quote": "Start where you are. Use what you have. Do what you can.", "source": "Arthur Ashe", "link": "https://www.brainyquote.com/quotes/arthur_ashe_371527"},
        {"quote": "Good, better, best. Never let it rest. 'Til your good is better and your better is best.", "source": "St. Jerome", "link": "https://www.brainyquote.com/quotes/st_jerome_389605"},
        {"quote": "Everything you've ever wanted is on the other side of fear.", "source": "George Addair", "link": "https://www.brainyquote.com/quotes/george_addair_175673"}
    ]

    quote_text = ctk.StringVar()
    quote_text.set("Nhấn vào đây để xem nguồn")
    quote_label = ctk.CTkLabel(frame, textvariable=quote_text, font=("Helvetica", 20), text_color="blue")
    quote_label.grid(row=2, column=0)

    def show_random_quote():
        quote = random.choice(motivational_quotes)
        quote_text.set(f'"{quote["quote"]}" - {quote["source"]}')
        quote_label.unbind("<Button-1>")
        quote_label.bind("<Button-1>", lambda e: open_link(quote["link"]))

    def open_link(url):
        webbrowser.open(url)
        show_random_quote()

    quote_label.bind("<Button-1>", lambda e: show_random_quote())
    show_random_quote()
    update_time()
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

# ===========================================================================================================

def schedule_frame_function(frame):
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    schedule_name = "" if current_schedule is None else current_schedule.split('_', 1)[1].replace('.txt', '')
    ctk.CTkLabel(frame, text=f"Tên TKB: {schedule_name}", font=("Arial", 20), text_color=colors["text_color"]).grid(row=0, column=0, sticky="nw")

    schedule_table = ctk.CTkFrame(frame, width=1000, height=600, fg_color="transparent")
    schedule_table.grid(row=1, column=0)

    create_schedule_table(schedule_table)

    frame.grid_rowconfigure(2, weight=1)
    
    buttons_frame = ctk.CTkFrame(frame, fg_color="transparent")
    buttons_frame.grid(row=2, column=0, sticky="nw")
    
    new_schedule_button = ctk.CTkButton(buttons_frame, text="Thêm TKB", width=150, font=("Arial", 20), text_color=colors["text_color"], command=lambda: create_new_schedule())
    new_schedule_button.grid(row=0, column=0, padx=20)

    load_schedule_button = ctk.CTkButton(buttons_frame, text="Chọn TKB", width=150, font=("Arial", 20), text_color=colors["text_color"], command=lambda: load_schedule_dialog())
    load_schedule_button.grid(row=0, column=1, padx=20)
    
    delete_schedule_button = ctk.CTkButton(buttons_frame, text="Xóa TKB", width=150, font=("Arial", 20), text_color=colors["text_color"], command=lambda: delete_schedules())
    delete_schedule_button.grid(row=0, column=2, padx=20)

    def delete_schedules():
        delete_dialog = ctk.CTkToplevel(fg_color=colors["background"])
        delete_dialog.title("Xóa thời khóa biểu")
        delete_dialog.geometry("300x400")
        delete_dialog.resizable(False, False)
        delete_dialog.grab_set()
        delete_dialog.transient(frame)

        schedule_label = ctk.CTkLabel(delete_dialog, text="Chọn thời khóa biểu cần xóa:", font=("Helvetica", 16), text_color=colors["text_color"])
        schedule_label.pack(pady=10)

        scroll_frame = ctk.CTkScrollableFrame(delete_dialog, width=270, height=280, fg_color=colors["background"])
        scroll_frame.pack()

        checkbox_var = {}
        schedule_files = os.listdir(f"saves/{config['current_user']}/schedules")

        for file in schedule_files:
            name = file.split('_', 1)[1].replace(".txt", "")
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(scroll_frame, text=name, variable=var, onvalue=True, offvalue=False, text_color=colors["text_color"])
            checkbox.pack(anchor="w", pady=5)
            checkbox_var[file] = var

        confirm_button = ctk.CTkButton(delete_dialog, text="Xác nhận", command=lambda: confirm_delete())
        confirm_button.pack(pady=10)

        def confirm_delete():
            selected_schedules = [schedule for schedule, var in checkbox_var.items() if var.get()]
            if selected_schedules:
                for schedule in selected_schedules:
                    schedule_path = os.path.join(f"saves/{config['current_user']}/schedules", schedule)
                    if os.path.exists(schedule_path):
                        os.remove(schedule_path)
                delete_dialog.destroy()
                restart_app(frame)

    def load_schedule_dialog():
        load_dialog = ctk.CTkToplevel(fg_color=colors["background"])
        load_dialog.title("Chọn thời khóa biểu")
        load_dialog.geometry("250x320")
        load_dialog.resizable(False, False)
        load_dialog.grab_set()
        
        schedule_label = ctk.CTkLabel(load_dialog, text="Chọn thời khóa biểu:", font=("Arial", 16), text_color=colors["text_color"])
        schedule_label.pack(pady=10)
        
        scroll_frame = ctk.CTkScrollableFrame(load_dialog, width=350, height=400, fg_color=colors['nav_bar'])
        scroll_frame.pack(pady=10)
        
        schedule_files = os.listdir(f"saves/{config['current_user']}/schedules")
        for file in schedule_files:
            name = file.split('_', 1)[1].replace(".txt", "")
            btn = ctk.CTkButton(
                scroll_frame, 
                text=name,
                command=lambda f=file: select_schedule(f, load_dialog),
                fg_color=colors["background"],
                text_color=colors["text_color"],
                hover_color=colors["dropdown_hover_color"],
                anchor='w'
            )
            btn.pack(pady=5, fill="x")
            
    def select_schedule(filename, dialog):
        old_path = f"saves/{config['current_user']}/schedules/{filename}"
        new_filename = f"{int(time.time())}_{filename.split('_', 1)[1]}"
        new_path = f"saves/{config['current_user']}/schedules/{new_filename}"
    
        os.rename(old_path, new_path)
        dialog.destroy()
        restart_app(frame)

    def create_new_schedule():
        new_schedule_window = ctk.CTkToplevel(fg_color=colors["background"])
        new_schedule_window.title("Tạo thời khóa biểu mới")
        new_schedule_window.geometry("660x500")
        new_schedule_window.resizable(False, False)
        new_schedule_window.attributes("-topmost", True)

        schedule_entries = []
        new_schedule_name = ctk.CTkEntry(new_schedule_window, width=150, fg_color=colors["background"], text_color=colors["text_color"], placeholder_text="Nhập tên TKB mới")
        new_schedule_name.grid(row=11, column=0, columnspan=6, padx=5, pady=5)
    
        weekdays = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"] 
        for i, day in enumerate(weekdays):
            ctk.CTkLabel(new_schedule_window, text=day, font=("Arial", 20), text_color=colors["text_color"]).grid(row=0, column=i, padx=5, pady=5)

        for row in range(10):
            row_entries = []
            for col in range(6):
                entry = ctk.CTkEntry(new_schedule_window, width=100, fg_color=colors["background"], text_color=colors["text_color"])
                entry.grid(row=row+1, column=col, padx=5, pady=5)
                row_entries.append(entry)
            schedule_entries.append(row_entries)

        def save_schedule():
            new_name = new_schedule_name.get()
            if new_name:
                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{new_name}.txt"
                with open(f"saves/{config['current_user']}/schedules/{filename}", "w+", encoding='utf-8') as f:
                    for row in range(10): 
                        line = []
                        for col in range(6):  
                            subject = schedule_entries[row][col].get()
                            if subject != "":
                                line.append(subject)
                            else:
                                line.append("-")
                        f.write(" ".join(line) + "\n")

                new_schedule_window.destroy()
                restart_app(frame)

        save_button = ctk.CTkButton(new_schedule_window, text="Lưu", command=save_schedule)
        save_button.grid(row=12, columnspan=6, pady=10)
    
def create_schedule_table(frame):
    frame.grid_columnconfigure(tuple(range(8)), weight=1)  
    frame.grid_rowconfigure(tuple(range(12)), weight=1) 
    ctk.CTkLabel(frame, text="Sáng", font=("Arial", 20), text_color=colors["text_color"]).grid(row=4, column=0, sticky="nsew")
    ctk.CTkLabel(frame, text="Chiều", font=("Arial", 20), text_color=colors["text_color"]).grid(row=10, column=0, sticky="nsew")
    
    ctk.CTkLabel(frame, text="Tiết", font=("Arial", 20), text_color=colors["text_color"]).grid(row=0, column=1, padx=10, sticky="nsew")
    for i in range(2, 7):
        ctk.CTkLabel(frame, text=str(i-1), font=("Arial", 18), text_color=colors["text_color"]).grid(row=i, column=1, padx=10, sticky="nsew")
        ctk.CTkLabel(frame, text=str(i-1), font=("Arial", 18), text_color=colors["text_color"]).grid(row=i+6, column=1, padx=10, sticky="nsew")

    weekdays = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"] 
    for i, weekday in enumerate(weekdays):
        ctk.CTkLabel(frame, text=weekday, font=("Arial", 20), text_color=colors["text_color"]).grid(row=0, column=i+2, padx=55, sticky="nsew")

    # line ngăn cách sáng chiều
    ctk.CTkFrame(frame, fg_color=colors["text_color"], height=2).grid(row=7, column=0, columnspan=8, sticky="nsew")
    
    load_schedule_subjects(frame)

def load_schedule_subjects(frame):
    global schedule_data
    schedule_data = [["", "", "", "", "", ""] for _ in range(10)]
    raw_schedule_data = [["", "", "", "", "", ""] for _ in range(10)]
    
    if current_schedule != None:
        with open(f"saves/{config['current_user']}/schedules/{current_schedule}", "r", encoding='utf-8') as f:
            for i, line in enumerate(f.readlines()):
                temp_ls = line.strip().split(" ")
                for j, subject in enumerate(temp_ls):
                    if j < 6 and i < 10:
                        if (subject != '-'):
                            schedule_data[i][j] = subject
    else:
        schedule_data = raw_schedule_data.copy()

    # các cell môn học sáng
    today = datetime.now().weekday()
    for i in range(2, 7):
        for j in range(3, 9):
            frame_subject = ctk.CTkFrame(frame)
            if ((today + 1) % 7 == j-3 and (today + 1) % 7 != 6):
                frame_subject.configure(fg_color=colors["tomorrow_schedule"])
                frame_subject.grid(row=i, column=j-1, sticky="nsew")
                ctk.CTkLabel(frame_subject, text=schedule_data[i-2][j-3], font=("Arial", 18), text_color=colors["alt_text_color"], fg_color=colors["tomorrow_schedule"]).pack(fill="both", ipady=15, ipadx=8, expand=True)
            elif (today + 2) % 7 == j-3 and (today + 2) % 7 != 6:
                frame_subject.configure(fg_color=colors["day_after_tomorrow_schedule"])
                frame_subject.grid(row=i, column=j-1, sticky="nsew")
                ctk.CTkLabel(frame_subject, text=schedule_data[i-2][j-3], font=("Arial", 18), text_color=colors["alt_text_color"], fg_color=colors["day_after_tomorrow_schedule"]).pack(fill="both", ipady=15, ipadx=8, expand=True)
            else:
                ctk.CTkLabel(frame, text=schedule_data[i-2][j-3], font=("Arial", 18), text_color=colors["text_color"]).grid(row=i, column=j-1, padx=8, pady=15, sticky="nsew")


    # các cell môn học chiều
    for i in range(8, 13):
        for j in range(3, 9):
            frame_subject = ctk.CTkFrame(frame)
            if ((today + 1) % 7 == j-3 and (today + 1) % 7 != 6):
                frame_subject.configure(fg_color=colors["tomorrow_schedule"])
                frame_subject.grid(row=i, column=j-1, sticky="nsew")
                ctk.CTkLabel(frame_subject, text=schedule_data[i-3][j-3], font=("Arial", 18), text_color=colors["alt_text_color"], fg_color=colors["tomorrow_schedule"]).pack(fill="both", ipady=15, ipadx=8, expand=True)
            elif (today + 2) % 7 == j-3 and (today + 2) % 7 != 6:
                frame_subject.configure(fg_color=colors["day_after_tomorrow_schedule"])
                frame_subject.grid(row=i, column=j-1, sticky="nsew")
                ctk.CTkLabel(frame_subject, text=schedule_data[i-3][j-3], font=("Arial", 18), text_color=colors["alt_text_color"], fg_color=colors["day_after_tomorrow_schedule"]).pack(fill="both", ipady=15, ipadx=8, expand=True)
            else:
                ctk.CTkLabel(frame, text=schedule_data[i-3][j-3], font=("Arial", 18), text_color=colors["text_color"]).grid(row=i, column=j-1, padx=8, pady=15, sticky="nsew")
    
def get_current_schedule():
    schedule_dir = f"saves/{config['current_user']}/schedules"
    files = os.listdir(schedule_dir)
    if files:
        sorted_files = sorted(files, key=lambda x: int(x.split('_')[0]), reverse=True)
        return sorted_files[0]
    else:
        return None

current_schedule = get_current_schedule()

# ================================================================================================================================================

def note_frame_function(frame):
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    buttons_frame = ctk.CTkFrame(frame, fg_color="transparent")
    buttons_frame.grid(row=0, column=0, sticky="nw")

    save_note_button = ctk.CTkButton(buttons_frame, text="Lưu ghi chú", width=150, font=("Arial", 20), text_color=colors["text_color"], command=lambda: save_current_note())
    save_note_button.grid(row=0, column=0, padx=20, pady=5)
    load_note_button = ctk.CTkButton(buttons_frame, text="Chọn ghi chú", width=150, font=("Arial", 20), text_color=colors["text_color"], command=lambda: load_note_dialog())
    load_note_button.grid(row=0, column=1, padx=20, pady=5)

    delete_note_button = ctk.CTkButton(buttons_frame, text="Xóa ghi chú", width=150, font=("Arial", 20), text_color=colors["text_color"], command=lambda: delete_notes())
    delete_note_button.grid(row=0, column=2, padx=20, pady=5)

    note_name = ctk.CTkEntry(frame, width=200, font=("Arial", 16), text_color=colors["text_color"], fg_color=colors["background"], placeholder_text="Tên ghi chú")
    note_name.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    note_text = ctk.CTkTextbox(frame, width=800, height=670, font=("Arial", 16), text_color=colors["text_color"], fg_color=colors["note_background"])
    note_text.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
    def save_current_note():
        name = note_name.get()
        content = note_text.get("1.0", "end-1c")
        if name and content:
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{name}.txt"
            with open(f"saves/{config['current_user']}/notes/{filename}", "w+", encoding='utf-8') as f:
                f.write(content)
            restart_app(frame)

    def load_note_dialog():
        load_dialog = ctk.CTkToplevel(fg_color=colors["background"])
        load_dialog.title("Chọn ghi chú")
        load_dialog.geometry("250x320")
        load_dialog.resizable(False, False)
        load_dialog.grab_set()
        note_label = ctk.CTkLabel(load_dialog, text="Chọn ghi chú:", font=("Arial", 16), text_color=colors["text_color"])
        note_label.pack(pady=10)
        scroll_frame = ctk.CTkScrollableFrame(load_dialog, width=350, height=400, fg_color=colors['nav_bar'])
        scroll_frame.pack(pady=10)
        note_files = os.listdir(f"saves/{config['current_user']}/notes")
        for file in note_files:
            name = file.split('_', 1)[1].replace(".txt", "")
            btn = ctk.CTkButton(
                scroll_frame, 
                text=name,
                command=lambda f=file: load_note(f, load_dialog),
                fg_color=colors["background"],
                text_color=colors["text_color"],
                hover_color=colors["dropdown_hover_color"],
                anchor="w",
                width=300
            )
            btn.pack(pady=5, padx=5, anchor="w")

    def load_note(filename, dialog):
        with open(f"saves/{config['current_user']}/notes/{filename}", "r", encoding='utf-8') as f:
            content = f.read()
        note_text.delete("1.0", "end")
        note_text.insert("1.0", content)
        old_path = f"saves/{config['current_user']}/notes/{filename}"
        new_filename = f"{int(time.time())}_{filename.split('_', 1)[1]}"
        new_path = f"saves/{config['current_user']}/notes/{new_filename}"
        os.rename(old_path, new_path)
        dialog.destroy()

    def delete_notes():
        delete_dialog = ctk.CTkToplevel(fg_color=colors["background"])
        delete_dialog.title("Xóa ghi chú")
        delete_dialog.geometry("300x400")
        delete_dialog.resizable(False, False)
        delete_dialog.grab_set()
        delete_dialog.transient(frame)
        note_label = ctk.CTkLabel(delete_dialog, text="Chọn ghi chú cần xóa:", font=("Helvetica", 16), text_color=colors["text_color"])
        note_label.pack(pady=10)
        scroll_frame = ctk.CTkScrollableFrame(delete_dialog, width=270, height=280, fg_color=colors["background"])
        scroll_frame.pack()
        checkbox_var = {}
        note_files = os.listdir(f"saves/{config['current_user']}/notes")
        for file in note_files:
            name = file.split('_', 1)[1].replace(".txt", "")
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(scroll_frame, text=name, variable=var, onvalue=True, offvalue=False, command=lambda file=file: checkbox_var.update({file: var}), text_color=colors["text_color"])
            checkbox.pack(anchor="w", pady=5)
            checkbox_var[file] = var
        confirm_button = ctk.CTkButton(delete_dialog, text="Xác nhận", command=lambda: confirm_delete())
        confirm_button.pack(pady=10)
        def confirm_delete():
            selected_notes = [note for note, var in checkbox_var.items() if var.get()]
            if selected_notes:
                for note in selected_notes:
                    note_path = os.path.join(f"saves/{config['current_user']}/notes", note)
                    if os.path.exists(note_path):
                        os.remove(note_path)
                delete_dialog.destroy()
                restart_app(frame)

# ================================================================================================================================================

def setting_frame_function(frame):
    frame.grid_columnconfigure(1, weight=1)

    theme_label = ctk.CTkLabel(frame, text="Chọn giao diện:", font=("Arial", 16), text_color=colors["text_color"])
    theme_label.grid(row=0, column=0, sticky="w", padx=[10, 0])

    theme_option = list(THEMES.keys())
    theme_dropdown = ctk.CTkOptionMenu(frame, values=theme_option, command=lambda choice: apply_config("theme_using", choice, frame), dropdown_fg_color=colors["background"], dropdown_text_color=colors["text_color"], dropdown_hover_color=colors["dropdown_hover_color"])
    theme_dropdown.set(config['theme_using'])
    theme_dropdown.grid(row=1, column=0, sticky="n", padx=[10, 0])

    user_label = ctk.CTkLabel(frame, text="Chọn người dùng:", font=("Arial", 16), text_color=colors["text_color"])
    user_label.grid(row=2, column=0, sticky="w", padx=[10, 0])

    user_option = [folder for folder in os.listdir("saves") if os.path.isdir(os.path.join("saves", folder))]
    user_dropdown = ctk.CTkOptionMenu(frame, values=user_option, command=lambda choice: apply_config("current_user", choice, frame), dropdown_fg_color=colors["background"], dropdown_text_color=colors["text_color"], dropdown_hover_color=colors["dropdown_hover_color"])
    user_dropdown.set(config['current_user'])
    user_dropdown.grid(row=3, column=0, sticky="n", padx=[10, 0])

    add_user_button = ctk.CTkButton(frame, text="Thêm người dùng", command=lambda: add_user(frame))
    add_user_button.grid(row=4, column=0, sticky="n", padx=[10, 0], pady=[10, 0])

    delete_user_button = ctk.CTkButton(frame, text="Xóa người dùng", command=lambda: delete_user(frame))
    delete_user_button.grid(row=5, column=0, sticky="n", padx=[10, 0], pady=[10, 0])

def apply_config(config_name, choice, frame):
    if (config_name == "theme_using"):
        old_value = config['theme_using']
    elif (config_name == "current_user"):
        old_value = config['current_user']
        global current_schedule
        current_schedule = get_current_schedule()

    if (old_value == choice):
        return

    with open("misc/configuration.json", "r") as f:
        content = json.load(f)
    
    content[config_name] = choice

    with open("misc/configuration.json", "w") as f:
        json.dump(content, f, indent=4)
    
    restart_app(frame)

def add_user(frame):
    new_user_dialog = ctk.CTkToplevel(fg_color=colors["background"])
    new_user_dialog.title("Thêm người dùng")
    new_user_dialog.geometry("400x160")
    new_user_dialog.resizable(False, False)
    new_user_dialog.grab_set()
    new_user_dialog.transient(frame)

    user_label = ctk.CTkLabel(new_user_dialog, text="Nhập tên người dùng mới:", font=("Helvetica", 16), text_color=colors["text_color"])
    user_label.pack(pady=10)

    user_entry = ctk.CTkEntry(new_user_dialog, font=("Helvetica", 16), text_color=colors["text_color"], fg_color=colors["background"])
    user_entry.pack(pady=10)

    accept_button = ctk.CTkButton(new_user_dialog, text="Xác nhận", command=lambda: save_user(user_entry.get(), frame))
    accept_button.pack(pady=10)

    def save_user(user_name, frame):
        if user_name:
            user_folder = os.path.join("saves", user_name)
            if (not os.path.exists(user_folder)):
                os.makedirs(user_folder)
                child_folders = os.path.join(user_folder, "schedules")
                os.makedirs(child_folders)
                child_folders = os.path.join(user_folder, "notes")
                os.makedirs(child_folders)
                
                with open("misc/configuration.json", "r") as config_file:
                    content = json.load(config_file)
                content['current_user'] = user_name
                with open("misc/configuration.json", "w") as config_file:
                    json.dump(content, config_file, indent=4)

                new_user_dialog.destroy()
                restart_app(frame)
            else:
                user_label.configure(text="Tên người dùng đã tồn tại. Vui lòng chọn tên khác.")
                new_user_dialog.after(1000, lambda: user_label.configure(text="Nhập tên người dùng mới:"))

def delete_user(frame):
    if (len(os.listdir("saves")) <= 1):
        error_dialog = ctk.CTkToplevel(fg_color=colors["background"])
        error_dialog.title("Lỗi")
        error_dialog.geometry("300x70")
        error_dialog.resizable(False, False)
        error_dialog.grab_set()
        error_dialog.transient(frame)
        ctk.CTkLabel(error_dialog, text="Cần nhiều hơn 1 người dùng để xóa", font=("Arial", 16), text_color=colors["text_color"]).pack(pady=10)
        return
    
    delete_dialog = ctk.CTkToplevel(fg_color=colors["background"])
    delete_dialog.title("Xóa người dùng")
    delete_dialog.geometry("300x400")
    delete_dialog.resizable(False, False)
    delete_dialog.grab_set()
    delete_dialog.transient(frame)

    user_label = ctk.CTkLabel(delete_dialog, text="Chọn người dùng cần xóa:", font=("Helvetica", 16), text_color=colors["text_color"])
    user_label.pack(pady=10)

    users_option = [folder for folder in os.listdir("saves") if os.path.isdir(os.path.join("saves", folder)) and folder != config['current_user']]
    scroll_frame = ctk.CTkScrollableFrame(delete_dialog, width=270, height=280, fg_color=colors["background"])
    scroll_frame.pack()

    checkbox_var = {}

    for user in users_option:
        var = ctk.BooleanVar()
        checkbox = ctk.CTkCheckBox(scroll_frame, text=user, variable=var, onvalue=True, offvalue=False, command=lambda user=user: checkbox_var.update({user: var}), text_color=colors["text_color"])
        checkbox.pack(anchor="w", pady=5)
        checkbox_var[user] = var
    
    confirm_button = ctk.CTkButton(delete_dialog, text="Xác nhận", command=lambda: confirm_delete())
    confirm_button.pack(pady=10)

    def confirm_delete():
        selected_users = [user for user, var in checkbox_var.items() if var.get()]
        if selected_users:
            for user in selected_users:
                user_path = os.path.join("saves", user)
                if os.path.exists(user_path):
                    shutil.rmtree(user_path)
            delete_dialog.destroy()
            restart_app(frame)              

def restart_app(frame):
    import sys
    import subprocess

    try:
        executable_path = sys.executable
        script_path = 'app.py'
        if getattr(sys, 'frozen', False): 
            subprocess.Popen([executable_path]) 
        else:  
            subprocess.Popen([executable_path, script_path])

    except Exception as e:
        print(f"Error restarting app: {e}")
    finally:
        sys.exit(0)

# ==================================================================================================================

def pomodoro_frame_function(frame):
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=2)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=0)
    frame.grid_rowconfigure(3, weight=2)

    time_remaining = ctk.StringVar(value="25:00")
    timer_label = ctk.CTkLabel(frame, textvariable=time_remaining, font=("Helvetica", 120), text_color=colors["text_color"])
    timer_label.grid(row=1, column=0)

    buttons_frame = ctk.CTkFrame(frame, fg_color="transparent")
    buttons_frame.grid(row=2, column=0, pady=(0, 20))

    start_button = ctk.CTkButton(buttons_frame, text="Start", width=150, font=("Arial", 20), text_color=colors["text_color"])
    start_button.grid(row=0, column=0, padx=10)

    reset_button = ctk.CTkButton(buttons_frame, text="Reset", width=150, font=("Arial", 20), text_color=colors["text_color"])
    reset_button.grid(row=0, column=1, padx=10)

    switch_button = ctk.CTkButton(buttons_frame, text="Switch Mode", width=150, font=("Arial", 20), text_color=colors["text_color"])
    switch_button.grid(row=0, column=2, padx=10)

    timer_running = False
    is_focus_time = True
    remaining_seconds = 25 * 60
    current_overlay = None

    def create_overlay():
        main_window = frame.winfo_toplevel()
        overlay = ctk.CTkFrame(main_window, fg_color=colors["focus_mode"])
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        overlay.lift()
        
        overlay.grid_columnconfigure(0, weight=1)
        overlay.grid_rowconfigure(0, weight=2)
        overlay.grid_rowconfigure(1, weight=1)
        overlay.grid_rowconfigure(2, weight=0)
        overlay.grid_rowconfigure(3, weight=2)

        overlay_timer = ctk.CTkLabel(overlay, textvariable=time_remaining, font=("Helvetica", 120), text_color=colors["focus_mode_text"])
        overlay_timer.grid(row=1, column=0)

        overlay_buttons = ctk.CTkFrame(overlay, fg_color="transparent")
        overlay_buttons.grid(row=2, column=0, pady=(0, 20))

        overlay_pause = ctk.CTkButton(overlay_buttons, text="Pause", width=150, font=("Arial", 20), text_color=colors["text_color"], command=lambda: toggle_timer(overlay))
        overlay_pause.grid(row=0, column=0, padx=10)

        overlay_reset = ctk.CTkButton(overlay_buttons, text="Reset", width=150, font=("Arial", 20), text_color=colors["text_color"], command=lambda: reset_timer(overlay))
        overlay_reset.grid(row=0, column=1, padx=10)

        overlay_switch = ctk.CTkButton(overlay_buttons, text="Switch Mode", width=150, font=("Arial", 20), text_color=colors["text_color"], command=lambda: manual_switch(overlay))
        overlay_switch.grid(row=0, column=2, padx=10)

        return overlay


    def update_timer(overlay=None):
        nonlocal remaining_seconds, timer_running
        if timer_running and remaining_seconds > 0:
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            time_remaining.set(f"{minutes:02d}:{seconds:02d}")
            remaining_seconds -= 1
            frame.timer_id = frame.after(1000, lambda: update_timer(overlay))
        elif timer_running and remaining_seconds <= 0:
            switch_mode(overlay)

    def switch_mode(overlay=None):
        nonlocal is_focus_time, remaining_seconds
        is_focus_time = not is_focus_time
        remaining_seconds = 25 * 60 if is_focus_time else 5 * 60
        if not is_focus_time and overlay:
            overlay.destroy()
        update_timer(overlay if is_focus_time else None)

    def manual_switch(overlay=None):
        nonlocal is_focus_time, remaining_seconds, timer_running, current_overlay
        is_focus_time = not is_focus_time
        remaining_seconds = 25 * 60 if is_focus_time else 5 * 60
        time_remaining.set("25:00" if is_focus_time else "05:00")
        if overlay:
            overlay.destroy()
        if is_focus_time and timer_running:
            current_overlay = create_overlay()
        timer_running = False
        start_button.configure(text="Start")

    def toggle_timer(overlay=None):
        nonlocal timer_running, current_overlay
        timer_running = not timer_running

        if hasattr(frame, 'timer_id'):
            frame.after_cancel(frame.timer_id)

        if overlay:
            if not timer_running:
                overlay.destroy()
                current_overlay = None
            else:
                for widget in overlay.winfo_children():
                    if isinstance(widget, ctk.CTkFrame):
                        for button in widget.winfo_children():
                            if isinstance(button, ctk.CTkButton) and button.cget("text") in ["Pause", "Start"]:
                                button.configure(text="Start" if not timer_running else "Pause")
        if timer_running:
            update_timer(overlay)
    def reset_timer(overlay=None):
        nonlocal timer_running, remaining_seconds, is_focus_time, current_overlay
        timer_running = False
        is_focus_time = True
        remaining_seconds = 25 * 60
        time_remaining.set("25:00")
        if overlay:
            overlay.destroy()
            current_overlay = None
        start_button.configure(text="Start")

    def start_overlay():
        nonlocal current_overlay
        if not timer_running and is_focus_time:
            current_overlay = create_overlay()
            toggle_timer(current_overlay)
        elif not timer_running and not is_focus_time:
            toggle_timer(None)

    start_button.configure(command=start_overlay)
    reset_button.configure(command=reset_timer)
    switch_button.configure(command=lambda: manual_switch(current_overlay))

# MISC FUNCTIONS