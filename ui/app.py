import customtkinter as ctk
from ui.components import SidebarFrame, TaskListFrame, HomeFrame, SettingsFrame, TaskFormFrame
from core.tasks_manager import load_tasks, add_task, edit_task

class TaskApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Task Flow Pro Manager")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color="#0D1117")

        self.columnconfigure(0, weight=0, minsize=250)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0, minsize=350)
        self.rowconfigure(0, weight=1)

        self.tasks_data = load_tasks()

        self.current_page = None
        self.pages = {
            "home": HomeFrame(self, self.tasks_data),
            "tasks": TaskListFrame(self),
            "settings": SettingsFrame(self)
        }

        self.sidebar = SidebarFrame(self, on_change_page=self.show_page)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.show_page("home")

        self.form = TaskFormFrame(self, on_add_task=self.handle_add_task, on_edit_task=self.handle_edit_task)
        self.form.grid(row=0, column=2, sticky="nsew")

        self.pages["tasks"].update_tasks(self.tasks_data)

    def show_page(self, page_name):
        if self.current_page:
            self.current_page.grid_forget()
        self.current_page = self.pages[page_name]
        self.current_page.grid(row=0, column=1, sticky="nsew", padx=2)

    def handle_add_task(self, task_data):
        add_task(task_data)
        self.tasks_data = load_tasks()
        self.pages["tasks"].update_tasks(self.tasks_data)
        self.pages["home"].update_stats(self.tasks_data)

    def handle_edit_task(self, task_id, field, value):
        edit_task(task_id, field, value)
        self.tasks_data = load_tasks()
        self.pages["tasks"].update_tasks(self.tasks_data)
        self.pages["home"].update_stats(self.tasks_data)
