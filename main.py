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
    store = db.reference('/students')
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
        self.generalVal = {}
        self.branch.currentIndexChanged.connect(self.branchListener)
        self.semester.currentIndexChanged.connect(self.semListener)
        self.section.currentIndexChanged.connect(self.sectionListener)
        self.search.clicked.connect(self.searchStudent)

    # this is the util function that will actually get the data
    def readData(self):
        self.attdArray=[]
        for val in store.get():
            print(val)
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
                col = 0
                self.table.setItem(row, col, QTableWidgetItem(f'{item["dates"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{item["month"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{item["year"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{item["usn"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{item["name"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{item["sem"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{item["attendance"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{item["branch"]}'))
                col = col+1
                self.table.setItem(row, col, QTableWidgetItem(f'{item["section"]}'))
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
    def generalQuery(self):
        try:
            field = self.generalVal['field']
            value = self.generalVal['value']
            print(field, value)
            temp_arr = []
            for val in self.attdArray:
                if val[f'{field}'] == value:
                    temp_arr.append(val)
            self.attdArray = []
            for val in temp_arr:
                self.attdArray.append(val)
        except Exception as error:
            print(error)

    def branchListener(self):
        self.generalVal = {"field": 'branch', "value": self.branch.currentText()}
        self.generalQuery()

    def semListener(self):
        self.generalVal = {"field": 'sem', "value": self.semester.currentText()}
        self.generalQuery()

    def sectionListener(self):
        self.generalVal = {"field": 'section', "value": self.section.currentText()}
        self.generalQuery()

    # this function is for search query
    def searchStudent(self):
        name = self.name.text()
        usn = self.usn.text()
        try:
            if name != "" and usn != "":
                self.attdArray = store.get()
                temp_arr = []
                for val in self.attdArray:
                    if val['name'] == name and val['usn'] == usn:
                        temp_arr.append(val)
                self.attdArray = []
                for val in temp_arr:
                    self.attdArray.append(val)
            elif name !="" and usn == "":
                self.attdArray = store.get()
                temp_arr = []
                for val in self.attdArray:
                    if val['name'] == name:
                        temp_arr.append(val)
                self.attdArray = []
                for val in temp_arr:
                    self.attdArray.append(val)
            elif name == "" and usn != "":
                self.attdArray = store.get()
                temp_arr = []
                for val in self.attdArray:
                    if val['usn'] == usn:
                        temp_arr.append(val)
                self.attdArray = []
                for val in temp_arr:
                    self.attdArray.append(val)
            else:
                self.attdArray = store.get()


        except Exception as error:
            print(error)


def mainFn():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.stopThreads = False
    Thread(target=main.readData).start()
    Thread(target=main.getData).start()
    Thread(target=main.writeTable).start()
    Thread(target=main.updateTable).start()
    Thread(target=main.generalQuery).start()
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
