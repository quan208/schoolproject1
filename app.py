from controller import AppController
import function

if __name__ == "__main__":
    app = AppController()
    function.show_tomorrow_subjects()
    app.view.mainloop()