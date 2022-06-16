from PyQt5 import QtWidgets, uic
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from threading import Thread
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
try:
    print(os.environ['DATABASE_URI'])
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('./configKey.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': f"{os.environ['DATABASE_URI']}"
    })
    # declaring the collection objects
    store = db.reference('/attendance')
except Exception as e:
    print(e)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('attendance.ui', self)
        self.stopThreads = False
        self.setWindowTitle('Attendance Register')
        self.stopThreads = False
        self.attdArray = []
        self.readData()
        # self.branch.currentIndexChanged.connect(self.branchListener)
        # self.semester.currentIndexChanged.connect(self.semListener)
        # self.section.currentIndexChanged.connect(self.sectionListener)
        self.search.clicked.connect(self.searchStudent)
        self.refresh.clicked.connect(self.refreshAction)

        # self.filters = {"branch": "", "semester": "", "section": ""}

    # this is the util function that will actually get the data
    def readData(self):
        self.attdArray = []
        for val in store.get():
            self.attdArray.append(val)

    # this function will keep on reading the data
    def getData(self):
        try:
            while 1 == 1:
                self.readData()
                time.sleep(10000)
                if self.stopThreads:
                    break
        except Exception as error:
            print(error)

    # this is the util function that will actually write the data
    def writeTable(self):
        try:
            self.table.setRowCount(len(self.attdArray))
            row = 0
            for item in self.attdArray:
                value = self.attdArray[item]
                col = 0
                self.table.setItem(row, col, QTableWidgetItem(f'{value["date"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{value["day"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{value["month"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{value["year"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{value["time"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{value["room"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{value["USN"]}'))
                row = row + 1
        except Exception as error:
            print(error)

    # this function will keep on updating table
    def updateTable(self):
        while 1 == 1:
            self.writeTable()
            time.sleep(1)
            if self.stopThreads:
                break

    # this function is for grouped query
    # def generalQuery(self):
    #     try:
    #         self.attdArray = store.get()
    #         if self.filters['branch'] != "":
    #             self.attdArray = self.filter(self.attdArray, 'branch', self.filters['branch'])
    #         if self.filters['semester'] != "":
    #             self.attdArray = self.filter(self.attdArray, 'sem', int(self.filters['semester']))
    #         if self.filters['section'] != "":
    #             self.attdArray = self.filter(self.attdArray, 'section', self.filters['section'])
    #
    #     except Exception as error:
    #         print(error)
    #
    # def filter(self, arr: list, field: str, value: str) -> list:
    #     dummy = []
    #     for val in arr:
    #         if val[f'{field}'] == value:
    #             dummy.append(val)
    #     return dummy
    #
    # def branchListener(self):
    #     try:
    #         self.filters['branch'] = self.branch.currentText()
    #         self.generalQuery()
    #
    #     except Exception as error:
    #         print(error)
    #
    # def semListener(self):
    #     try:
    #         self.filters['semester'] = self.semester.currentText()
    #         self.generalQuery()
    #
    #     except Exception as error:
    #         print(error)
    #
    # def sectionListener(self):
    #     try:
    #         self.filters['section'] = self.section.currentText()
    #         self.generalQuery()
    #
    #     except Exception as error:
    #         print(error)

    # this function is for search query
    def searchStudent(self):
        usn = self.usn.text()
        try:
            if usn != "":
                self.attdArray = store.get()
                temp_arr = []
                for val in self.attdArray:
                    value = self.attdArray[val]
                    if value['USN'] == usn:
                        temp_arr.append(value)
                self.attdArray = []
                for val in temp_arr:
                    self.attdArray.append(val)
            else:
                self.attdArray = store.get()

            self.usn.setText("")

        except Exception as error:
            print(error)

    def refreshAction(self):
        self.attdArray = store.get()
        # self.filters['branch'] = ""
        # self.filters['section'] = ""
        # self.filters['semester'] = ""
        # self.branch.setCurrentIndex = 0
        # self.semester.setCurrentIndex = 0
        # self.section.setCurrentIndex = 0


def mainFn():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.stopThreads = False
    Thread(target=main.readData).start()
    Thread(target=main.getData).start()
    Thread(target=main.writeTable).start()
    Thread(target=main.updateTable).start()
    # Thread(target=main.generalQuery).start()
    Thread(target=main.searchStudent).start()
    Thread(target=main.show()).start()
    sys.exit(exitApp())


def exitApp():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.stopThreads=True
    app.exec_()


if __name__ == '__main__':
    mainFn()
