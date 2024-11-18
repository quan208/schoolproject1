import customtkinter as ctk
from PIL import Image, ImageTk
from themes import get_theme
from function import home_frame_function, schedule_frame_function, note_frame_function, setting_frame_function
import misc.configuration as config

colors = get_theme(config.theme_using)

class MainView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("TimeMate v1.0")
        self.resizable(False, False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self._set_appearance_mode(colors["app_theme"])
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
        self.lift()
        self.focus_force()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1366) // 2
        y = (screen_height - 768) // 2
        self.geometry(f"1366x768+{x}+{y}")

        self.create_frames()
        self.create_navigation_bar()
        home_frame_function(self.home_frame)
        schedule_frame_function(self.schedule_frame)
        setting_frame_function(self.setting_frame)
        self.show_frame(self.home_frame)

    def create_navigation_bar(self):
        nav_bar = ctk.CTkFrame(self, width=70, corner_radius=0, fg_color=colors["nav_bar"])
        nav_bar.grid(row=0, column=0, sticky="ns")
        nav_bar.grid_rowconfigure(3, weight=1)

        home_icon = ctk.CTkImage(Image.open("images/home.png").resize((42, 42)), size=(42, 42))
        schedule_icon = ctk.CTkImage(Image.open("images/calendar.png").resize((42, 42)), size=(42, 42))
        note_icon = ctk.CTkImage(Image.open("images/note.png").resize((42, 42)), size=(42, 42))
        setting_icon = ctk.CTkImage(Image.open("images/setting.png").resize((42, 42)), size=(42, 42))

        ctk.CTkButton(nav_bar, width=64, height=64, image=home_icon, text="", command=lambda: self.show_frame(self.home_frame), fg_color="transparent").grid(row=0, column=0)
        ctk.CTkButton(nav_bar, width=64, height=64, image=schedule_icon, text="", command=lambda: self.show_frame(self.schedule_frame), fg_color="transparent").grid(row=1, column=0)
        ctk.CTkButton(nav_bar, width=64, height=64, image=note_icon, text="", command=lambda: self.show_frame(self.note_frame), fg_color="transparent").grid(row=2, column=0)
        ctk.CTkButton(nav_bar, width=64, height=64, image=setting_icon, text="", command=lambda: self.show_frame(self.setting_frame), fg_color="transparent").grid(row=4, column=0)

    def create_frames(self):
        self.home_frame = ctk.CTkFrame(self, fg_color=colors["background"], corner_radius=0)
        self.home_frame.grid(row=0, column=1, sticky="nsew")
        self.schedule_frame = ctk.CTkFrame(self, fg_color=colors["background"], corner_radius=0)
        self.schedule_frame.grid(row=0, column=1, sticky="nsew")
        self.note_frame = ctk.CTkFrame(self, fg_color=colors["background"], corner_radius=0)
        self.note_frame.grid(row=0, column=1, sticky="nsew")
        self.setting_frame = ctk.CTkFrame(self, fg_color=colors["background"], corner_radius=0)
        self.setting_frame.grid(row=0, column=1, sticky="nsew")  

    def show_frame(self, frame):
        frame.tkraise()