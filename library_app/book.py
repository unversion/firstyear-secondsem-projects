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
        loadUi("book.ui", self)
        self.setWindowTitle("Library App")
        self.connection = self.create_connection()
        if self.connection is not None:
            self.load_data()
            self.btnAddBook.clicked.connect(self.add_book)
            self.btnUpdateBook.clicked.connect(self.update_book)
            self.btnDeleteBook.clicked.connect(self.delete_book)
            self.btnAddBook.clicked.connect(self.load_data)

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

    def add_book(self):
        book_title = self.txtBookTitle.text()
        book_author = self.txtBookAuthor.text()
        book_publication_year = self.txtPublicationYear.text()
        book_availability = self.txtBookAvailability.text()

        query = "INSERT INTO Book (Book_Title, Book_Author, Book_Publication_Year, Book_Availability) VALUES (%s, %s, %s, %s)"
        data = (book_title, book_author, book_publication_year, book_availability)
        self.execute_query(query, data)
        self.update_book_ids()
        self.load_data()

    def update_book(self):
        isbn = self.tableBooks.item(self.tableBooks.currentRow(), 0).text()
        book_title = self.txtBookTitle.text()
        book_author = self.txtBookAuthor.text()
        book_publication_year = self.txtPublicationYear.text()
        book_availability = self.txtBookAvailability.text()

        query = "UPDATE Book SET Book_Title = %s, Book_Author = %s, Book_Publication_Year = %s, Book_Availability = %s WHERE ISBN = %s"
        data = (book_title, book_author, book_publication_year, book_availability, isbn)
        self.execute_query(query, data)
        self.load_data()

    def delete_book(self):
        isbn = self.tableBooks.item(self.tableBooks.currentRow(), 0).text()
        book_title = self.txtBookTitle.text()

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("Delete Book")
        msg_box.setText(f"Are you sure you want to delete {book_title}?")
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            query = "DELETE FROM Book WHERE ISBN = %s"
            data = (isbn,)
            self.execute_query(query, data)
            self.update_book_ids()
            self.load_data()

    def load_data(self):
        query = "SELECT * FROM Book"
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        self.tableBooks.setRowCount(len(result))
        for row_number, row_data in enumerate(result):
            for column_number, data in enumerate(row_data):
                self.tableBooks.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )

        self.tableBooks.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    def update_book_ids(self):
        try:
            cursor1 = self.connection.cursor()
            cursor2 = self.connection.cursor()

            query1 = "SET @row_number = 0;"
            cursor1.execute(query1)

            query2 = "UPDATE Book SET ISBN = @row_number:=@row_number+1;"
            cursor2.execute(query2)

            cursor1.close()
            cursor2.close()

            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error updating book IDs: {e}")


app = QApplication([])
main_window = LibraryApp()
main_window.show()
sys.exit(app.exec())