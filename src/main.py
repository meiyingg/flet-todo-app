import flet as ft
from datetime import datetime
import json

class Task(ft.Container):
    def __init__(self, task_name, priority, category, task_status_change, task_delete, completed=False, due_date=None, notes=""):
        super().__init__()
        self.completed = completed
        self.task_name = task_name
        self.priority = priority  # "high", "medium", "low"
        self.category = category
        self.due_date = due_date
        self.notes = notes
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Priority colors
        priority_colors = {
            "high": ft.Colors.RED_400,
            "medium": ft.Colors.ORANGE_400,
            "low": ft.Colors.GREEN_400
        }
        
        self.display_task = ft.Checkbox(
            value=self.completed, 
            label=self.task_name, 
            on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1, value=self.task_name)
        
        # Priority indicator
        self.priority_chip = ft.Chip(
            label=ft.Text(self.priority.upper(), size=10),
            bgcolor=priority_colors.get(self.priority, ft.Colors.GREY_400),
            height=25,
        )
        
        # Category chip
        self.category_chip = ft.Chip(
            label=ft.Text(self.category, size=10),
            bgcolor=ft.Colors.BLUE_200,
            height=25,
        )
        
        # Display view
        self.display_view = ft.Column(
            spacing=5,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row([
                            self.display_task,
                            self.priority_chip,
                            self.category_chip,
                        ], spacing=10),
                        ft.Row(
                            spacing=0,
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.INFO_OUTLINE,
                                    icon_size=18,
                                    tooltip="View Details",
                                    on_click=self.show_details,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CREATE_OUTLINED,
                                    icon_size=18,
                                    tooltip="Edit",
                                    on_click=self.edit_clicked,
                                ),
                                ft.IconButton(
                                    ft.Icons.DELETE_OUTLINE,
                                    icon_size=18,
                                    tooltip="Delete",
                                    on_click=self.delete_clicked,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
        
        # Edit view
        self.priority_dropdown = ft.Dropdown(
            width=120,
            value=self.priority,
            options=[
                ft.dropdown.Option("high", "High"),
                ft.dropdown.Option("medium", "Medium"),
                ft.dropdown.Option("low", "Low"),
            ],
        )
        
        self.category_field = ft.TextField(width=120, value=self.category, label="Category")
        self.notes_field = ft.TextField(multiline=True, min_lines=2, max_lines=4, value=self.notes, label="Notes")
        
        self.edit_view = ft.Column(
            visible=False,
            spacing=10,
            controls=[
                self.edit_name,
                ft.Row([
                    self.priority_dropdown,
                    self.category_field,
                ]),
                self.notes_field,
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                        icon_color=ft.Colors.GREEN,
                        tooltip="Save",
                        on_click=self.save_clicked,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CANCEL_OUTLINED,
                        icon_color=ft.Colors.RED,
                        tooltip="Cancel",
                        on_click=self.cancel_edit,
                    ),
                ]),
            ],
        )
        
        self.content = ft.Column(
            controls=[self.display_view, self.edit_view]
        )
        self.border_radius = 10
        self.padding = 12
        self.bgcolor = ft.Colors.BLUE_50 if not self.completed else ft.Colors.GREY_200

    def show_details(self, e):
        details = f"""
📋 Task: {self.task_name}
🎯 Priority: {self.priority.upper()}
📁 Category: {self.category}
📅 Created: {self.created_date}
📝 Notes: {self.notes if self.notes else "No notes"}
        """
        dlg = ft.AlertDialog(
            title=ft.Text("Task Details"),
            content=ft.Text(details),
            actions=[ft.TextButton("Close", on_click=lambda e: self.close_dialog(dlg))],
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()
    
    def close_dialog(self, dialog):
        dialog.open = False
        self.page.update()

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def cancel_edit(self, e):
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def save_clicked(self, e):
        self.task_name = self.edit_name.value
        self.priority = self.priority_dropdown.value
        self.category = self.category_field.value
        self.notes = self.notes_field.value
        
        self.display_task.label = self.task_name
        
        # Update chips
        priority_colors = {
            "high": ft.Colors.RED_400,
            "medium": ft.Colors.ORANGE_400,
            "low": ft.Colors.GREEN_400
        }
        self.priority_chip.label = ft.Text(self.priority.upper(), size=10)
        self.priority_chip.bgcolor = priority_colors.get(self.priority, ft.Colors.GREY_400)
        self.category_chip.label = ft.Text(self.category, size=10)
        
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()
        self.task_status_change(self)

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.bgcolor = ft.Colors.GREY_200 if self.completed else ft.Colors.BLUE_50
        self.update()
        self.task_status_change(self)

    def delete_clicked(self, e):
        self.task_delete(self)
    
    def to_dict(self):
        return {
            "name": self.task_name,
            "completed": self.completed,
            "priority": self.priority,
            "category": self.category,
            "notes": self.notes,
            "created_date": self.created_date,
        }


class TodoApp(ft.Column):
    def __init__(self):
        super().__init__()
        
        # Search field
        self.search_field = ft.TextField(
            hint_text="Search tasks...",
            prefix_icon=ft.Icons.SEARCH,
            on_change=self.search_tasks,
            width=300,
        )
        
        # Input fields
        self.new_task = ft.TextField(
            hint_text="What needs to be done?",
            on_submit=self.add_clicked,
            expand=True
        )
        
        self.priority_selector = ft.Dropdown(
            width=120,
            value="medium",
            options=[
                ft.dropdown.Option("high", "High"),
                ft.dropdown.Option("medium", "Medium"),
                ft.dropdown.Option("low", "Low"),
            ],
        )
        
        self.category_input = ft.TextField(
            hint_text="Category",
            width=120,
        )
        
        self.tasks = ft.Column(spacing=10)

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text="All", icon=ft.Icons.LIST),
                ft.Tab(text="Active", icon=ft.Icons.RADIO_BUTTON_UNCHECKED),
                ft.Tab(text="Completed", icon=ft.Icons.CHECK_CIRCLE_OUTLINE),
                ft.Tab(text="High Priority", icon=ft.Icons.PRIORITY_HIGH),
            ],
        )

        # Statistics
        self.stats_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.Column([
                    ft.Text("Total", size=12, color=ft.Colors.GREY_600),
                    ft.Text("0", size=24, weight=ft.FontWeight.BOLD),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([
                    ft.Text("Active", size=12, color=ft.Colors.BLUE_600),
                    ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([
                    ft.Text("Completed", size=12, color=ft.Colors.GREEN_600),
                    ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ],
        )

        self.width = 700
        self.controls = [
            ft.Container(
                content=ft.Text(
                    "✨ Advanced Todo Manager",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                padding=20,
            ),
            ft.Container(
                content=self.stats_row,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=10,
                padding=15,
            ),
            ft.Container(content=self.search_field, padding=ft.padding.only(top=10)),
            ft.Row([
                self.new_task,
                self.priority_selector,
                self.category_input,
                ft.FloatingActionButton(
                    icon=ft.Icons.ADD,
                    on_click=self.add_clicked,
                    bgcolor=ft.Colors.BLUE_600,
                ),
            ]),
            ft.Container(content=self.filter, padding=ft.padding.only(top=20, bottom=10)),
            ft.Container(
                content=self.tasks,
                height=400,
                padding=10,
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.OutlinedButton(
                        "Clear Completed",
                        icon=ft.Icons.DELETE_SWEEP,
                        on_click=self.clear_clicked
                    ),
                    ft.OutlinedButton(
                        "Export Data",
                        icon=ft.Icons.DOWNLOAD,
                        on_click=self.export_tasks
                    ),
                ],
            ),
        ]

    def load_tasks(self):
        try:
            # 检查client_storage是否可用
            if not hasattr(self.page, 'client_storage') or self.page.client_storage is None:
                print("⚠️ Client storage not available, creating sample tasks")
                self.create_sample_tasks()
                return
            
            stored_tasks = self.page.client_storage.get("advanced_tasks")
            if stored_tasks:
                for t_data in stored_tasks:
                    task = Task(
                        t_data["name"],
                        t_data.get("priority", "medium"),
                        t_data.get("category", "General"),
                        self.task_status_change,
                        self.task_delete,
                        t_data["completed"],
                        notes=t_data.get("notes", "")
                    )
                    self.tasks.controls.append(task)
                self.update()
                self.update_statistics()
            else:
                # 首次使用，创建示例任务
                print("📝 First time use, creating sample tasks")
                self.create_sample_tasks()
        except Exception as e:
            print(f"⚠️ Error loading tasks: {e}")
            self.create_sample_tasks()

    def create_sample_tasks(self):
        """创建示例任务"""
        sample_tasks = [
            {"name": "📱 Welcome to Flet Todo!", "priority": "high", "category": "Welcome", "completed": False, "notes": "Tap to edit or check to complete"},
            {"name": "📝 Add your first task", "priority": "medium", "category": "Getting Started", "completed": False, "notes": "Use the input field above"},
            {"name": "🎯 Set priorities and categories", "priority": "low", "category": "Tutorial", "completed": False, "notes": "Organize your tasks better"},
        ]
        
        for t_data in sample_tasks:
            task = Task(
                t_data["name"],
                t_data["priority"],
                t_data["category"],
                self.task_status_change,
                self.task_delete,
                t_data["completed"],
                notes=t_data.get("notes", "")
            )
            self.tasks.controls.append(task)
        
        self.update()
        self.update_statistics()
    
    def save_tasks(self):
        try:
            # 检查client_storage是否可用
            if not hasattr(self.page, 'client_storage') or self.page.client_storage is None:
                print("⚠️ Client storage not available, tasks will not persist")
                return
            
            tasks_data = [t.to_dict() for t in self.tasks.controls]
            self.page.client_storage.set("advanced_tasks", tasks_data)
        except Exception as e:
            print(f"⚠️ Error saving tasks: {e}")

    def add_clicked(self, e):
        if self.new_task.value:
            task = Task(
                self.new_task.value,
                self.priority_selector.value,
                self.category_input.value or "General",
                self.task_status_change,
                self.task_delete
            )
            self.tasks.controls.insert(0, task)
            self.new_task.value = ""
            self.category_input.value = ""
            self.priority_selector.value = "medium"
            self.new_task.focus()
            self.update()
            self.save_tasks()
            self.update_statistics()
            self.show_snackbar("✅ Task added successfully!")

    def task_status_change(self, task):
        self.update()
        self.save_tasks()
        self.update_statistics()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()
        self.save_tasks()
        self.update_statistics()
        self.show_snackbar("🗑️ Task deleted!")

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        count = 0
        for task in self.tasks.controls[:]:
            if task.completed:
                self.tasks.controls.remove(task)
                count += 1
        self.update()
        self.save_tasks()
        self.update_statistics()
        self.show_snackbar(f"🧹 Cleared {count} completed task(s)!")

    def search_tasks(self, e):
        search_term = self.search_field.value.lower()
        for task in self.tasks.controls:
            if search_term in task.task_name.lower() or search_term in task.category.lower():
                task.visible = True
            else:
                task.visible = False
        self.update()

    def export_tasks(self, e):
        tasks_data = [t.to_dict() for t in self.tasks.controls]
        json_data = json.dumps(tasks_data, indent=2)
        
        dlg = ft.AlertDialog(
            title=ft.Text("Export Tasks (JSON)"),
            content=ft.Container(
                content=ft.Text(json_data, selectable=True),
                width=500,
                height=300,
            ),
            actions=[ft.TextButton("Close", on_click=lambda e: self.close_dialog(dlg))],
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()
    
    def close_dialog(self, dialog):
        dialog.open = False
        self.page.update()

    def show_snackbar(self, message):
        snack = ft.SnackBar(content=ft.Text(message), duration=2000)
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def update_statistics(self):
        total = len(self.tasks.controls)
        completed = sum(1 for t in self.tasks.controls if t.completed)
        active = total - completed
        
        self.stats_row.controls[0].controls[1].value = str(total)
        self.stats_row.controls[1].controls[1].value = str(active)
        self.stats_row.controls[2].controls[1].value = str(completed)
        self.update()

    def before_update(self):
        selected_tab = self.filter.tabs[self.filter.selected_index].text.lower()
        for task in self.tasks.controls:
            if selected_tab == "all":
                task.visible = True
            elif selected_tab == "active":
                task.visible = not task.completed
            elif selected_tab == "completed":
                task.visible = task.completed
            elif selected_tab == "high priority":
                task.visible = task.priority == "high"


def main(page: ft.Page):
    page.title = "Advanced Todo Manager"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        e.control.icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("Advanced Todo Manager", weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.Colors.BLUE_700,
        actions=[
            ft.IconButton(
                ft.Icons.DARK_MODE,
                on_click=toggle_theme,
                tooltip="Toggle Theme"
            )
        ]
    )

    app = TodoApp()
    page.add(app)
    app.load_tasks()


if __name__ == "__main__":
    ft.app(main)
        print("📱 Starting in Mobile-optimized mode...")
        print(f"🔗 Access from mobile: http://{local_ip}:8550")
        print("🔗 Or use: http://192.168.32.34:8550")
        print("⚠️  Keep this window open to maintain the server")
        ft.app(target=main, view=ft.AppView.FLET_APP_WEB, port=8550, host="0.0.0.0")
    else:
        # 默认桌面模式
        ft.app(target=main)
