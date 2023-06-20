import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
)
from PyQt6.uic import loadUi


class LibraryApp(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("staff.ui", self)
        self.setWindowTitle("Library App")
        self.connection = self.create_connection()
        if self.connection is not None:
            self.load_data()
            self.btnAddStaff.clicked.connect(self.add_staff)
            self.btnUpdateStaff.clicked.connect(self.update_staff)
            self.btnDeleteStaff.clicked.connect(self.delete_staff)
            self.btnAddStaff.clicked.connect(self.load_data)

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost", database="mydb", user="root", password=""
            )
            print("Connected to MySQL database")
            return connection
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return None

    def execute_query(self, query, data=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            self.connection.commit()
            print("Query executed successfully")
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")

    def add_staff(self):
        staff_name = self.txtStaffName.text()
        staff_phone = self.txtStaffPhone.text() or None
        staff_email = self.txtStaffEmail.text() or None
        position = self.txtPosition.text()

        query = "INSERT INTO Library_Staff (Staff_Name, Staff_Phone_Number, Staff_Email, Position) VALUES (%s, %s, %s, %s)"
        data = (staff_name, staff_phone, staff_email, position)
        self.execute_query(query, data)
        self.update_staff_ids()
        self.load_data()

    def update_staff(self):
        staff_id = self.tableStaff.item(self.tableStaff.currentRow(), 0).text()
        staff_name = self.txtStaffName.text()
        staff_phone = self.txtStaffPhone.text() or None
        staff_email = self.txtStaffEmail.text() or None
        position = self.txtPosition.text()

        query = "UPDATE Library_Staff SET Staff_Name = %s, Staff_Phone_Number = %s, Staff_Email = %s, Position = %s WHERE Staff_ID = %s"
        data = (staff_name, staff_phone, staff_email, position, staff_id)
        self.execute_query(query, data)
        self.load_data()

    def delete_staff(self):
        staff_name = self.txtStaffName.text()

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("Delete Staff")
        msg_box.setText(f"Are you sure you want to delete {staff_name}?")
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            query = "DELETE FROM Library_Staff WHERE Staff_Name = %s"
            data = (staff_name,)
            self.execute_query(query, data)
            self.update_staff_ids()
            self.load_data()

    def load_data(self):
        query = "SELECT * FROM Library_Staff"
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        self.tableStaff.setRowCount(len(result))
        for row_number, row_data in enumerate(result):
            for column_number, data in enumerate(row_data):
                self.tableStaff.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )

        self.tableStaff.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    def update_staff_ids(self):
        try:
            cursor1 = self.connection.cursor()
            cursor2 = self.connection.cursor()

            query1 = "SET @row_number = 0;"
            cursor1.execute(query1)

            query2 = "UPDATE Library_Staff SET Staff_ID = @row_number:=@row_number+1;"
            cursor2.execute(query2)

            cursor1.close()
            cursor2.close()

            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error updating staff IDs: {e}")


app = QApplication([])
main_window = LibraryApp()
main_window.show()
sys.exit(app.exec())