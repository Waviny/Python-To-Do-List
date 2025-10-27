import customtkinter as ctk
from core.tasks_manager import load_tasks, remove_task
from tkinter import messagebox

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, parent, on_change_page=None):
        super().__init__(parent, fg_color="#0D1117", corner_radius=0)
        self.on_change_page = on_change_page
        self.active_button = None

        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=(30, 40), padx=20)
        
        ctk.CTkLabel(logo_frame, text="◆", font=ctk.CTkFont(size=40, weight="bold"), 
                     text_color="#58A6FF").pack()
        ctk.CTkLabel(logo_frame, text="TASK FLOW", font=ctk.CTkFont(size=20, weight="bold"), 
                     text_color="#C9D1D9").pack()
        ctk.CTkLabel(logo_frame, text="Pro Manager", font=ctk.CTkFont(size=11), 
                     text_color="#8B949E").pack()

        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=15, pady=20)

        self.home_btn = self.create_nav_button("🏠", "Dashboard", "home")
        self.tasks_btn = self.create_nav_button("✓", "Tasks", "tasks")
        self.settings_btn = self.create_nav_button("⚙", "Settings", "settings")

        self.footer = ctk.CTkFrame(self, fg_color="#161B22", corner_radius=10)
        self.footer.pack(side="bottom", fill="x", padx=15, pady=20)
        
        ctk.CTkLabel(self.footer, text="Version 2.0", font=ctk.CTkFont(size=10), 
                     text_color="#6E7681").pack(pady=5)

    def create_nav_button(self, icon, text, page):
        btn_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=8)
        
        btn = ctk.CTkButton(
            btn_frame, text=f"{icon}  {text}", 
            fg_color="transparent",
            hover_color="#21262D",
            text_color="#8B949E",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            anchor="w",
            corner_radius=8,
            border_width=0,
            command=lambda: self.switch_page(page, btn)
        )
        btn.pack(fill="x", padx=5)
        
        if page == "home":
            self.switch_page(page, btn)
        
        return btn

    def switch_page(self, page, button):
        if self.active_button:
            self.active_button.configure(fg_color="transparent", text_color="#8B949E")
        
        button.configure(fg_color="#1F6FEB", text_color="#FFFFFF")
        self.active_button = button
        
        if self.on_change_page:
            self.on_change_page(page)


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, tasks_data):
        super().__init__(parent, fg_color="#0D1117")
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        ctk.CTkLabel(header, text="Dashboard Overview", 
                     font=ctk.CTkFont(size=32, weight="bold"),
                     text_color="#C9D1D9").pack(anchor="w")
        ctk.CTkLabel(header, text="Monitor your productivity and task progress", 
                     font=ctk.CTkFont(size=14),
                     text_color="#8B949E").pack(anchor="w", pady=(5,0))

        cards_container = ctk.CTkFrame(self, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        for i in range(4):
            cards_container.columnconfigure(i, weight=1)
        
        self.total_card = self.create_stat_card(cards_container, "Total Tasks", "0", "#58A6FF", "📊", 0)
        self.pending_card = self.create_stat_card(cards_container, "Pending", "0", "#F85149", "⏳", 1)
        self.progress_card = self.create_stat_card(cards_container, "In Progress", "0", "#D29922", "🔄", 2)
        self.done_card = self.create_stat_card(cards_container, "Completed", "0", "#3FB950", "✓", 3)
        
        progress_frame = ctk.CTkFrame(cards_container, fg_color="#161B22", corner_radius=15)
        progress_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(20,0))
        
        ctk.CTkLabel(progress_frame, text="Overall Progress", 
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#C9D1D9").pack(anchor="w", padx=25, pady=(20,10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, height=20, corner_radius=10,
                                               progress_color="#3FB950", fg_color="#21262D")
        self.progress_bar.pack(fill="x", padx=25, pady=(0,15))
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(progress_frame, text="0% Complete", 
                                           font=ctk.CTkFont(size=14),
                                           text_color="#8B949E")
        self.progress_label.pack(anchor="w", padx=25, pady=(0,20))
        
        self.update_stats(tasks_data)

    def create_stat_card(self, parent, title, value, color, icon, column):
        card = ctk.CTkFrame(parent, fg_color="#161B22", corner_radius=15, 
                           border_width=2, border_color="#21262D")
        card.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=40),
                     text_color=color).pack(pady=(25,10))
        
        value_label = ctk.CTkLabel(card, text=value, 
                                   font=ctk.CTkFont(size=36, weight="bold"),
                                   text_color=color)
        value_label.pack()
        
        ctk.CTkLabel(card, text=title, 
                     font=ctk.CTkFont(size=14),
                     text_color="#8B949E").pack(pady=(5,25))
        
        return {"card": card, "value": value_label}

    def update_stats(self, tasks_data):
        total = len(tasks_data["id"])
        pending = tasks_data["status"].count("pending")
        inprogress = tasks_data["status"].count("in progress")
        done = tasks_data["status"].count("done")
        
        self.total_card["value"].configure(text=str(total))
        self.pending_card["value"].configure(text=str(pending))
        self.progress_card["value"].configure(text=str(inprogress))
        self.done_card["value"].configure(text=str(done))
        
        if total > 0:
            progress = done / total
            self.progress_bar.set(progress)
            self.progress_label.configure(text=f"{int(progress * 100)}% Complete")
        else:
            self.progress_bar.set(0)
            self.progress_label.configure(text="0% Complete")


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0D1117")
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        ctk.CTkLabel(header, text="Settings & Preferences", 
                     font=ctk.CTkFont(size=32, weight="bold"),
                     text_color="#C9D1D9").pack(anchor="w")
        
        settings_container = ctk.CTkFrame(self, fg_color="#161B22", corner_radius=15)
        settings_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        ctk.CTkLabel(settings_container, text="Appearance", 
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#C9D1D9").pack(anchor="w", padx=30, pady=(30,15))
        
        theme_frame = ctk.CTkFrame(settings_container, fg_color="#0D1117", corner_radius=10)
        theme_frame.pack(fill="x", padx=30, pady=(0,20))
        
        ctk.CTkLabel(theme_frame, text="Theme Mode", 
                     font=ctk.CTkFont(size=14),
                     text_color="#8B949E").pack(side="left", padx=20, pady=15)
        
        ctk.CTkSegmentedButton(theme_frame, values=["Dark", "Light", "System"],
                               fg_color="#21262D",
                               selected_color="#1F6FEB",
                               selected_hover_color="#1A5BC4").pack(side="right", padx=20, pady=15)
        
        ctk.CTkLabel(settings_container, text="About", 
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#C9D1D9").pack(anchor="w", padx=30, pady=(20,15))
        
        about_frame = ctk.CTkFrame(settings_container, fg_color="#0D1117", corner_radius=10)
        about_frame.pack(fill="x", padx=30, pady=(0,30))
        
        ctk.CTkLabel(about_frame, text="Task Flow Pro Manager v2.0\nProfessional Task Management System", 
                     font=ctk.CTkFont(size=13),
                     text_color="#8B949E",
                     justify="left").pack(anchor="w", padx=20, pady=15)


class TaskListFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0D1117")
        self.parent = parent
        self.task_frames = []
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        ctk.CTkLabel(header, text="Task Management", 
                     font=ctk.CTkFont(size=32, weight="bold"),
                     text_color="#C9D1D9").pack(side="left")
        
        filter_frame = ctk.CTkFrame(header, fg_color="transparent")
        filter_frame.pack(side="right")
        
        ctk.CTkSegmentedButton(filter_frame, values=["All", "Pending", "In Progress", "Done"],
                               fg_color="#21262D",
                               selected_color="#1F6FEB",
                               selected_hover_color="#1A5BC4").pack(side="right")

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", 
                                                   corner_radius=0)
        self.scroll_frame.pack(fill="both", expand=True, padx=40, pady=(0,20))

    def update_tasks(self, tasks_data):
        for frame in self.task_frames:
            frame.destroy()
        self.task_frames.clear()

        if not tasks_data["id"]:
            empty_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#161B22", 
                                    corner_radius=15, height=200)
            empty_frame.pack(fill="x", pady=20)
            
            ctk.CTkLabel(empty_frame, text="📋", font=ctk.CTkFont(size=60)).pack(pady=(40,10))
            ctk.CTkLabel(empty_frame, text="No tasks yet", font=ctk.CTkFont(size=20, weight="bold"),
                        text_color="#C9D1D9").pack()
            ctk.CTkLabel(empty_frame, text="Create your first task to get started", 
                        font=ctk.CTkFont(size=14), text_color="#8B949E").pack(pady=(5,40))
            
            self.task_frames.append(empty_frame)
            return

        status_config = {
            "En attente": {"color": "#F85149", "icon": "⏳", "bg": "#2D1519"},
            "En cours": {"color": "#D29922", "icon": "🔄", "bg": "#2B2416"},
            "Terminé": {"color": "#3FB950", "icon": "✓", "bg": "#162F1A"}
        }

        for i in range(len(tasks_data["id"])):
            task_id = tasks_data["id"][i]
            status = tasks_data["status"][i]
            config = status_config.get(status, {"color": "#808080", "icon": "?", "bg": "#21262D"})

            card = ctk.CTkFrame(self.scroll_frame, fg_color="#161B22", 
                                corner_radius=12, border_width=1, border_color="#21262D")
            card.pack(fill="x", pady=8)

            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=20, pady=15)

            left_frame = ctk.CTkFrame(content, fg_color="transparent")
            left_frame.pack(side="left", fill="x", expand=True)

            task_name = ctk.CTkLabel(left_frame, text=tasks_data['tasks'][i], 
                                    font=ctk.CTkFont(size=16, weight="bold"),
                                    text_color="#C9D1D9", anchor="w")
            task_name.pack(anchor="w")

            meta_text = f"🏷 {tasks_data['projects'][i]} • 📅 {tasks_data['date'][i]} • ⭐ Priority {tasks_data['priority'][i]}"
            meta = ctk.CTkLabel(left_frame, text=meta_text, 
                                font=ctk.CTkFont(size=12),
                                text_color="#8B949E", anchor="w")
            meta.pack(anchor="w", pady=(5,0))

            right_frame = ctk.CTkFrame(content, fg_color="transparent")
            right_frame.pack(side="right")

            status_badge = ctk.CTkFrame(right_frame, fg_color=config["bg"], corner_radius=8)
            status_badge.pack(side="left", padx=10)
            
            ctk.CTkLabel(status_badge, text=f"{config['icon']} {status}", 
                        text_color=config["color"],
                        font=ctk.CTkFont(size=12, weight="bold")).pack(padx=15, pady=8)

            actions = ctk.CTkFrame(right_frame, fg_color="transparent")
            actions.pack(side="left")

            edit_btn = ctk.CTkButton(actions, text="✏", width=40, height=40,
                                    fg_color="#1F6FEB", hover_color="#1A5BC4",
                                    corner_radius=8,
                                    font=ctk.CTkFont(size=16),
                                    command=lambda tid=task_id: self.parent.form.load_task(tid))
            edit_btn.pack(side="left", padx=3)

            del_btn = ctk.CTkButton(actions, text="🗑", width=40, height=40,
                                    fg_color="#21262D", hover_color="#F85149",
                                    corner_radius=8,
                                    font=ctk.CTkFont(size=16),
                                    command=lambda tid=task_id: self.delete_task(tid))
            del_btn.pack(side="left", padx=3)

            self.task_frames.append(card)


    def delete_task(self, task_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            remove_task(task_id)
            tasks_data = load_tasks()
            self.update_tasks(tasks_data)
            self.parent.pages["home"].update_stats(tasks_data)


class TaskFormFrame(ctk.CTkFrame):
    def __init__(self, parent, on_add_task=None, on_edit_task=None):
        super().__init__(parent, fg_color="#0D1117", corner_radius=0)
        self.parent = parent
        self.on_add_task = on_add_task
        self.on_edit_task = on_edit_task
        self.editing_id = None

        header_frame = ctk.CTkFrame(self, fg_color="#161B22", corner_radius=0)
        header_frame.pack(fill="x", pady=(0,20))
        
        self.header_label = ctk.CTkLabel(header_frame, text="Create New Task", 
                                        font=ctk.CTkFont(size=20, weight="bold"),
                                        text_color="#C9D1D9")
        self.header_label.pack(pady=20)

        form_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        form_container.pack(fill="both", expand=True, padx=20)

        ctk.CTkLabel(form_container, text="Task Name", 
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#8B949E", anchor="w").pack(fill="x", pady=(10,5))
        self.task_entry = ctk.CTkEntry(form_container, placeholder_text="Enter task name...",
                                      height=45, corner_radius=8,
                                      fg_color="#161B22", border_color="#21262D")
        self.task_entry.pack(fill="x", pady=(0,15))

        ctk.CTkLabel(form_container, text="Project", 
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#8B949E", anchor="w").pack(fill="x", pady=(10,5))
        self.project_entry = ctk.CTkEntry(form_container, placeholder_text="Project name...",
                                         height=45, corner_radius=8,
                                         fg_color="#161B22", border_color="#21262D")
        self.project_entry.pack(fill="x", pady=(0,15))

        ctk.CTkLabel(form_container, text="Due Date", 
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#8B949E", anchor="w").pack(fill="x", pady=(10,5))
        self.date_entry = ctk.CTkEntry(form_container, placeholder_text="YYYY-MM-DD",
                                      height=45, corner_radius=8,
                                      fg_color="#161B22", border_color="#21262D")
        self.date_entry.pack(fill="x", pady=(0,15))

        ctk.CTkLabel(form_container, text="Priority Level", 
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#8B949E", anchor="w").pack(fill="x", pady=(10,5))
        self.priority_menu = ctk.CTkOptionMenu(form_container, 
                                              values=[str(i) for i in range(1,11)],
                                              height=45, corner_radius=8,
                                              fg_color="#161B22", 
                                              button_color="#1F6FEB",
                                              button_hover_color="#1A5BC4")
        self.priority_menu.pack(fill="x", pady=(0,15))

        ctk.CTkLabel(form_container, text="Status", 
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#8B949E", anchor="w").pack(fill="x", pady=(10,5))
        self.status_menu = ctk.CTkOptionMenu(form_container, 
                                            values=["pending", "in progress", "done"],
                                            height=45, corner_radius=8,
                                            fg_color="#161B22",
                                            button_color="#1F6FEB",
                                            button_hover_color="#1A5BC4")
        self.status_menu.pack(fill="x", pady=(0,25))

        self.submit_btn = ctk.CTkButton(form_container, text="Create Task",
                                       height=50, corner_radius=8,
                                       font=ctk.CTkFont(size=15, weight="bold"),
                                       fg_color="#3FB950", hover_color="#33A043",
                                       command=self.submit_task)
        self.submit_btn.pack(fill="x", pady=(10,10))

        self.clear_btn = ctk.CTkButton(form_container, text="Clear Form",
                                      height=45, corner_radius=8,
                                      font=ctk.CTkFont(size=14),
                                      fg_color="#21262D", hover_color="#30363D",
                                      command=self.clear_form)
        self.clear_btn.pack(fill="x", pady=(0,20))

    def submit_task(self):
        data = {
            "task": self.task_entry.get().strip(),
            "project": self.project_entry.get().strip(),
            "date": self.date_entry.get().strip(),
            "priority": self.priority_menu.get(),
            "status": self.status_menu.get()
        }

        if not data["task"]:
            messagebox.showwarning("Missing Information", "Please enter a task name.")
            return

        if self.editing_id:
            for field in ["tasks", "projects", "date", "priority", "status"]:
                key = "task" if field == "tasks" else field[:-1] if field.endswith("s") else field
                self.on_edit_task(self.editing_id, field, data[key])
            self.editing_id = None
            self.header_label.configure(text="Create New Task")
            self.submit_btn.configure(text="Create Task", fg_color="#3FB950", hover_color="#33A043")
            messagebox.showinfo("Success", "Task updated successfully!")
        else:
            self.on_add_task(data)
            messagebox.showinfo("Success", "Task created successfully!")
        
        self.clear_form()

    def load_task(self, task_id):
        data = load_tasks()
        if task_id not in data["id"]:
            return
            
        idx = data["id"].index(task_id)
        self.editing_id = task_id

        self.task_entry.delete(0, "end")
        self.task_entry.insert(0, data["tasks"][idx])
        self.project_entry.delete(0, "end")
        self.project_entry.insert(0, data["projects"][idx])
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, data["date"][idx])
        self.priority_menu.set(str(data["priority"][idx]))
        self.status_menu.set(data["status"][idx])
        
        self.header_label.configure(text="Edit Task")
        self.submit_btn.configure(text="Update Task", fg_color="#1F6FEB", hover_color="#1A5BC4")

    def clear_form(self):
        self.task_entry.delete(0, "end")
        self.project_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.priority_menu.set("1")
        self.status_menu.set("pending")
        self.editing_id = None
        self.header_label.configure(text="Create New Task")
        self.submit_btn.configure(text="Create Task", fg_color="#3FB950", hover_color="#33A043")