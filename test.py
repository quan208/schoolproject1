import customtkinter as ctk
from PIL import Image, ImageTk
import time
import tkinter as tk
from tkinter import simpledialog


def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.configure(text=current_time)
    clock_label.after(1000, update_clock)


def show_frame(frame):
    frame.tkraise()


def edit_subject(cell):
    subject_name = simpledialog.askstring("Nhập môn học", "Tên môn học:")
    if subject_name:
        cell.configure(text=subject_name)


def create_schedule_table(parent, start_row):
    days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]
    periods = ["1", "2", "3", "4", "5"]

    # Tạo hàng tiêu đề các ngày
    ctk.CTkLabel(
        parent, text="Buổi sáng", font=("Helvetica", 16, "bold"), fg_color="#00bcd4"
    ).grid(row=start_row, column=0, columnspan=7, sticky="nsew", pady=5)
    for col, day in enumerate(["", *days]):
        ctk.CTkLabel(parent, text=day, fg_color="#00bcd4", width=80).grid(
            row=start_row + 1, column=col, sticky="nsew"
        )

    # Tạo các ô cho các tiết học buổi sáng
    for row, period in enumerate(periods, start=start_row + 2):
        ctk.CTkLabel(parent, text=period, fg_color="#d3d3d3", width=30).grid(
            row=row, column=0, sticky="nsew"
        )
        for col in range(1, 7):
            cell = ctk.CTkLabel(
                parent, text="", fg_color="lightblue", width=100, height=40
            )
            cell.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            cell.bind("<Button-1>", lambda e, c=cell: edit_subject(c))

    # Tạo hàng tiêu đề buổi chiều
    ctk.CTkLabel(
        parent, text="Buổi chiều", font=("Helvetica", 16, "bold"), fg_color="#00bcd4"
    ).grid(row=start_row + 7, column=0, columnspan=7, sticky="nsew", pady=5)
    for col, day in enumerate(["", *days]):
        ctk.CTkLabel(parent, text=day, fg_color="#00bcd4", width=80).grid(
            row=start_row + 8, column=col, sticky="nsew"
        )

    # Tạo các ô cho các tiết học buổi chiều
    for row, period in enumerate(periods, start=start_row + 9):
        ctk.CTkLabel(parent, text=period, fg_color="#d3d3d3", width=30).grid(
            row=row, column=0, sticky="nsew"
        )
        for col in range(1, 7):
            cell = ctk.CTkLabel(
                parent, text="", fg_color="lightblue", width=100, height=40
            )
            cell.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            cell.bind("<Button-1>", lambda e, c=cell: edit_subject(c))


app = ctk.CTk()
app.title("My app!")
app.geometry("1280x720")
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Biểu tượng của các nút điều hướng
home_icon = ImageTk.PhotoImage(Image.open("settings.png").resize((42, 42)))
schedule_icon = ImageTk.PhotoImage(Image.open("settings.png").resize((42, 42)))

nav_bar = ctk.CTkFrame(app, width=70, corner_radius=5, fg_color="#cfcdcd")
nav_bar.grid(row=0, column=0, sticky="nsew")

home_frame = ctk.CTkFrame(app)
home_frame.grid(row=0, column=1, sticky="nsew")
schedule_frame = ctk.CTkFrame(app)
schedule_frame.grid(row=0, column=1, sticky="nsew")

# Các nút điều hướng
home_button = ctk.CTkButton(
    nav_bar,
    width=64,
    height=64,
    image=home_icon,
    text="",
    command=lambda: show_frame(home_frame),
    fg_color="transparent",
    hover_color="#9b9797",
)
home_button.grid(row=0, column=0, pady=[5, 0])
schedule_button = ctk.CTkButton(
    nav_bar,
    width=64,
    height=64,
    image=schedule_icon,
    text="",
    command=lambda: show_frame(schedule_frame),
    fg_color="transparent",
    hover_color="#9b9797",
)
schedule_button.grid(row=1, column=0)

clock_label = ctk.CTkLabel(
    home_frame, text="", font=("Helvetica", 245), fg_color="transparent"
)
clock_label.grid(row=0, column=0, sticky="nsew")

schedule_label = ctk.CTkLabel(
    schedule_frame, text="Thời khóa biểu", font=("Helvetica", 35), text_color="red"
)
schedule_label.grid(row=0, column=0, sticky="n", pady=(20, 0))

# Khung bảng thời khóa biểu
timetable_frame = ctk.CTkFrame(schedule_frame, fg_color="white")
timetable_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
create_schedule_table(timetable_frame, start_row=1)

home_frame.grid_rowconfigure(0, weight=1)
home_frame.grid_columnconfigure(0, weight=1)

schedule_frame.grid_rowconfigure(0, weight=0)
schedule_frame.grid_rowconfigure(1, weight=1)
schedule_frame.grid_columnconfigure(0, weight=1)

update_clock()
show_frame(home_frame)
app.mainloop()