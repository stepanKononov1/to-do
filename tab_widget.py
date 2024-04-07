from PyQt5.QtCore import Qt

from add_new_dialog import NewTaskDialog
from db_controller import DbController
from delete_dialog import DeleteTaskDialog
from edit_dialog import EditTaskDialog
from radio_button_widget import *
from table_widget import TasksTable


class TaskProjectTabs(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = DbController("to_do.db")

        self.tabs = QTabWidget()
        self.tasks_tab = QWidget()

        self.tabs.addTab(self.tasks_tab, "Tasks")
             
        self.tasks_radio_buttons = RadioButtonWidget(['Active Tasks', 'Completed Tasks', 'All Tasks'])

        self.tasks_sort_label = QLabel("Sort by:")
        self.tasks_sort_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tasks_sort_combobox = QComboBox()
        self.tasks_sort_combobox.addItems(["TaskID", "Decription", "Deadline", "Created", "Completed", "ProjectID"])

        self.tasks_top_layout = QHBoxLayout()
        self.tasks_top_layout.addWidget(self.tasks_radio_buttons)
        self.tasks_top_layout.addWidget(self.tasks_sort_label)
        self.tasks_top_layout.addWidget(self.tasks_sort_combobox)

        self.tasks_table = TasksTable()
        self.populate_tasks_table()

        self.new_task_button = QPushButton("Add New")
        self.task_complete_button = QPushButton("Mark Completed")
        self.task_complete_button.setEnabled(False)
        self.task_edit_button = QPushButton("Edit")
        self.task_edit_button.setEnabled(False)
        self.task_delete_button = QPushButton("Delete")
        self.task_delete_button.setEnabled(False)
        self.task_exit_button = QPushButton("Exit")

        self.tasks_tab_button_layout = QHBoxLayout()
        self.tasks_tab_button_layout.addWidget(self.new_task_button)
        self.tasks_tab_button_layout.addWidget(self.task_complete_button)
        self.tasks_tab_button_layout.addWidget(self.task_edit_button)
        self.tasks_tab_button_layout.addWidget(self.task_delete_button)
        self.tasks_tab_button_layout.addWidget(self.task_exit_button)

        self.tasks_tab_layout = QVBoxLayout()
        self.tasks_tab_layout.addLayout(self.tasks_top_layout)
        self.tasks_tab_layout.addWidget(self.tasks_table)
        self.tasks_tab_layout.addLayout(self.tasks_tab_button_layout)
        self.tasks_tab.setLayout(self.tasks_tab_layout)
        self.tab_widget_layout = QVBoxLayout()
        self.tab_widget_layout.addWidget(self.tabs)
        self.setLayout(self.tab_widget_layout)

        self.tabs.currentChanged.connect(self.refresh_tab)
        self.tasks_radio_buttons.radio_button_group.buttonClicked.connect(self.populate_tasks_table)
        self.tasks_sort_combobox.currentIndexChanged.connect(self.sort_tasks_table)
        self.tasks_table.clicked.connect(self.enable_task_buttons)
        self.new_task_button.clicked.connect(self.open_new_task_dialog)
        self.task_complete_button.clicked.connect(self.mark_task_completed)
        self.task_edit_button.clicked.connect(self.open_edit_task_dialog)
        self.task_delete_button.clicked.connect(self.open_delete_task_dialog)

    def populate_tasks_table(self):
        table_type = self.tasks_radio_buttons.selected_button()
        table_items = self.tasks_table.get_tasks(table_type)
        self.tasks_table.show_items(table_items)

    def refresh_tab(self):
        if self.tabs.currentIndex() == 0:
            self.populate_tasks_table()

    def sort_tasks_table(self):
        sort_by = self.tasks_sort_combobox.currentIndex()
        self.tasks_table.sortByColumn(sort_by, Qt.AscendingOrder)

    def enable_task_buttons(self):
        if not self.tasks_table.check_completed():
            self.task_complete_button.setEnabled(True)
        else:
            self.task_complete_button.setEnabled(False)
        self.task_edit_button.setEnabled(True)
        self.task_delete_button.setEnabled(True)

    def open_new_task_dialog(self):
        new_task_dialog = NewTaskDialog()
        new_task_dialog.exec_()
        self.populate_tasks_table()

    def open_edit_task_dialog(self):
        task_id = self.tasks_table.get_id()
        edit_task_dialog = EditTaskDialog(task_id)
        edit_task_dialog.exec_()
        self.populate_tasks_table()

    def mark_task_completed(self):
        task_id = self.tasks_table.get_id()
        self.controller.mark_task_completed(task_id)
        self.populate_tasks_table()

    def open_delete_task_dialog(self):
        task_id = self.tasks_table.get_id()
        delete_task_dialog = DeleteTaskDialog(task_id)
        delete_task_dialog.exec_()
        self.populate_tasks_table()
