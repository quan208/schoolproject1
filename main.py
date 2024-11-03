import customtkinter as ctk
from PIL import Image, ImageTk
import time
import random
from tkinter import messagebox, simpledialog
import webbrowser

motivational_quotes = [
    {"quote": "The only way to do great work is to love what you do.", "source": "Steve Jobs", "link": "https://www.youtube.com/watch?v=kSjj0LlsqnI"},
    {"quote": "Success is not the key to happiness. Happiness is the key to success.", "source": "Albert Schweitzer", "link": "https://www.youtube.com/watch?v=VbtVgQn_Zkk"},
]

focus_mode_is_running = False

def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.configure(text=current_time)
    clock_label.after(1000, update_clock)

def show_frame(frame):
    frame.tkraise()

def activate_focus_mode():
    global focus_mode_is_running
    if not focus_mode_is_running:
        focus_mode_is_running = True
        home_frame.configure(fg_color="black")
        schedule_frame.configure(fg_color="black")
        nav_bar.configure(fg_color="#171717")
    
    focus_time = 25 * 60
    pomodoro(focus_time)

def deactivate_focus_mode():
    global focus_mode_is_running
    focus_mode_is_running = False
    home_frame.configure(fg_color="#2b2b2b")
    schedule_frame.configure(fg_color="#2b2b2b")
    nav_bar.configure(fg_color="#282828")
    timer_label.configure(text="")

def pomodoro(count):
    if count > 0 and focus_mode_is_running:
        minutes, seconds = divmod(count, 60)
        current_text = f"{minutes:02}:{seconds:02}"
        if timer_label.cget("text") != current_text:
            timer_label.configure(text=current_text)
        timer_label.after(1000, pomodoro, count-1)
    elif focus_mode_is_running:
        messagebox.showinfo("Thông báo", "Kết thúc thời gian tập trung!")
        deactivate_focus_mode()

def show_random_quote():
    quote = random.choice(motivational_quotes)
    quote_text.set(f'"{quote["quote"]}" - {quote["source"]}')
    quote_label.unbind("<Button-1>")
    quote_label.bind("<Button-1>", lambda e: open_link(quote["link"]))

def open_link(url):
    webbrowser.open(url)
    show_random_quote()

def edit_subject(cell):
    subject_name = simpledialog.askstring("Nhập môn học", "Tên môn học:")
    if subject_name:
        cell.configure(text=subject_name)


def create_schedule_table(parent, start_row):
    days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]
    periods = ["1", "2", "3", "4", "5"]

    ctk.CTkLabel(
        parent, text="Buổi sáng", font=("Helvetica", 16, "bold"), fg_color="#00bcd4"
    ).grid(row=start_row, column=0, columnspan=7, sticky="nsew", pady=5)
    for col, day in enumerate(["", *days]):
        ctk.CTkLabel(parent, text=day, fg_color="#2b2b2b", width=80).grid(
            row=start_row + 1, column=col, sticky="nsew"
        )

    for row, period in enumerate(periods, start=start_row + 2):
        ctk.CTkLabel(parent, text=period, fg_color="#2b2b2b", width=30).grid(
            row=row, column=0, sticky="nsew"
        )
        for col in range(1, 7):
            cell = ctk.CTkLabel(
                parent, text="", fg_color="#2b2b2b", width=100, height=40
            )
            cell.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            cell.bind("<Button-1>", lambda e, c=cell: edit_subject(c))

    ctk.CTkLabel(
        parent, text="Buổi chiều", font=("Helvetica", 16, "bold"), fg_color="#00bcd4"
    ).grid(row=start_row + 7, column=0, columnspan=7, sticky="nsew", pady=5)
    for col, day in enumerate(["", *days]):
        ctk.CTkLabel(parent, text=day, fg_color="#2b2b2b", width=80).grid(
            row=start_row + 8, column=col, sticky="nsew"
        )

    for row, period in enumerate(periods, start=start_row + 9):
        ctk.CTkLabel(parent, text=period, fg_color="#2b2b2b", width=30).grid(
            row=row, column=0, sticky="nsew"
        )
        for col in range(1, 7):
            cell = ctk.CTkLabel(
                parent, text="", fg_color="#2b2b2b", width=100, height=40
            )
            cell.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            cell.bind("<Button-1>", lambda e, c=cell: edit_subject(c))


app = ctk.CTk()
app.title("My app!")
app.geometry("1280x720")
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# biểu tượng của các nút điều hướng
home_icon = ImageTk.PhotoImage(Image.open("home.png").resize((42, 42)))
schedule_icon = ImageTk.PhotoImage(Image.open("file.png").resize((42, 42)))

nav_bar = ctk.CTkFrame(app, width=70, corner_radius=0, fg_color="#282828")
nav_bar.grid(row=0, column=0, sticky="ns")
home_frame = ctk.CTkFrame(app)
home_frame.grid(row=0, column=1, sticky="nsew")
schedule_frame = ctk.CTkFrame(app)
schedule_frame.grid(row=0, column=1, sticky="nsew")

# các nút điều hướng
home_button = ctk.CTkButton(nav_bar, width=64, height=64, image=home_icon, text="", command=lambda: show_frame(home_frame), fg_color="transparent")
home_button.grid(row=0, column=0, pady=[5, 0 ])
schedule_button = ctk.CTkButton(nav_bar, width=64, height=64, image=schedule_icon, text="", command=lambda: show_frame(schedule_frame), fg_color="transparent")
schedule_button.grid(row=1, column=0)

clock_label = ctk.CTkLabel(home_frame, text="", font=("Helvetica", 245), fg_color="transparent")
clock_label.grid(row=0, column=0, sticky="nsew")
home_frame.grid_rowconfigure(0, weight=1)
home_frame.grid_columnconfigure(0, weight=1)

schedule_frame.columnconfigure(0, weight=1)
schedule_title = ctk.CTkLabel(schedule_frame, text="THỜI KHÓA BIỂU", font=("Helvetica", 40))
schedule_title.grid(row=0, column=0, sticky="we")

# chế độ tập trung
focus_mode_button = ctk.CTkButton(nav_bar, width=64, text="Focus", command=activate_focus_mode)
focus_mode_button.grid(row=2, column=0, pady=[10, 0])
exit_focus_button = ctk.CTkButton(nav_bar, width=64, text="Stop", command=deactivate_focus_mode)
exit_focus_button.grid(row=3, column=0, pady=[5, 0])

timer_label = ctk.CTkLabel(home_frame, text="", font=("Helvetica", 40))
timer_label.grid(row=1, column=0)

quote_text = ctk.StringVar()
quote_text.set("Nhấn vào đây để xem nguồn")
quote_label = ctk.CTkLabel(home_frame, textvariable=quote_text, font=("Helvetica", 20), text_color="blue")
quote_label.grid(row=2, column=0)
quote_label.bind("<Button-1>", lambda e: show_random_quote())

timetable_frame = ctk.CTkFrame(schedule_frame, fg_color="#2b2b2b")
timetable_frame.grid(row=1, column=0, padx=20, pady=20)
create_schedule_table(timetable_frame, start_row=1)

home_frame.grid_rowconfigure(0, weight=1)
home_frame.grid_columnconfigure(0, weight=1)

schedule_frame.grid_rowconfigure(0, weight=0)
schedule_frame.grid_rowconfigure(1, weight=1)
schedule_frame.grid_columnconfigure(0, weight=1)

update_clock()
show_random_quote()
show_frame(home_frame)

app.mainloop()
