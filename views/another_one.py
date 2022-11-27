import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import uic
from PyQt5 import QtWidgets
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor


class Attendance(QMainWindow):
    def __init__(self):
        super(Attendance, self).__init__()
        loadUi("attendance.ui", self)
        self.Attendance.clicked.connect(self.attendanceUp)
        self.class_.clicked.connect(self.classesUp)
        self.student.clicked.connect(self.studentUp)
        self.permission.clicked.connect(self.permissionsUp)

    def attendanceUp(self):
        widget.setCurrentIndex(0)

    def classesUp(self):
        widget.setCurrentIndex(1)

    def studentUp(self):
        widget.setCurrentIndex(2)

    def permissionsUp(self):
        widget.setCurrentIndex(3)


class Classes(QMainWindow):
    def __init__(self):
        super(Classes, self).__init__()
        loadUi("classes.ui", self)
        self.Attendance.clicked.connect(self.attendanceUp)
        self.class_.clicked.connect(self.classesUp)
        self.student.clicked.connect(self.studentUp)
        self.permission.clicked.connect(self.permissionsUp)

    def attendanceUp(self):
        widget.setCurrentIndex(0)

    def classesUp(self):
        widget.setCurrentIndex(1)

    def studentUp(self):
        widget.setCurrentIndex(2)

    def permissionsUp(self):
        widget.setCurrentIndex(3)


class Student(QMainWindow):
    def __init__(self):
        super(Student, self).__init__()
        loadUi("students.ui", self)
        self.Attendance.clicked.connect(self.attendanceUp)
        self.class_.clicked.connect(self.classesUp)
        self.student.clicked.connect(self.studentUp)
        self.permission.clicked.connect(self.permissionsUp)

    def attendanceUp(self):
        widget.setCurrentIndex(0)

    def classesUp(self):
        widget.setCurrentIndex(1)

    def studentUp(self):
        widget.setCurrentIndex(2)

    def permissionsUp(self):
        widget.setCurrentIndex(3)


class Permissions(QMainWindow):
    def __init__(self):
        super(Permissions, self).__init__()
        loadUi("permissions.ui", self)
        self.Attendance.clicked.connect(self.attendanceUp)
        self.class_.clicked.connect(self.classesUp)
        self.student.clicked.connect(self.studentUp)
        self.permission.clicked.connect(self.permissionsUp)

    def attendanceUp(self):
        widget.setCurrentIndex(0)

    def classesUp(self):
        widget.setCurrentIndex(1)

    def studentUp(self):
        widget.setCurrentIndex(2)

    def permissionsUp(self):
        widget.setCurrentIndex(3)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
screen1 = Attendance()
screen2 = Classes()
screen3 = Student()
screen4 = Permissions()
widget.addWidget(screen1)
widget.addWidget(screen2)
widget.addWidget(screen3)
widget.addWidget(screen4)

widget.setFixedWidth(1197)
widget.setFixedHeight(888)
widget.show()

try:
    sys.exit(app.exec_())

except Exception as e:
    print(e)
    print("Exiting the app!!")
