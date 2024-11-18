import customtkinter as ctk
import os, shutil
import time
from datetime import datetime
from themes import get_theme, THEMES
import misc.configuration as config

colors = get_theme(config.theme_using)
current_schedule = ""
schedule_date = [["", "Toan", "Toan", "Toan", "Toan", "Toan"],
                  ["Toan", "", "Toan", "Toan", "Toan", "Toan"],
                  ["", "", "", "", "", ""],
                  ["Toan", "Toan", "Toan", "Toan", "Toan", "Toan"],
                  ["Toan", "Toan", "Toan", "Toan", "Toan", "Toan"],
                  ["a", "Toan", "Toan", "Toan", "Toan", "-"],
                  ["b", "Toan", "Toan", "Toan", "Toan", "Toan"],
                  ["c", "Toan", "Toan", "Toan", "Toan", "Toan"],
                  ["d", "Toan", "Toan", "Toan", "Toan", "Toan"],
                  ["e", "Toan", "Toan", "Toan", "Toan", "end"]]

def home_frame_function(frame):
    clock_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 245), fg_color="transparent", text_color=colors["text_color"])
    clock_label.grid(row=0, column=0, sticky="nsew")

    def update_time():
        current_time = time.strftime("%H:%M:%S")
        clock_label.configure(text=current_time)
        clock_label.after(1000, update_time)

    update_time()
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)



def schedule_frame_function(frame):
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    schedule_table = ctk.CTkFrame(frame, width=1000, height=600, fg_color=colors["background"])
    schedule_table.grid(row=1, column=0)


    create_schedule_table(schedule_table)

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
    # các cell môn học sáng
    today = datetime.now().weekday()
    for i in range(2, 7):
        for j in range(3, 9):
            frame_subject = ctk.CTkFrame(frame)
            if ((today + 1) % 7 == j-3 and (today + 1) % 7 != 6):
                frame_subject.configure(fg_color=colors["tomorrow_schedule"], bg_color=colors["tomorrow_schedule"])
                frame_subject.grid(row=i, column=j-1, sticky="nsew")
                ctk.CTkLabel(frame_subject, text=schedule_date[i-2][j-3], font=("Arial", 18), text_color=colors["alt_text_color"], fg_color=colors["tomorrow_schedule"]).pack(fill="both", ipady=15, ipadx=8, expand=True)
            elif (today + 2) % 7 == j-3 and (today + 2) % 7 != 6:
                frame_subject.configure(fg_color=colors["day_after_tomorrow_schedule"], bg_color=colors["day_after_tomorrow_schedule"])
                frame_subject.grid(row=i, column=j-1, sticky="nsew")
                ctk.CTkLabel(frame_subject, text=schedule_date[i-2][j-3], font=("Arial", 18), text_color=colors["alt_text_color"], fg_color=colors["day_after_tomorrow_schedule"]).pack(fill="both", ipady=15, ipadx=8, expand=True)
            else:
                ctk.CTkLabel(frame, text=schedule_date[i-2][j-3], font=("Arial", 18), text_color=colors["text_color"]).grid(row=i, column=j-1, padx=8, pady=15, sticky="nsew")


    # các cell môn học chiều
    for i in range(8, 13):
        for j in range(3, 9):
            frame_subject = ctk.CTkFrame(frame)
            if ((today + 1) % 7 == j-3 and (today + 1) % 7 != 6):
                frame_subject.configure(fg_color=colors["tomorrow_schedule"], bg_color=colors["tomorrow_schedule"])
                frame_subject.grid(row=i, column=j-1, sticky="nsew")
                ctk.CTkLabel(frame_subject, text=schedule_date[i-8][j-3], font=("Arial", 18), text_color=colors["alt_text_color"], fg_color=colors["tomorrow_schedule"]).pack(fill="both", ipady=15, ipadx=8, expand=True)
            elif (today + 2) % 7 == j-3 and (today + 2) % 7 != 6:
                frame_subject.configure(fg_color=colors["day_after_tomorrow_schedule"], bg_color=colors["day_after_tomorrow_schedule"])
                frame_subject.grid(row=i, column=j-1, sticky="nsew")
                ctk.CTkLabel(frame_subject, text=schedule_date[i-8][j-3], font=("Arial", 18), text_color=colors["alt_text_color"], fg_color=colors["day_after_tomorrow_schedule"]).pack(fill="both", ipady=15, ipadx=8, expand=True)
            else:
                ctk.CTkLabel(frame, text=schedule_date[i-8][j-3], font=("Arial", 18), text_color=colors["text_color"]).grid(row=i, column=j-1, padx=8, pady=15, sticky="nsew")
            


def note_frame_function(frame):
    pass



def setting_frame_function(frame):
    frame.grid_columnconfigure(1, weight=1)

    theme_label = ctk.CTkLabel(frame, text="Chọn giao diện:", font=("Arial", 16), text_color=colors["text_color"])
    theme_label.grid(row=0, column=0, sticky="w", padx=[10, 0])

    theme_option = list(THEMES.keys())
    theme_dropdown = ctk.CTkOptionMenu(frame, values=theme_option, command=lambda choice: apply_config("theme_using", choice, frame), dropdown_fg_color=colors["background"], dropdown_text_color=colors["text_color"], dropdown_hover_color=colors["dropdown_hover_color"])
    theme_dropdown.set(config.theme_using)
    theme_dropdown.grid(row=1, column=0, sticky="n", padx=[10, 0])

    user_label = ctk.CTkLabel(frame, text="Chọn người dùng:", font=("Arial", 16), text_color=colors["text_color"])
    user_label.grid(row=2, column=0, sticky="w", padx=[10, 0])

    user_option = [folder for folder in os.listdir("saves") if os.path.isdir(os.path.join("saves", folder))]
    user_dropdown = ctk.CTkOptionMenu(frame, values=user_option, command=lambda choice: apply_config("current_user", choice, frame), dropdown_fg_color=colors["background"], dropdown_text_color=colors["text_color"], dropdown_hover_color=colors["dropdown_hover_color"])
    user_dropdown.set(config.current_user)
    user_dropdown.grid(row=3, column=0, sticky="n", padx=[10, 0])

    add_user_button = ctk.CTkButton(frame, text="Thêm người dùng", command=lambda: add_user(frame))
    add_user_button.grid(row=4, column=0, sticky="n", padx=[10, 0], pady=[10, 0])

    delete_user_button = ctk.CTkButton(frame, text="Xóa người dùng", command=lambda: delete_user(frame))
    delete_user_button.grid(row=5, column=0, sticky="n", padx=[10, 0], pady=[10, 0])

def apply_config(config_name, choice, frame):
    if (config_name == "theme_using"):
        old_value = config.theme_using
    elif (config_name == "current_user"):
        old_value = config.current_user

    if (old_value == choice):
        return

    with open("misc/configuration.py", "r") as config_file:
        content = config_file.read()
    new_content = content.replace(f"{config_name} = '{old_value}'", f"{config_name} = '{choice}'")
    with open("misc/configuration.py", "w") as config_file:
        config_file.write(new_content)
    
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
                new_user_dialog.destroy()
                restart_app(frame)
            else:
                user_label.configure(text="Tên người dùng đã tồn tại. Vui lòng chọn tên khác.")
                new_user_dialog.after(1000, lambda: user_label.configure(text="Nhập tên người dùng mới:"))

def delete_user(frame):
    if (len(os.listdir("saves")) <= 1):
        error_dialog = ctk.CTkToplevel(fg_color=colors["background"])
        error_dialog.title("Lỗi")
        error_dialog.geometry("300x100")
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

    users_option = [folder for folder in os.listdir("saves") if os.path.isdir(os.path.join("saves", folder)) and folder != config.current_user]
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
    import sys, subprocess
    python_executable = sys.executable
    script_path = sys.argv[0]
    subprocess.Popen([python_executable, script_path])
    frame.winfo_toplevel().destroy()


