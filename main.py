import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
import sqlite3
from PIL import Image

connection = sqlite3.connect('employess.db')
cursor = connection .cursor()
defaultImg = "person.png"

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Employee")
        self.setGeometry(450, 150, 750, 500)

        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()
        self.getEmployees()
        self.displayFirstRecord()

    def mainDesign(self):
        self.employeeList = QListWidget()
        self.employeeList.itemClicked.connect(self.singleClick)
        self.btnNew = QPushButton("New")
        self.btnNew.clicked.connect(self.addEmployee)
        self.btnDelete = QPushButton("Delete")
        self.btnDelete.clicked.connect(self.deleteEmployee)


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
        self.rightBottomLayout.addWidget(self.btnDelete)

        # Setting layout #
        self.setLayout(self.mainLayout)

    def addEmployee(self):
        self.newEmployee = AddEmployee()
        self.close()

    def getEmployees(self):
        query = "SELECT id,name,surname FROM employees"
        employees = cursor.execute(query).fetchall()
        for employee in employees:
            self.employeeList.addItem(str(employee[0]) + "-" + employee[1] + " " + employee[2] )

    def displayFirstRecord(self):
        query = "SELECT * FROM employees ORDER BY ROWID ASC LIMIT 1"
        employee = cursor.execute(query).fetchone()
        img = QLabel()
        img.setPixmap(QPixmap("images/" + employee[5]))
        name = QLabel(employee[1])
        surname = QLabel(employee[2])
        phone = QLabel(employee[3])
        email = QLabel(employee[4])
        address = QLabel(employee[6])
        self.leftLayout.setVerticalSpacing(20) #20px between rows
        self.leftLayout.addRow("", img)
        self.leftLayout.addRow("Name: ", name)
        self.leftLayout.addRow("Surname :", surname)
        self.leftLayout.addRow("Phone :", phone)
        self.leftLayout.addRow("Email :", email)
        self.leftLayout.addRow("Address:", address)

    def singleClick(self):
        for i in reversed(range(self.leftLayout.count())):
            widget = self.leftLayout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        employee = self.employeeList.currentItem().text()
        id = employee.split("-")[0]
        query = ("SELECT * FROM employees WHERE id=?")
        person = cursor.execute(query, (id,)).fetchone()  # single item tuple=(1,)
        img = QLabel()
        img.setPixmap(QPixmap("images/" + person[5]))
        name = QLabel(person[1])
        surname = QLabel(person[2])
        phone = QLabel(person[3])
        email = QLabel(person[4])
        address = QLabel(person[6])
        self.leftLayout.setVerticalSpacing(20)
        self.leftLayout.addRow("", img)
        self.leftLayout.addRow("Name: ", name)
        self.leftLayout.addRow("Surname :", surname)
        self.leftLayout.addRow("Phone :", phone)
        self.leftLayout.addRow("Email :", email)
        self.leftLayout.addRow("Address:", address)

    def deleteEmployee(self):
        if self.employeeList.selectedItems():
            person = self.employeeList.currentItem().text()
            id = person.split("-")[0]
            mbox = QMessageBox.question(self, "Warning", "Are you sure to delete this person?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    query = "DELETE FROM employees WHERE id=?"
                    cursor.execute(query, (id,))
                    connection.commit()
                    QMessageBox.information(self, "Info!!!", "Person has been deleted")
                    self.close()
                    self.main = Main()

                except:
                    QMessageBox.information(self, "Warning!!!", "Person has not been deleted")


        else:
            QMessageBox.information(self, "Warning!!!", "Please select a person to delete")

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

    def closeEvent(self, event):
        self.main = Main()


    def mainDesign(self):
        # top widget #
        self.setStyleSheet("font-size: 14pt; font-family: Times")
        self.title = QLabel("Add Person")
        self.title.setStyleSheet('font-size: 24pt; font-family: Arial Bold;')
        self.imgAdd = QLabel()
        self.imgAdd.setPixmap(QPixmap("icons/person.png"))
        # bottom widget #
        self.nameLbl = QLabel("Name :")
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Employee Name")
        self.surnameLbl = QLabel("Surname :")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setPlaceholderText("Enter Employee surname")
        self.phoneLbl = QLabel("Phone :")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter Employee Phone Number")
        self.emailLbl = QLabel("Email :")
        self.emailEntry = QLineEdit()
        self.emailEntry.setPlaceholderText("Enter Employee Email")
        self.imgLbl = QLabel("Picture: ")
        self.imgButton = QPushButton("Browse")
        self.imgButton.setStyleSheet("background-color: orange; font-size: 10pt")
        self.imgButton.clicked.connect(self.uploadImage)
        self.addressLbl = QLabel("Address: ")
        self.addressEditor = QTextEdit()
        self.addButton = QPushButton("Update")
        self.addButton.setStyleSheet("background-color: orange; font-size: 10pt")
        self.addButton.clicked.connect(self.addEmployee)

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
        self.topLayout.setContentsMargins(110, 20, 10, 30) # left, top, right, bottom
        self.bottomLayout.addRow(self.nameLbl, self.nameEntry)
        self.bottomLayout.addRow(self.surnameLbl, self.surnameEntry)
        self.bottomLayout.addRow(self.phoneLbl, self.phoneEntry)
        self.bottomLayout.addRow(self.emailLbl, self.emailEntry)
        self.bottomLayout.addRow(self.imgLbl, self.imgButton)
        self.bottomLayout.addRow(self.addressLbl, self.addressEditor)
        self.bottomLayout.addRow("", self.addButton)
        # setting main layout #
        self.setLayout(self.mainLayout)

    def uploadImage(self):
        global defaultImg
        size = (128, 128)
        self.fileName, ok = QFileDialog.getOpenFileName(self,'Upload Image', '','Image Files (*.jpg *.png)')

        if ok:
            defaultImg = os.path.basename(self.fileName)
            img = Image.open(self.fileName)
            img = img.resize(size)
            img.save("images/{}".format(defaultImg))

    def addEmployee(self):
        global defaultImg
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        img = defaultImg
        address = self.addressEditor.toPlainText()

        if (name and surname and phone != ""):
            try:
                query = "INSERT INTO employees (name,surname,phone,email,img,address) VALUES(?,?,?,?,?,?)"
                cursor.execute(query, (name, surname, phone, email, img, address))
                connection.commit()
                QMessageBox.information(self, "Success", "Person has been added")
                self.close()
                self.main = Main()

            except:
                QMessageBox.information(self, "Warning", "Person has not been added")

        else:
            QMessageBox.information(self, "Warning", "Fields can not be empty")

def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()