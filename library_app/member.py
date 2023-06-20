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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("menu.ui", self)
        self.setWindowTitle("Point of Sale System")
        self.menuProduct.triggered.connect(self.open_product_record)
        self.btnProductTable.triggered.connect(self.open_product_table)
        self.btnUpdateMember.clicked.connect(self.update_member)

    def open_product_record(self):
        dialog = ProductDialog()
        dialog.exec()

    def open_product_table(self):
        table_dialog = ProductTableDialog()
        table_dialog.exec()


class ProductDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("product_dialog.ui", self)
        self.setWindowTitle("Product Record")
        self.tableProduct.setColumnCount(3)
        self.tableProduct.setRowCount(3)
        data = [
            ("Item 1", "Category 1", "Price 1"),
            ("Item 2", "Category 2", "Price 2"),
            ("Item 3", "Category 3", "Price 3"),
        ]
        for row, (item, category, price) in enumerate(data):
            self.tableProduct.setItem(row, 0, QTableWidgetItem(item))
            self.tableProduct.setItem(row, 1, QTableWidgetItem(category))
            self.tableProduct.setItem(row, 2, QTableWidgetItem(price))


class ProductTableDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("product_table_dialog.ui", self)
        self.setWindowTitle("Product Table")


class LibraryApp(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("member.ui", self)
        self.setWindowTitle("Library App")
        self.connection = self.create_connection()
        if self.connection is not None:
            self.load_data()
            self.btnAddMember.clicked.connect(self.add_member)
            self.btnUpdateMember.clicked.connect(self.update_member)
            self.btnDeleteMember.clicked.connect(self.delete_member)

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost", database="mydb", user="root", password=""
            )

            cursor = connection.cursor()
            cursor.execute("ALTER TABLE Library_Member AUTO_INCREMENT = 1")
            cursor.nextset()

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

    def add_member(self):
        member_name = self.txtMemberName.text()
        member_phone = self.txtMemberPhone.text()
        member_email = self.txtMemberEmail.text()
        membership_status = self.txtMembershipStatus.text()

        query = "INSERT INTO Library_Member (Member_Name, Member_Phone_Number, Member_Email, Membership_Status) VALUES (%s, %s, %s, %s)"
        data = (member_name, member_phone, member_email, membership_status)
        self.execute_query(query, data)

        self.update_member_ids()
        self.load_data()

    def update_member(self):
        member_id = self.tableMembers.item(self.tableMembers.currentRow(), 0).text()
        member_name = self.txtMemberName.text()
        member_phone = self.txtMemberPhone.text() or None
        member_email = self.txtMemberEmail.text()
        membership_status = self.txtMembershipStatus.text()

        query = "UPDATE Library_Member SET Member_Name = %s, Member_Phone_Number = %s, Member_Email = %s, Membership_Status = %s WHERE Member_ID = %s"
        data = (member_name, member_phone, member_email, membership_status, member_id)
        self.execute_query(query, data)
        self.load_data()

    def delete_member(self):
        member_id = self.tableMembers.item(self.tableMembers.currentRow(), 0).text()

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("Delete Member")
        msg_box.setText(f"Are you sure you want to delete member ID {member_id}?")
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            query = "DELETE FROM Library_Member WHERE Member_ID = %s"
            data = (member_id,)
            self.execute_query(query, data)
            self.update_member_ids()
            self.load_data()

    def update_member_ids(self):
        try:
            cursor1 = self.connection.cursor()
            cursor2 = self.connection.cursor()

            query1 = "SET @row_number = 0;"
            cursor1.execute(query1)

            query2 = "UPDATE Library_Member SET Member_ID = @row_number:=@row_number+1;"
            cursor2.execute(query2)

            cursor1.close()
            cursor2.close()

            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error updating member IDs: {e}")

    def load_data(self):
        query = "SELECT * FROM Library_Member"
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        self.tableMembers.setRowCount(len(result))
        for row_number, row_data in enumerate(result):
            for column_number, data in enumerate(row_data):
                self.tableMembers.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )

        self.tableMembers.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )


app = QApplication([])
main_window = LibraryApp()
main_window.show()
app.exec()