from tab_widget import *
from db_creator import db
from sorting_feature import sorter

class ToDoWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("To Do List")
        self.setMinimumHeight(300)

        self.central_widget = TaskProjectTabs()
        self.setCentralWidget(self.central_widget)

        self.central_widget.task_exit_button.clicked.connect(self.close)


if __name__ == "__main__":
    creator = db
    data_sorter = sorter
    to_do = QApplication([])
    main_window = ToDoWindow()
    main_window.show()
    main_window.raise_()
    to_do.exec_()
