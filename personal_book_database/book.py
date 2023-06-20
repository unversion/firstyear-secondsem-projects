import os, mysql.connector

class Book: 
    def __init__(self, bookid, bookname, bookauthor, bookprice, bookrating): 
        self.bookid = bookid
        self.bookname = bookname
        self.bookauthor = bookauthor
        self.bookprice = bookprice
        self.bookrating = bookrating

class SearchBook: 
    def __init__(self, bookid):
        self.bookid = bookid

def connect():
    try:
        con = mysql.connector.connect(user="root", password="", host="localhost", database="book")
        print("Connection successful.")
    except mysql.connector.Error as e:
        print("Error connecting to database:", e)
    return con

def add(con):
    while True:
        try:
            book = Book(input("\nEnter Book ID: "), input("Enter Book Name: "), input("Enter Book Author: "), input("Enter Book Price: "), input("Enter Book Rating: "))
            cursor = con.cursor()
            cursor.execute("INSERT INTO booktable VALUES (%s, %s, %s, %s, %s)", (book.bookid, book.bookname, book.bookauthor, book.bookprice, book.bookrating))
            con.commit()
            print("\nRecord saved.\n")
        except mysql.connector.Error as e:
            print(e)
            con.rollback()
        if input("Add another record [Y/N]? ").lower() != "y":
            break

def edit(con):
    while True:
        try:
            book = Book(input("\nEnter Book ID: "), input("Enter Book Name: "), input("Enter Book Author: "), input("Enter Book Price: "), input("Enter Book Rating: "))
            cursor = con.cursor()
            cursor.execute("UPDATE booktable SET bookname = %s, bookauthor = %s, bookprice = %s, bookrating = %s WHERE bookid = %s", (book.bookname, book.bookauthor, book.bookprice, book.bookrating, book.bookid))
            con.commit()
            print("\nChanges saved.\n")
        except mysql.connector.Error as e:
            print(e)
            con.rollback()
        if input("Edit another record [Y/N]? ").lower() != "y":
            break

def delete(con):
    while True:
        try:
            cursor = con.cursor()
            cursor.execute("DELETE FROM booktable WHERE bookid = %s", (input("\nEnter Book ID: "),))
            con.commit()
            print("\nRecord deleted.\n")
        except mysql.connector.Error as e:
            print(e)
            con.rollback()
        if input("Delete another record [Y/N]? ").lower() != "y":
            break

def search(con):
    while True:
        try:
            searchbook = SearchBook(input("\nEnter Book ID: "))
            cursor = con.cursor()
            cursor.execute("SELECT bookname, bookauthor, bookprice, bookrating FROM booktable WHERE bookid = %s", (searchbook.bookid,))
            row = cursor.fetchone()
            if row:
                print("Book Name:", row[0])
                print("Book Author:", row[1])
                print("Book Price:", row[2])
                print("Book Rating:", row[3])
            else:
                print("\nRecord not found.")
        except mysql.connector.Error as e:
            print(e)
            con.rollback()
        if input("\nSearch another record [Y/N]? ").lower() != "y":
            break

def searchAll(con):
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM booktable")
        for row in cursor:
            print("Book ID:", row[0])
            print("Book Name:", row[1])
            print("Book Author:", row[2])
            print("Book Price:", row[3])
            print("Book Rating:", row[4], "\n")
    except mysql.connector.Error as e:
        print(e)
        con.rollback()
    input("Return to menu [Enter]? ")

def main():
    while True:
        print("\n[1] Add Record")
        print("[2] Edit Record")
        print("[3] Delete Record")
        print("[4] Search Record")
        print("[5] Show All Record")
        print("[0] Quit Program\n")
        x = input("Select option: ")
        os.system("clear")
        con = connect()
        if x == "0":
            quit()
        elif x == "1":
            add(con)
        elif x == "2":
            edit(con)
        elif x == "3":
            delete(con)
        elif x == "4":
            search(con)
        elif x == "5":
            searchAll(con)
        else:
            print("Invalid option.")
            
main()