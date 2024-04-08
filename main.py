import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
import sqlite3

connection = sqlite3.connect('employess.db')
cursor = connection .cursor()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Employee")
        self.setGeometry(450, 150, 750, 500)

        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()

    def mainDesign(self):
        self.employeeList = QListWidget()
        self.btnNew = QPushButton("New")
        self.btnNew.clicked.connect(self.addEmployee)
        self.btnUpdate = QPushButton("Update")
        self.btnDelete = QPushButton("Delete")


    def layouts(self):
        # Layouts #
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QFormLayout()
        self.rightMainLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightBottomLayout = QHBoxLayout()
        # Child Layout #
        self.rightMainLayout.addLayout(self.rightTopLayout)
        self.rightMainLayout.addLayout(self.rightBottomLayout)
        self.mainLayout.addLayout(self.leftLayout, 40)
        self.mainLayout.addLayout(self.rightMainLayout, 60)
        # Adding widgets #
        self.rightTopLayout.addWidget(self.employeeList)
        self.rightBottomLayout.addWidget(self.btnNew)
        self.rightBottomLayout.addWidget(self.btnUpdate)
        self.rightBottomLayout.addWidget(self.btnDelete)

        # Setting layout #
        self.setLayout(self.mainLayout)

    def addEmployee(self):
        self.newEmployee = AddEmployee()
        self.close()


class AddEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Employee")
        self.setGeometry(450, 150, 350, 600)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()

    def mainDesign(self):
        self.title = QLabel("Add Person")
        self.title.setStyleSheet('font-size: 24pt; font-family: Arial Bold; background-color:red;')
        self.imgAdd = QLabel()
        self.imgAdd.setPixmap(QPixmap("icons/person.png"))


    def layouts(self):
        # Main Layout #
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        # child layout #
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        # adding Widgets
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)
        self.topLayout.addWidget(self.imgAdd)
        self.topLayout.addStretch()
        # setting main layout #
        self.setLayout(self.mainLayout)




def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()