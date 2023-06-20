import csv, os, re

class Record:
    def __init__(self, recordname):
        self.recordname = recordname
        self.recordlist = []
    def displayrecord(self):
        for r in self.recordlist:
            print()
            print(r)

def readclass():
    file_name = input("Enter file name: ")

    class Data:
        def __init__(self, row, header, the_id):
            self.__dict__ = dict(zip(header, row)) 
            self.the_id = the_id
        def __repr__(self):
            return self.the_id

    data = list(csv.reader(open(file_name)))
    instances = [Data(a, data[0], "id_{}".format(i+1)) for i, a in enumerate(data[1:])]

    print(data)
    print()
    print(instances)

storage = Record("storage")
container = []
header = []
subheader = []
newvalues = []

def editselect():
    print("\n[1] Rename file")
    print("[2] Delete file")
    print("[0] Go back\n")

    try:
        editoption = int(input("Select option: "))
    except ValueError:
        print("\nPlease enter a number.")
        editselect()

    while True:
        if editoption == 1:
            old = input("Enter file name: ")
            new = input("Give new name: ")
            try:
                os.rename(old, new)
            except FileNotFoundError:
                print("\nIt does not exist or has been deleted.")
            editselect()
        elif editoption == 2:
            deletefile()
        elif editoption == 0:
            menu()
        else:
            editselect()

def addfile():
    header.clear()
    wfn = input("\nEnter file name: ")

    with open(wfn + ".csv", "w") as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"')

        try:
            rows = int(input("Enter number of rows: "))
        except ValueError:
            print("\nPlease enter a number.")
            menu()

        for i in range(rows):
            data = input("Enter data: ")
            header.append(data)
            
        container.append(header)
        csv_writer.writerow(header)

    addselect = input("Keep adding? (Y/N): ")
    if addselect.lower() == "y":
        addfile()
    elif addselect.lower() == "n":
        menu()
    else:
        print("\nInvalid answer.")
        menu()

def editdata():
    newvalues.clear()
    file = input("\nEnter file name: ")

    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            data = list(reader)
    except FileNotFoundError:
        print("\nIt does not exist or has been deleted.")
        manipulatedata()

    try:
        for (i, item) in enumerate(data, start=0):
            print(i, item)
    except UnboundLocalError:
        editdata()

    try:
        rowindex = int(input("Enter row index: "))
        rows = int(input("Enter number of rows: "))
    except ValueError:
        print("\nPlease enter a number.")
        editdata()
    
    for i in range(rows):
        value = input("Enter data: ")
        newvalues.append(value)
        print(newvalues)

    container.append(newvalues)
    data[rowindex] = newvalues

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    manipulatedata()

def manipulatedata():
    print("\n[1] Add data")
    print("[2] Edit data")
    print("[3] Delete data")
    print("[0] Go back\n")

    try:
        manipulateoption = int(input("Select option: "))
    except ValueError:
        print("\nPlease enter a number.")
        manipulatedata()

    while True:
        if manipulateoption == 1:
            adddata()
        elif manipulateoption == 2:
            editdata()
        elif manipulateoption == 3:
            deletedata()
        elif manipulateoption == 0:
            menu()
        else:
            print("\nInvalid answer.")
            manipulatedata()

def adddata():
    subheader.clear()
    efn = input("\nEnter file name: ")
    
    try:
        with open(efn, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)

            with open(efn, "a", newline="") as f:
                csv_writer = csv.writer(f, delimiter=',', quotechar='"')

                try:
                    rows = int(input("Enter number of rows: "))
                except ValueError:
                    print("\nPlease enter a number.")
                    manipulatedata()
                
                for i in range(rows):
                    subdata = input("Enter data: ")
                    subheader.append(subdata)
                    print(subheader)

                container.append(subheader)
                csv_writer.writerow(subheader)    
        manipulatedata()
    except FileNotFoundError:
        print("\nIt does not exist or has been deleted.")
        manipulatedata()

def deletefile():
    osdelete = input("\nEnter file name: ")

    try:
        os.remove(osdelete)
    except FileNotFoundError:
        print("\nIt does not exist or has been deleted.")
        editselect()

    deleteselect = input("Keep deleting? (Y/N): ")
    if deleteselect.lower() == "y":
        deletefile()
    elif deleteselect.lower() == "n":
        menu()
    else:
        print("\nInvalid answer.")
        menu()

def searchdata():
    file = input("\nEnter file name: ")
    search = input("Search: ")

    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            data = list(reader)
        for line in data:
            for string in line:
                if re.match("(?i)" + search, string):
                    print(string)
    except FileNotFoundError:
        print("\nIt does not exist or has been deleted.")
        menu()

def deletedata():
    file = input("\nEnter file name: ")

    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            data = list(reader)
        for (i, item) in enumerate(data, start=0):
            print(i, item)
    except FileNotFoundError:
        print("\nIt does not exist or has been deleted.")
        manipulatedata()

    try:
        deleteindex = int(input("Delete row index: "))
    except ValueError:
        print("\nPlease enter a number.")
        manipulatedata()

    try:
        del data[deleteindex]
    except IndexError:
        print("\nIt does not exist or has been deleted.")
        manipulatedata()
        
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    manipulatedata()

def displayoption():
    while True:
        print("\n[1] Read data")
        print("[2] Show history")
        print("[0] Go back\n")

        try:
            optiondisplay = int(input("Select option: "))
        except ValueError:
            print("\nPlease enter a number.")
            menu()

        if optiondisplay == 1:
            readclass()
        elif optiondisplay == 2:
            storage.displayrecord()
        elif optiondisplay == 0:
            menu()
        else:
            print("\nInvalid option.")
            displayoption()

def menu():
    while True:
        print("\n[1] Add file")
        print("[2] Edit file")
        print("[3] Manipulate data")
        print("[4] Search data")
        print("[5] Display data")
        print("[0] Exit program\n")

        option = input("Select option: ")

        if option == "1":
            addfile()
        elif option == "2":
            editselect()
        elif option == "3":
            manipulatedata()
        elif option == "4":
            searchdata()
        elif option == "5":
            displayoption()
        elif option == "0":
            quit()
        else:
            print("\nInvalid option.")

storage.recordlist.append(container)
menu()