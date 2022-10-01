import os
import random
import time
from students import StudentTable
from variants import VariantTable


class DB:
    def __init__(self):
        self.stopflag = 0
        self.autoflag = 0
        self.command = []
        while True:
            print("\nChoose:\nCREATE - Create new database\nOPEN - Open existing database\nLEAVE - Stop")
            option, *args = input().upper().split(" ")
            if option == "OPEN":
                print("Enter name of existing database:")
                self.dbName = input().strip()
                if self.dbName not in os.listdir("C:\\Users\\ageev\\PycharmProjects\\LabBD1\\databases"):
                    print("Database does not exist.\n")
                    continue
                self.folderPath = "C:\\Users\\ageev\\PycharmProjects\\LabBD1\\databases\\" + self.dbName
                break
            elif option == "CREATE":
                print("Enter name for new database:")
                self.dbName = input()
                self.folderPath = "C:\\Users\\ageev\\PycharmProjects\\LabBD1\\databases\\" + self.dbName
                try:
                    os.mkdir(self.folderPath)
                    break
                except FileExistsError:
                    print("Database already exists.\n")
            elif option == "LEAVE":
                exit()
            else:
                print("Wrong input. Try again.")
        self.stTable = StudentTable(option, self.folderPath)
        self.varTable = VariantTable(option, self.folderPath)
        self.directions = {"STUDENT": {"ADD": self.stTable.add, "EDIT": self.stTable.edit,
                                       "DELETE": self.stTable.delete, "PRINT": self.stTable.print,
                                       "SAVE": self.stTable.save, "FILL": self.stTable.autofill,
                                       "HELP": self.stTable.help},
                           "VAR": {"ADD": self.varTable.add, "EDIT": self.varTable.edit,
                                   "DELETE": self.varTable.delete, "PRINT": self.varTable.print,
                                   "SAVE": self.varTable.save, "FILL": self.varTable.autofill,
                                   "HELP": self.varTable.help},
                           "TEST": {"GENERATE": self.generateTable, "PRINT": self.printGenerated},
                           "DB": {"CLOSE": self.quit, "SWITCH": self.quit, "RECOVER": self.recover,
                                  "BACKUP": self.backup, "SAVE": self.save,
                                  "HELP": self.help, "AUTOSAVE": self.autosave},
                           }

    def help(self, args):
        print("List of commands:")
        commands = {"STUDENT": {"ADD <name> [<surname>] [<patronymic>]": "add new student to the table",
                                "EDIT <id_number>": "edit name of existing student",
                                "DELETE <id_number>": "delete student from the table",
                                "PRINT <id_number>": "print name of existing student",
                                "SAVE": "save changes in the table",
                                "FILL": "import students from file",
                                "HELP": "show list of options"},
                    "VAR": {"ADD <variant name>": "add new variant to the table",
                            "EDIT <id_number>": "edit name of existing variant",
                            "DELETE <id_number>": "delete variant from the table",
                            "PRINT <id_number>": "print name of existing variant",
                            "SAVE": "save changes in the table",
                            "FILL": "import variants from file",
                            "HELP": "show list of options"},
                    "TEST": {"GENERATE": "generate testing table", "PRINT": "print testing table"},
                    "DB": {"CLOSE": "close data base",
                           "SWITCH": "start working with new data base",
                           "RECOVER": "recover a database from back-up file",
                           "BACKUP": "back-up changes", "SAVE": "save changes in the data base",
                           "AUTOSAVE": "turn on/off autosave option"},
                    }
        for obj in commands.keys():
            print(obj, " <options>")
            for func in commands[obj].keys():
                print("{:<5} {:<20} {:<50}".format("", func, commands[obj][func]))
        print()

    def save(self, args):
        print()
        self.stTable.save(args)
        self.varTable.save(args)

    def quit(self, args):
        print("Do you want to save changes before quitting? (yes/no)")
        answer = input().lower().strip()
        if answer == "yes":
            self.save(args)
        self.stopflag = 1

    def backup(self, args):
        self.save(args)
        backupPath = self.folderPath + "\\backup"
        if "backup" not in os.listdir(self.folderPath):
            os.mkdir(backupPath)
        version = "bu_" + str(len(os.listdir(backupPath))) + time.strftime(" (%Y-%m-%d %H-%M-%S)", time.localtime())
        backupPath += ("\\" + version)
        os.mkdir(backupPath)
        with open(self.stTable.fileName) as stTable:
            with open(backupPath + "\\stTable.txt", "wt") as stBackUp:
                stBackUp.write(stTable.read())
        with open(self.varTable.fileName) as varTable:
            with open(backupPath + "\\varTable.txt", "wt") as varBackUp:
                varBackUp.write(varTable.read())
        try:
            with open(self.folderPath + "\\testTable.txt") as testTable:
                with open(backupPath + "\\testTable.txt", "wt") as testBackUp:
                    testBackUp.write(testTable.read())
        except FileNotFoundError:
            pass
        print("Latest data base version backed-up successfully as ", version)

    def recover(self, args):
        backupPath = self.folderPath + "\\backup"
        if "backup" not in os.listdir(self.folderPath):
            print("No back-up versions available.")
            return
        print("Available back-up versions:")
        for v in os.listdir(backupPath):
            print(v)
        print("Copy and paste version name to choose which one to recover:")
        version = input().strip()
        if version not in os.listdir(backupPath):
            print("There is no version with name:", version)
        backupPath += ("\\" + version)
        self.backup(args)
        with open(self.stTable.fileName, "wt") as stTable:
            with open(backupPath + "\\stTable.txt", "rt") as stBackUp:
                stTable.write(stBackUp.read())
        with open(self.varTable.fileName, "wt") as varTable:
            with open(backupPath + "\\varTable.txt", "rt") as varBackUp:
                varTable.write(varBackUp.read())
        try:
            with open(self.folderPath + "\\testTable.txt", "wt") as testTable:
                with open(backupPath + "\\testTable.txt", "rt") as testBackUp:
                    testTable.write(testBackUp.read())
        except FileNotFoundError:
            pass
        self.stTable.recover()
        self.varTable.recover()
        print("Version {} recovered successfully".format(version))

    def autosave(self, args):
        if not self.autoflag:
            self.autoflag = 1
            print("AUTOSAVE is ON.")
        else:
            self.autoflag = 0
            print("AUTOSAVE is OFF.")

    def generateTable(self, args):
        generatedName = self.folderPath + "\\testTable.txt"
        f = open(generatedName, "wt")
        if not self.stTable.table.keys():
            print("Cannot create Test Table, because Student Table is empty.")
            return
        if not self.varTable.table.keys():
            print("Cannot create Test Table, because Variant Table is empty.")
            return
        for studID in self.stTable.table.keys():
            f.write("{} {}\n".format(studID, random.choice(list(self.varTable.table.keys()))))
        f.close()
        print("Table was generated successfully.")

    def printGenerated(self, args):
        generatedName = self.folderPath + "\\testTable.txt"
        gen = {}
        try:
            f = open(generatedName)
            for i in f.readlines():
                try:
                    studID, varID = i.split(' ')
                    gen[int(studID)] = int(varID)
                except ValueError:
                    pass
            print("{:^50} {:^25}".format("full_name", "path_to_file"))
            for studID, varID in gen.items():
                try:
                    fullname = ' '.join([self.stTable.table[studID]["surname"],
                              self.stTable.table[studID]["name"],
                              self.stTable.table[studID]["patronymic"]])
                except KeyError:
                    print("Student with id = {} was removed in the table.".format(studID))
                    continue
                try:
                    print("{:^50} {:^25}".format(fullname, self.varTable.table[varID]))
                except KeyError:
                    print("Variant with id = {} was removed in the table.".format(varID))
                    continue
        except FileNotFoundError:
            print("Table was not generated yet.")

    def run(self):
        print("Enter DB HELP to see options.")
        while not self.stopflag:
            try:
                print()
                obj, function, *args = input().split(' ')
                obj, function = obj.upper(), function.upper()
                try:
                    self.directions[obj][function](args)
                    if self.autoflag and (function == "ADD" or function == "EDIT"
                                          or function == "DELETE" or function == "FILL"
                                          or function == "AUTOSAVE" and self.autoflag == 1):
                        self.save(args)
                except KeyError:
                    print("Wrong input. Try again.")
                    print("Enter DB HELP to see options.")
            except ValueError:
                print("Not enough arguments given. Try again.")
                print("Enter DB HELP to see options.")