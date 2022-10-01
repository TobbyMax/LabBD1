import os
import random
import time


def checkargs(args):
    if len(args) > 1:
        print("Too many arguments given. Try again.")
        return -1
    if len(args) == 0:
        print("Enter id number:")
        args.append(input())
    if not args[0].isdigit():
        print("Wrong input.")
        return -1
    return int(args[0])


class StudentTable:
    def __init__(self, mode, folderPath):
        self.fileName = folderPath + "\\stTable.txt"
        self.table = {}
        if mode == "OPEN":
            try:
                self.recover()
            except FileNotFoundError:
                print("Student table was not found. New student table created.")
                f = open(self.fileName, "wt")
        else:
            print("New student table created.")
            f = open(self.fileName, "wt")
            f.close()

    def recover(self):
        self.table.clear()
        f = open(self.fileName)
        for i in f.readlines():
            try:
                idn, name, surname, patronymic = i.rstrip('\n').split(' ')
                self.table[int(idn)] = {"name": name, "surname": surname, "patronymic": patronymic}
            except ValueError:
                pass
        f.close()

    def duplicateCheck(self, fullname):
        for key, val in self.table.items():
            if val["name"] == fullname[0] and val["surname"] == fullname[1] and val["patronymic"] == fullname[2]:
                print("A student with name <{} {} {}> already exists in the table with "
                      "id = {}.".format(fullname[0], fullname[1], fullname[2], key))
                print("Are you sure that you want to add this student again? (yes/no)")
                if input().lower() != "yes":
                    print("Student was not added to the table.")
                    return 1
                return 0
        return 0

    def save(self, args):
        with open(self.fileName, "wt") as f:
            for key, val in self.table.items():
                f.write('{} {} {} {}\n'.format(key, val["name"], val["surname"], val["patronymic"]))
        print("Changes in student table were saved.")

    def add(self, args):
        if len(args) > 3:
            print("Too many arguments given. Try again.")
            return
        if len(args) == 0:
            print("Enter new student full name:")
            args = input().title().split(' ')
        else:
            while len(args) < 3:
                args.append('-')
        fullname = [st.strip().title() for st in args]
        if self.duplicateCheck(fullname):
            return
        idn = 1
        if self.table.keys():
            idn = max(self.table.keys()) + 1
        self.table[idn] = dict(zip(["name", "surname", "patronymic"], fullname))
        print("Student was successfully added to the table.")
        print("id = {}, name = {}, surname = {}, "
              "patronymic = {}".format(idn, fullname[0], fullname[1], fullname[2]))

    def edit(self, args):
        idn = checkargs(args)
        if idn < 0:
            return
        if idn in self.table.keys():
            print('Row {} currently contains:\nname: {}, surname: {}, '
                  'patronymic: {}'.format(idn, self.table[idn]["name"],
                                          self.table[idn]["surname"], self.table[idn]["patronymic"]))
            print('Enter new student full name:')
            fullname = [i.strip() for i in input().title().split(' ')]
            while len(fullname) < 3:
                fullname.append('-')
            if self.duplicateCheck(fullname):
                return
            self.table[idn] = dict(zip(["name", "surname", "patronymic"], fullname))
            print("Student's attributes were successfully changed.")
            print("id = {}, name = {}, surname = {}, "
                  "patronymic = {}".format(idn, fullname[0], fullname[1], fullname[2]))
        else:
            print("There is no student with id = {} in the table.\n"
                  "Do you want to add student with this id? (yes, no)".format(idn))
            respond = input().lower()
            if respond == "yes":
                print("Enter changed full name:")
                fullname = [st.strip().title() for st in args]
                while len(fullname) < 3:
                    fullname.append('-')
                if self.duplicateCheck(fullname):
                    return
                self.table[idn] = dict(zip(["name", "surname", "patronymic"], fullname))
                print("Student was successfully added to the table.")
                print("id = {}, name = {}, surname = {}, "
                      "patronymic = {}".format(idn, fullname[0], fullname[1], fullname[2]))

    def delete(self, args):
        idn = checkargs(args)
        if idn < 0:
            return
        if idn in self.table.keys():
            print('Deleted row {}, which contained:\nname: {}, surname: {}, '
                  'patronymic: {}'.format(idn, self.table[idn]["name"],
                                          self.table[idn]["surname"], self.table[idn]["patronymic"]))
            self.table.pop(idn)
        else:
            print("There is no student with id = {} in the table.")

    def print(self, args):
        idn = checkargs(args)
        if idn < 0:
            return
        if idn in self.table.keys():
            print('Row {} contains:\nname: {}, surname: {}, '
                  'patronymic: {}'.format(idn, self.table[idn]["name"],
                                          self.table[idn]["surname"], self.table[idn]["patronymic"]))
        else:
            print("There is no student with id = {} in the table.".format(idn))

    def autofill(self, args):
        if len(args) == 0:
            print("Enter absolute path to source file:")
            args.append(input().strip())
        try:
            f = open(' '.join(args).strip('"'))
            count = 0
            for i in f.readlines():
                try:
                    surname, name, patronymic = [j.strip() for j in i.rstrip('\n').split(' ')]
                    if self.duplicateCheck([name, surname, patronymic]):
                        continue
                    idn = 1
                    if self.table.keys():
                        idn = max(self.table.keys()) + 1
                    self.table[idn] = {"name": name, "surname": surname, "patronymic": patronymic}
                    count += 1
                except ValueError:
                    pass
            f.close()
            print("{} students added successfully.".format(count))
        except FileNotFoundError or OSError:
            print("Cannot open the file.")


class VariantTable:
    def __init__(self, mode, folderPath):
        self.fileName = folderPath + "\\varTable.txt"
        self.table = {}
        if mode == "OPEN":
            try:
                self.recover()
            except FileNotFoundError:
                print("Variant table was not found. New variant table created.")
                f = open(self.fileName, "wt")
        else:
            print("New variant table created.")
            f = open(self.fileName, "wt")
            f.close()
    def recover(self):
        f = open(self.fileName)
        for i in f.readlines():
            try:
                idn, varname = i.rstrip('\n').split(' ')
                self.table[int(idn)] = varname
            except ValueError:
                pass
        f.close()

    def duplicateCheck(self, varname):
        for key, val in self.table.items():
            if val == varname:
                print("A variant with name <{}> already exists in the table with "
                      "id = {}.".format(varname, key))
                print("Are you sure that you want to add this variant again? (yes/no)")
                if input().lower() != "yes":
                    print("Variant was not added to the table.")
                    return 1
                return 0
        return 0

    def save(self, args):
        with open(self.fileName, "wt") as f:
            for key, val in self.table.items():
                f.write('{} {}\n'.format(key, val))
        print("Changes in variant table were saved.")

    def add(self, args):
        varname = ' '.join(args).strip()
        if self.duplicateCheck(varname):
            return
        idn = 1
        if self.table.keys():
            idn = max(self.table.keys()) + 1
        self.table[idn] = varname
        print("Variant was successfully added to the table.")
        print("id = {}, name = {}".format(idn, varname))

    def edit(self, args):
        idn = checkargs(args)
        if idn < 0:
            return
        if idn in self.table.keys():
            print('Row {} currently contains variant with name: {}'.format(idn, self.table[idn]))
            print('Enter  modified name of the variant:')
            varname = input().strip()
            if self.duplicateCheck(varname):
                return
            self.table[idn] = varname
            print("Variant's name was successfully changed.")
            print("id = {}, name = {}".format(idn, self.table[idn]))
        else:
            print("There is no variant with id = {} in the table."
                  "\nDo you want to add variant with this id? (yes, no)".format(idn))
            respond = input().lower()
            if respond == "yes":
                print("Enter name for new variant:")
                varname = input().strip()
                if self.duplicateCheck(varname):
                    return
                self.table[idn] = varname
                print("Variant was successfully added to the table.")
                print("id = {}, name = {}".format(idn, self.table[idn]))

    def delete(self, args):
        idn = checkargs(args)
        if idn < 0:
            return
        if idn in self.table.keys():
            print('Deleted row {}, which contained variant with name: {}'.format(idn, self.table[idn]))
            self.table.pop(idn)
        else:
            print("There is no variant with id = {} in the table.".format(idn))

    def print(self, args):
        idn = checkargs(args)
        if idn < 0:
            return
        if idn in self.table.keys():
            print('Row {} contains variant with name: {}'.format(idn, self.table[idn]))
        else:
            print("There is no variant with id = {} in the table.")

    def autofill(self, args):
        if len(args) == 0:
            print("Enter absolute path to source file:")
            args.append(input().strip())
        try:
            f = open(' '.join(args).strip('"'))
            count = 0
            for i in f.readlines():
                try:
                    varname = i.rstrip('\n').strip()
                    if self.duplicateCheck(varname):
                        continue
                    idn = 1
                    if self.table.keys():
                        idn = max(self.table.keys()) + 1
                    self.table[idn] = varname
                    count += 1
                except ValueError:
                    pass
            f.close()
            print("{} variants added successfully.".format(count))
        except FileNotFoundError:
            print("Cannot open the file.")


class DB:
    def __init__(self):
        self.stopflag = 0
        self.command = []
        while True:
            print("Choose:\nCREATE - Create new database\nOPEN - Open existing database\nLEAVE - Stop")
            option = input().upper()
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
            else:
                exit()
        self.stTable = StudentTable(option, self.folderPath)
        self.varTable = VariantTable(option, self.folderPath)
        self.directions = {"STUDENT": {"ADD": self.stTable.add, "EDIT": self.stTable.edit,
                                       "DELETE": self.stTable.delete, "PRINT": self.stTable.print,
                                       "SAVE": self.stTable.save, "FILL": self.stTable.autofill},
                           "VAR": {"ADD": self.varTable.add, "EDIT": self.varTable.edit,
                                   "DELETE": self.varTable.delete, "PRINT": self.varTable.print,
                                   "SAVE": self.varTable.save, "FILL": self.varTable.autofill},
                           "ALL": {"SAVE": self.save},
                           "TEST": {"GENERATE": self.generateTable, "PRINT": self.printGenerated},
                           "DB": {"QUIT": self.quit, "RECOVER": self.recover, "BACKUP": self.backup, "SAVE": self.save}
                           }

    def save(self, args):
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
                print("{:^50} {:^25}".format(' '.join([self.stTable.table[studID]["surname"],
                                                       self.stTable.table[studID]["name"],
                                                       self.stTable.table[studID]["patronymic"]]),
                                             self.varTable.table[varID]))
        except FileNotFoundError:
            print("Table was not generated yet.")

    def run(self):
        while not self.stopflag:
            try:
                function, obj, *args = input().split(' ')
                function, obj = function.upper(), obj.upper()
                try:
                    self.directions[obj][function](args)
                except KeyError:
                    print("Wrong input. Try again.")
            except ValueError:
                print("Not enough arguments given. Try again.")


if __name__ == '__main__':
    while True:
        db = DB()
        db.run()
