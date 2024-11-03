import customtkinter as ctk
from PIL import Image, ImageTk
import time
import webbrowser
from tkinter import filedialog, messagebox
import threading
import random

# Các câu truyền cảm hứng
motivational_quotes = [
    {"quote": "The only way to do great work is to love what you do.", "source": "Steve Jobs", "link": "https://www.youtube.com/watch?v=kSjj0LlsqnI"},
    {"quote": "Success is not the key to happiness. Happiness is the key to success.", "source": "Albert Schweitzer", "link": "https://www.youtube.com/watch?v=VbtVgQn_Zkk"},
]


focus_active = False  # Biến để kiểm tra trạng thái của Focus Mode

# Cập nhật đồng hồ
def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.configure(text=current_time)
    clock_label.after(1000, update_clock)

# Chuyển các frame
def show_frame(frame):
    frame.tkraise()

# Chế độ focus mode
def activate_focus_mode():
    global focus_active
    if not focus_active:
        # Kích hoạt chế độ focus
        focus_active = True
        app.configure(fg_color="black")
        for widget in app.winfo_children():
            widget.configure(fg_color="black")

        # Đếm thời gian tập trung
        focus_time = 25 * 60  # 25 phút tập trung
        countdown(focus_time)

def deactivate_focus_mode():
    global focus_active
    focus_active = False
    app.configure(fg_color="#282828")  # Trả lại màu giao diện ban đầu
    for widget in app.winfo_children():
        widget.configure(fg_color="#282828")
    timer_label.configure(text="")  # Xóa bộ đếm

def countdown(count):
    if count > 0 and focus_active:  # Kiểm tra xem focus mode có đang bật không
        minutes, seconds = divmod(count, 60)
        current_text = f"{minutes:02}:{seconds:02}"
        if timer_label.cget("text") != current_text:  # Chỉ cập nhật nếu giá trị thay đổi
            timer_label.configure(text=current_text)
        timer_label.after(1000, countdown, count - 1)
    elif focus_active:
        messagebox.showinfo("Thông báo", "Kết thúc thời gian tập trung!")
        deactivate_focus_mode()

# Hiển thị câu truyền cảm hứng ngẫu nhiên
def show_random_quote():
    quote = random.choice(motivational_quotes)
    quote_text.set(f'"{quote["quote"]}" - {quote["source"]}')
    quote_label.bind("<Button-1>", lambda e: open_link(quote["link"]))

# Mở link của câu nói truyền cảm hứng
def open_link(url):
    webbrowser.open(url)

# Hiển thị giao diện chính
app = ctk.CTk()
app.title("My app!")
app.geometry("1280x720")
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Biểu tượng của các nút điều hướng
home_icon = ImageTk.PhotoImage(Image.open("settings.png").resize((42, 42)))
schedule_icon = ImageTk.PhotoImage(Image.open("settings.png").resize((42, 42)))

# Nav bar với màu dễ nhìn hơn
nav_bar = ctk.CTkFrame(app, width=70, corner_radius=0, fg_color="#383838")
nav_bar.grid(row=0, column=0, sticky="ns")

home_frame = ctk.CTkFrame(app)
home_frame.grid(row=0, column=1, sticky="nsew")
schedule_frame = ctk.CTkFrame(app)
schedule_frame.grid(row=0, column=1, sticky="nsew")

# Nút điều hướng
home_button = ctk.CTkButton(nav_bar, width=64, height=64, image=home_icon, text="", command=lambda: show_frame(home_frame), fg_color="transparent")
home_button.grid(row=0, column=0, pady=[5, 0 ])
schedule_button = ctk.CTkButton(nav_bar, width=64, height=64, image=schedule_icon, text="", command=lambda: show_frame(schedule_frame), fg_color="transparent")
schedule_button.grid(row=1, column=0)

# Đồng hồ
clock_label = ctk.CTkLabel(home_frame, text="", font=("Helvetica", 245), fg_color="transparent")
clock_label.grid(row=0, column=0, sticky="nsew")
home_frame.grid_rowconfigure(0, weight=1)
home_frame.grid_columnconfigure(0, weight=1)

# Thời khóa biểu
schedule_frame.columnconfigure(0, weight=1)
schedule_title = ctk.CTkLabel(schedule_frame, text="THỜI KHÓA BIỂU", font=("Helvetica", 40))
schedule_title.grid(row=0, column=0, sticky="we")

# Focus Mode và Motivation
focus_mode_button = ctk.CTkButton(nav_bar, text="Focus", command=activate_focus_mode)
focus_mode_button.grid(row=2, column=0, pady=(10, 0))

# Nút tắt Focus Mode
exit_focus_button = ctk.CTkButton(nav_bar, text="Exit Focus", command=deactivate_focus_mode)
exit_focus_button.grid(row=3, column=0, pady=(10, 0))

timer_label = ctk.CTkLabel(home_frame, text="", font=("Helvetica", 40))
timer_label.grid(row=1, column=0)

# Motivation Quote
quote_text = ctk.StringVar()
quote_text.set("Click here for motivation")
quote_label = ctk.CTkLabel(home_frame, textvariable=quote_text, font=("Helvetica", 20), text_color="blue")
quote_label.grid(row=2, column=0)
quote_label.bind("<Button-1>", lambda e: show_random_quote())

# Khởi động các tính năng
update_clock()
show_random_quote()
show_frame(home_frame)

app.mainloop()
