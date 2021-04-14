"""

@Author: Eduardo Mariscal
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from datetime import datetime

import sys, os
import sqlite3

from os import path

def resource_path(relative_path):
    """ Get absolute path resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets, uic

FORM_CLASS, _ = loadUiType(resource_path("Main.ui"))



class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.Month_Update()

    def Handel_Buttons(self):
        self.Customer_Refresh_Button.clicked.connect(self.GET_DATA)
        #self.All_Count_Button.clicked.connect(self.SEARCH_COUNT)
        self.All_First_Button.clicked.connect(self.SEARCH_FIRST)
        self.Customer_Birth_Button.clicked.connect(self.CUSTOMER_SEARCH_BIRTHDATE)
        self.Customer_First_Last_Button.clicked.connect(self.CUSTOMER_SEARCH_FIRST_LAST)
        self.Update_ResidentName_Search_Button.clicked.connect(self.UPDATE_SEARCH_RESIDENT_NAME)
        self.Update_ResidentUpdate_Button.clicked.connect(self.UPDATE_UPDATE_RESIDENT_WEIGHT)
        self.Update_ResidentUpdate_Button.clicked.connect(self.UPDATE_EDIT_NAMEWEIGHT_RESIDENT)
        self.Update_Edit_ResidentName_Button.clicked.connect(self.UPDATE_EDIT_NAMEBIRTHDATE_RESIDENT)
        self.Update_ResidentDelete_Button.clicked.connect(self.UPDATE_DELETE_RESIDENT)
        self.Update_ResidentAdd_Button.clicked.connect(self.UPDATE_NEW_RESIDENT)
        self.Update_ResidentAddWeight_Button.clicked.connect(self.UPDATE_RESIDENT_ADD_WEIGHT_CURRENT)
        self.Update_EditAddWeight_Button.clicked.connect(self.UPDATE_EDITADDWEIGHT_EDITMONTHYEAR)
        self.Update_EditEditWeight_Button.clicked.connect(self.UPDATE_EDITEDITWEIGHT)
        self.Update_EditDeleteWeight_Button.clicked.connect(self.UPDATE_EDITDELETEWEIGHT_EDITMONTHYEAR)
        self.Update_Previous_Button.clicked.connect(self.UPDATE_PREVIOUS_BUTTON)
        self.Update_Next_Button.clicked.connect(self.UPDATE_NEXT_BUTTON)

    def GET_DATA(self):

        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()
        cursor2 = db.cursor()
        cursor3 = db.cursor()
        cursor4 = db.cursor()

        command = '''SELECT FirstLastName, BirthDate from Customers_tables ORDER BY FirstLastName'''

        result = cursor.execute(command)

        for row_number, row_data in enumerate(result):

            Customer_Name = row_data[0]
            Customer_BirthDate = row_data[1]

            print(row_data)

            command2 = ''' SELECT Month, Weight FROM Customer_DateWeight_table WHERE FirstLastName LIKE ? AND BirthDate LIKE ? ORDER BY Year DESC,
            Case Month WHEN ? THEN 12 WHEN ? THEN 11 WHEN ? THEN 10 WHEN ? THEN 9 WHEN ? THEN 8 WHEN ? THEN 7 WHEN ? THEN 6
            WHEN ? THEN 5 WHEN ? THEN 4 WHEN ? THEN 3 WHEN ? THEN 2 WHEN ? THEN 1 END DESC LIMIT 7'''

            result2 = cursor2.execute(command2, [Customer_Name, Customer_BirthDate, "December", "November", "October",
                                                "September", "August", "July", "June", "May", "April", "March", "February",
                                                "January"])

            list1 = []
            for row_number2, row_data_2 in enumerate(result2):
                list1.append(row_data_2[0])
                list1.append(row_data_2[1])

            print(list1)
            print(len(list1))
            if len(list1) == 0:
                row = (Customer_Name, Customer_BirthDate)
                command3 = ''' UPDATE Customers_tables SET Current = NULL, WT0 = NULL, Month1 = NULL, WT1 = NULL, Month2 = NULL, WT2 = NULL, Month3 = NULL, WT3 = NULL, Month4 = NULL, WT4 = NULL, Month5 = NULL, WT5 = NULL, Month6 = NULL, WT6 = NULL   WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''
                cursor3.execute(command3, row)
                db.commit()
            elif len(list1) == 2:
                print(list1[0], list1[1])
                row = (list1[0], list1[1], Customer_Name, Customer_BirthDate)
                command3 = ''' UPDATE Customers_tables SET Current = ?, WT0 = ?, Month1 = NULL, WT1 = NULL, Month2 = NULL, WT2 = NULL, Month3 = NULL, WT3 = NULL, Month4 = NULL, WT4 = NULL, Month5 = NULL, WT5 = NULL, Month6 = NULL, WT6 = NULL  WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''
                cursor3.execute(command3, row)
                db.commit()
            elif len(list1) == 4:
                print(list1[0], list1[1], list1[2], list1[3])
                decimal = (list1[1]-list1[3])/list1[3]
                percentage = "{:.2%}".format(decimal)
                row = (percentage, list1[0], list1[1], list1[2], list1[3], Customer_Name, Customer_BirthDate)
                command3 = ''' UPDATE Customers_tables SET WT1Month = ?, Current = ?, WT0 = ?, Month1 = ?, WT1 = ?, Month2 = NULL, WT2 = NULL, Month3 = NULL, WT3 = NULL, Month4 = NULL, WT4 = NULL, Month5 = NULL, WT5 = NULL, Month6 = NULL, WT6 = NULL  WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''
                cursor3.execute(command3, row)
            elif len(list1) == 6:
                print(list1[0], list1[1], list1[2], list1[3], list1[4], list1[5])
                decimal = (list1[1]-list1[3])/list1[3]
                percentage = "{:.2%}".format(decimal)
                # decimal1 = (list1[1]-list1[5])/list1[5]
                # percentage1 = "{:.2%}".format(decimal1)
                row = (percentage, list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], Customer_Name, Customer_BirthDate)
                command3 = ''' UPDATE Customers_tables SET WT1Month = ?, Current = ?, WT0 = ?, Month1 = ?, WT1 = ?, Month2 = ?, WT2 = ?, Month3 = NULL, WT3 = NULL, Month4 = NULL, WT4 = NULL, Month5 = NULL, WT5 = NULL, Month6 = NULL, WT6 = NULL WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''
                cursor3.execute(command3, row)
            elif len(list1) == 8:
                print(list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6], list1[7])

                decimal = (list1[1]-list1[3])/list1[3]
                percentage = "{:.2%}".format(decimal)
                decimal1 = (list1[1]-list1[7])/list1[7]
                percentage1 = "{:.2%}".format(decimal1)
                row = (percentage, percentage1, list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6], list1[7], Customer_Name, Customer_BirthDate)
                command3 = ''' UPDATE Customers_tables SET WT1Month = ?, WT3Month = ?, Current = ?, WT0 = ?, Month1 = ?, WT1 = ?, Month2 = ?, WT2 = ?, Month3 = ?, WT3 = ?, Month4 = NULL, WT4 = NULL, Month5 = NULL, WT5 = NULL, Month6 = NULL, WT6 = NULL WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''
                cursor3.execute(command3, row)
            elif len(list1) == 10:
                print(list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6], list1[7], list1[8], list1[9])
                decimal = (list1[1]-list1[3])/list1[3]
                percentage = "{:.2%}".format(decimal)
                decimal1 = (list1[1]-list1[7])/list1[7]
                percentage1 = "{:.2%}".format(decimal1)

                row = (percentage, percentage1, list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6], list1[7], list1[8], list1[9], Customer_Name, Customer_BirthDate)

                command3 = ''' UPDATE Customers_tables SET WT1Month = ?, WT3Month = ?, Current = ?, WT0 = ?, Month1 = ?, WT1 = ?, Month2 = ?, WT2 = ?, Month3 = ?, WT3 = ?, Month4 = ?, WT4 = ?, Month5 = NULL, WT5 = NULL, Month6 = NULL, WT6 = NULL WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''
                cursor3.execute(command3, row)
            elif len(list1) == 12:
                print(list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6], list1[7], list1[8], list1[9], list1[10], list1[11])
                decimal = (list1[1]-list1[3])/list1[3]
                percentage = "{:.2%}".format(decimal)
                decimal1 = (list1[1]-list1[7])/list1[7]
                percentage1 = "{:.2%}".format(decimal1)
                row = (percentage, percentage1, list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6], list1[7], list1[8], list1[9], list1[10], list1[11], Customer_Name, Customer_BirthDate)
                command3 = ''' UPDATE Customers_tables SET WT1Month = ?, WT3Month = ?, Current = ?, WT0 = ?, Month1 = ?, WT1 = ?, Month2 = ?, WT2 = ?, Month3 = ?, WT3 = ?, Month4 = ?, WT4 = ?, Month5 = ?, WT5 = ?, Month6 = NULL, WT6 = NULL WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''
                cursor3.execute(command3, row)
            elif len(list1) >= 14:
                print(list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6], list1[7], list1[8], list1[9], list1[10], list1[11], list1[12], list1[13])
                decimal = (list1[1]-list1[3])/list1[3]
                percentage = "{:.2%}".format(decimal)
                decimal1 = (list1[1]-list1[7])/list1[7]
                percentage1 = "{:.2%}".format(decimal1)
                decimal2 = (list1[1]-list1[13])/list1[13]
                percentage2 = "{:.2%}".format(decimal2)
                row = (percentage, percentage1, percentage2, list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6], list1[7], list1[8], list1[9], list1[10], list1[11], list1[12], list1[13], Customer_Name, Customer_BirthDate)
                command3 = ''' UPDATE Customers_tables SET WT1Month = ?, WT3Month = ?, WT6Month = ?, Current = ?, WT0 = ?, Month1 = ?, WT1 = ?, Month2 = ?, WT2 = ?, Month3 = ?, WT3 = ?, Month4 = ?, WT4 = ?, Month5 = ?, WT5 = ?, Month6 = ?, WT6 = ? WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''
                cursor3.execute(command3, row)

        db.commit()
        db.commit()
        db.commit()
        self.SEARCH_FIRST()


    def SEARCH_COUNT(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        nbr = int(self.All_Count_Input.text())

        command = ''' SELECT * from Customers_tables WHERE count <=? ORDER BY FirstLastName'''

        result = cursor.execute(command, [nbr])

        self.All_Table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.All_Table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.All_Table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def SEARCH_FIRST(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        All_Input = self.All_Edit_Search_Button.text()
        All_Input_Plus = '%' + All_Input + '%'

        command = ''' SELECT * from Customers_tables WHERE FirstLastName LIKE ? ORDER BY FirstLastName'''

        result = cursor.execute(command, [All_Input_Plus])

        self.All_Table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.All_Table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.All_Table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def CUSTOMER_SEARCH_FIRST_LAST(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Customer_Edit_First_Button.text()
        Customer_Name_Plus = '%' + Customer_Name + '%'

        command = '''SELECT FirstLastName, BirthDate from Customers_tables WHERE FirstLastName LIKE ? ORDER BY FirstLastName'''

        result = cursor.execute(command, [Customer_Name_Plus])

        self.Customer_Table_FirstLastBirth.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.Customer_Table_FirstLastBirth.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Customer_Table_FirstLastBirth.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def Month_Update(self):

        current_month_num = datetime.now().month
        if current_month_num == 1:
            current_month_txt = "January"
        elif current_month_num == 2:
            current_month_txt = "February"
        elif current_month_num == 3:
            current_month_txt = "March"
        elif current_month_num == 4:
            current_month_txt = "April"
        elif current_month_num == 5:
            current_month_txt = "May"
        elif current_month_num == 6:
            current_month_txt = "June"
        elif current_month_num == 7:
            current_month_txt = "July"
        elif current_month_num == 8:
            current_month_txt = "August"
        elif current_month_num == 9:
            current_month_txt = "September"
        elif current_month_num == 10:
            current_month_txt = "October"
        elif current_month_num == 11:
            current_month_txt = "November"
        elif current_month_num == 12:
            current_month_txt = "December"

        current_year = datetime.now().year

        self.Update_Current_Month_Edit.setText(str(current_month_txt))
        self.Update_Current_Year_Edit.setText(str(current_year))

    def CUSTOMER_SEARCH_BIRTHDATE(self):
        # Connect to Sqlite3 database ad fill GUI table with data

        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Customer_Edit_First_Button.text()
        Customer_Name_Plus = '%' + Customer_Name + '%'
        Customer_BirthDate = self.Customer_Edit_Birth_Button.text()

        command = ''' SELECT Year, Month, Weight FROM Customer_DateWeight_table WHERE FirstLastName LIKE ? AND BirthDate LIKE ? ORDER BY Year DESC, 
        Case Month WHEN ? THEN 12 WHEN ? THEN 11 WHEN ? THEN 10 WHEN ? THEN 9 WHEN ? THEN 8 WHEN ? THEN 7 WHEN ? THEN 6 
        WHEN ? THEN 5 WHEN ? THEN 4 WHEN ? THEN 3 WHEN ? THEN 2 WHEN ? THEN 1 END DESC'''

        result = cursor.execute(command, [Customer_Name_Plus, Customer_BirthDate, "December", "November", "October",
                                          "September", "August", "July", "June", "May", "April", "March", "February",
                                          "January"])

        self.Customer_Table_DateWeight.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.Customer_Table_DateWeight.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Customer_Table_DateWeight.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        command2 = '''SELECT FirstLastName, BirthDate from Customers_tables WHERE FirstLastName LIKE ? AND BirthDate Like ? ORDER BY FirstLastName'''

        result2 = cursor.execute(command2, [Customer_Name_Plus, Customer_BirthDate])

        self.Customer_FirstLastBirth_Table.setRowCount(0)

        for row_number, row_data in enumerate(result2):
            self.Customer_FirstLastBirth_Table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Customer_FirstLastBirth_Table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def UPDATE_SEARCH_RESIDENT_NAME(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_Name_Plus = '%' + Customer_Name + '%'

        command = '''SELECT FirstLastName, BirthDate from Customers_tables WHERE FirstLastName LIKE ? ORDER BY FirstLastName'''

        result = cursor.execute(command, [Customer_Name_Plus])

        self.Update_ResidentSeach_Table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.Update_ResidentSeach_Table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Update_ResidentSeach_Table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def UPDATE_UPDATE_RESIDENT_WEIGHT(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_Name_Plus = '%' + Customer_Name + '%'
        Customer_BirthDate = self.Update_Edit_BirthDate_Button.text()
        Customer_BirthDate = '%' + Customer_BirthDate + '%'

        command = '''SELECT FirstLastName, BirthDate from Customers_tables WHERE FirstLastName LIKE ? AND BirthDate LIKE ? ORDER BY FirstLastName'''

        result = cursor.execute(command, [Customer_Name_Plus, Customer_BirthDate])

        self.Update_ResidentBirthDate_Table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.Update_ResidentBirthDate_Table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Update_ResidentBirthDate_Table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        command2 = ''' SELECT Year, Month, Weight FROM Customer_DateWeight_table WHERE FirstLastName LIKE ? AND BirthDate LIKE ? ORDER BY Year DESC, 
        Case Month WHEN ? THEN 12 WHEN ? THEN 11 WHEN ? THEN 10 WHEN ? THEN 9 WHEN ? THEN 8 WHEN ? THEN 7 WHEN ? THEN 6 
        WHEN ? THEN 5 WHEN ? THEN 4 WHEN ? THEN 3 WHEN ? THEN 2 WHEN ? THEN 1 END DESC'''

        result2 = cursor.execute(command2, [Customer_Name_Plus, Customer_BirthDate, "December", "November", "October",
                                           "September", "August", "July", "June", "May", "April", "March", "February",
                                           "January"])

        self.Update_MonthWeight_Table.setRowCount(0)

        for row_number, row_data in enumerate(result2):
            self.Update_MonthWeight_Table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Update_MonthWeight_Table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def UPDATE_RESIDENT_ADD_WEIGHT_CURRENT(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_BirthDate = self.Update_Edit_BirthDate_Button.text()
        Customer_Weight = self.Update_Current_Edit_Weigt_Box.text()
        current_month_num = datetime.now().month
        current_year_num = datetime.now().year

        if current_month_num == 1:
            current_month_txt = "January"
        elif current_month_num == 2:
            current_month_txt = "February"
        elif current_month_num == 3:
            current_month_txt = "March"
        elif current_month_num == 4:
            current_month_txt = "April"
        elif current_month_num == 5:
            current_month_txt = "May"
        elif current_month_num == 6:
            current_month_txt = "June"
        elif current_month_num == 7:
            current_month_txt = "July"
        elif current_month_num == 8:
            current_month_txt = "August"
        elif current_month_num == 9:
            current_month_txt = "September"
        elif current_month_num == 10:
            current_month_txt = "October"
        elif current_month_num == 11:
            current_month_txt = "November"
        elif current_month_num == 12:
            current_month_txt = "December"

        row = (Customer_Name, Customer_BirthDate, current_year_num, current_month_txt, Customer_Weight)

        command = ''' INSERT INTO Customer_DateWeight_table (FirstLastName, BirthDate, Year, Month, Weight) VALUES (?,?,?,?,?)'''

        cursor.execute(command, row)

        db.commit()
        self.UPDATE_UPDATE_RESIDENT_WEIGHT()
        self.GET_DATA()

    def UPDATE_EDIT_NAMEWEIGHT_RESIDENT(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_Name_Plus = '%' + Customer_Name + '%'
        Customer_BirthDate = self.Update_Edit_BirthDate_Button.text()

        command = ''' SELECT FirstLastName, BirthDate FROM Customers_tables WHERE FirstLastName LIKE ? AND BirthDate = ? ORDER BY FirstLastName'''

        result = cursor.execute(command, [Customer_Name_Plus, Customer_BirthDate])

        val = result.fetchone()
        self.Update_Edit_ResidentName_Box.setText(str(val[0]))
        self.Update_Edit_ResidentBirthdate_Box.setText(str(val[1]))



    def UPDATE_EDIT_NAMEBIRTHDATE_RESIDENT(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        resident_name = self.Update_Edit_ResidentName_Box.text()
        resident_birthdate = self.Update_Edit_ResidentBirthdate_Box.text()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_Name_Plus = '%' + Customer_Name + '%'
        Customer_BirthDate = self.Update_Edit_BirthDate_Button.text()

        row = (resident_name, resident_birthdate, Customer_Name_Plus, Customer_BirthDate)

        command = ''' UPDATE Customers_tables SET FirstLastName = ?, BirthDate = ? WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''

        cursor.execute(command, row)

        command2 = ''' UPDATE Customer_DateWeight_table SET FirstLastName = ?, BirthDate = ? WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''

        cursor.execute(command2, row)
        db.commit()
        self.Update_Edit_First_Button.setText(resident_name)
        self.Update_Edit_BirthDate_Button.setText(resident_birthdate)

        self.UPDATE_UPDATE_RESIDENT_WEIGHT()
        self.UPDATE_SEARCH_RESIDENT_NAME()
        self.GET_DATA()


    def UPDATE_DELETE_RESIDENT(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_Name_Plus = '%' + Customer_Name + '%'
        Customer_BirthDate = self.Update_Edit_BirthDate_Button.text()

        command = ''' DELETE FROM Customers_tables WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''

        command2 = ''' DELETE FROM Customer_DateWeight_table WHERE FirstLastName LIKE ? AND BirthDate LIKE ?'''

        cursor.execute(command, [Customer_Name_Plus, Customer_BirthDate])

        cursor.execute(command2, [Customer_Name_Plus, Customer_BirthDate])

        db.commit()

        self.UPDATE_UPDATE_RESIDENT_WEIGHT()
        self.UPDATE_SEARCH_RESIDENT_NAME()
        self.GET_DATA()

    def UPDATE_NEW_RESIDENT(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_BirthDate = self.Update_Edit_BirthDate_Button.text()

        row = (Customer_Name, Customer_BirthDate)

        command = ''' INSERT INTO Customers_tables (FirstLastName, BirthDate) VALUES (?,?)'''

        cursor.execute(command, row)

        db.commit()

        self.UPDATE_SEARCH_RESIDENT_NAME()
        self.UPDATE_UPDATE_RESIDENT_WEIGHT()
        self.GET_DATA()

    def UPDATE_EDITADDWEIGHT_EDITMONTHYEAR(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_BirthDate = self.Update_Edit_BirthDate_Button.text()
        Customer_Weight = self.Update_Edit_Weigt_Box.text()
        current_month_num = str(self.Update_Month_Edit.currentText())
        #        QDateTimeEdit Update_Year_Edit;
        current_year_num = str(self.Update_Year_Edit.date().year())

        if current_month_num == 1:
            current_month_txt = "January"
        elif current_month_num == 2:
            current_month_txt = "February"
        elif current_month_num == 3:
            current_month_txt = "March"
        elif current_month_num == 4:
            current_month_txt = "April"
        elif current_month_num == 5:
            current_month_txt = "May"
        elif current_month_num == 6:
            current_month_txt = "June"
        elif current_month_num == 7:
            current_month_txt = "July"
        elif current_month_num == 8:
            current_month_txt = "August"
        elif current_month_num == 9:
            current_month_txt = "September"
        elif current_month_num == 10:
            current_month_txt = "October"
        elif current_month_num == 11:
            current_month_txt = "November"
        elif current_month_num == 12:
            current_month_txt = "December"

        row = (Customer_Name, Customer_BirthDate, current_year_num, current_month_num, Customer_Weight)

        command = ''' INSERT INTO Customer_DateWeight_table (FirstLastName, BirthDate, Year, Month, Weight) VALUES (?,?,?,?,?)'''

        cursor.execute(command, row)

        db.commit()
        self.UPDATE_UPDATE_RESIDENT_WEIGHT()
        self.GET_DATA()


    def UPDATE_EDITEDITWEIGHT(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        resident_name = self.Update_Edit_ResidentName_Box.text()
        resident_birthdate = self.Update_Edit_ResidentBirthdate_Box.text()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_Name_Plus = '%' + Customer_Name + '%'
        Customer_BirthDate = self.Update_Edit_BirthDate_Button.text()
        Customer_Weight = int(self.Update_Edit_Weigt_Box.text())
        current_month_num = str(self.Update_Month_Edit.currentText())
        #        QDateTimeEdit Update_Year_Edit;
        current_year_num = str(self.Update_Year_Edit.date().year())

        row = (Customer_Weight, Customer_Name_Plus, Customer_BirthDate, current_year_num, current_month_num)

        command2 = '''UPDATE Customer_DateWeight_table SET Weight = ? WHERE FirstLastName LIKE ? AND BirthDate LIKE ? 
        AND Year LIKE ? AND Month LIKE ? '''

        cursor.execute(command2, row)
        db.commit()

        self.UPDATE_UPDATE_RESIDENT_WEIGHT()
        self.GET_DATA()


    def UPDATE_EDITDELETEWEIGHT_EDITMONTHYEAR(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_Name_Plus = '%' + Customer_Name + '%'
        Customer_BirthDate = self.Update_Edit_BirthDate_Button.text()
        current_month_num = str(self.Update_Month_Edit.currentText())
        #        QDateTimeEdit Update_Year_Edit;
        current_year_num = str(self.Update_Year_Edit.date().year())

        command = ''' DELETE FROM Customer_DateWeight_table WHERE FirstLastName LIKE ? AND BirthDate LIKE ? 
        AND Year LIKE ? AND Month LIKE ?'''

        cursor.execute(command, [Customer_Name_Plus, Customer_BirthDate, current_year_num, current_month_num])

        db.commit()

        self.UPDATE_UPDATE_RESIDENT_WEIGHT()
        self.GET_DATA()



    def UPDATE_PREVIOUS_BUTTON(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_Name_Plus = '%' + Customer_Name + '%'
        Customer_BirthDate = self.Update_Edit_BirthDate_Button.text()

        command = '''SELECT FirstLastName, BirthDate from Customers_tables ORDER BY FirstLastName DESC'''

        result = cursor.execute(command)

        # self.Customer_Table_FirstLastBirth.setRowCount(0)
        x = False

        for row_number, row_data in enumerate(result):
            if row_data[0] == Customer_Name and row_data[1] == Customer_BirthDate:

                x = True
            elif x == True:

                x = False

                self.Update_Edit_ResidentName_Box.setText(row_data[0])
                self.Update_Edit_ResidentBirthdate_Box.setText(row_data[1])
                self.Update_Edit_First_Button.setText(row_data[0])
                self.Update_Edit_BirthDate_Button.setText(row_data[1])
            else:
                pass
        self.UPDATE_SEARCH_RESIDENT_NAME()
        self.UPDATE_UPDATE_RESIDENT_WEIGHT()

    def UPDATE_NEXT_BUTTON(self):
        # Connect to Sqlite3 database ad fill GUI table with data
        db = sqlite3.connect(resource_path("CustomerData.db"))
        cursor = db.cursor()

        Customer_Name = self.Update_Edit_First_Button.text()
        Customer_Name_Plus = '%' + Customer_Name + '%'
        Customer_BirthDate = self.Update_Edit_BirthDate_Button.text()

        command = '''SELECT FirstLastName, BirthDate from Customers_tables ORDER BY FirstLastName'''

        result = cursor.execute(command)

        # self.Customer_Table_FirstLastBirth.setRowCount(0)
        x = False

        for row_number, row_data in enumerate(result):
            if row_data[0] == Customer_Name and row_data[1] == Customer_BirthDate:

                x = True
            elif x == True:

                x = False

                self.Update_Edit_ResidentName_Box.setText(row_data[0])
                self.Update_Edit_ResidentBirthdate_Box.setText(row_data[1])
                self.Update_Edit_First_Button.setText(row_data[0])
                self.Update_Edit_BirthDate_Button.setText(row_data[1])
            else:
                pass
        self.UPDATE_SEARCH_RESIDENT_NAME()
        self.UPDATE_UPDATE_RESIDENT_WEIGHT()
    # Here is our code


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
