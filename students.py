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

    def help(self, args):
        commands = {"ADD <name> [<surname>] [<patronymic>]": "add new student to the table",
                    "EDIT <id_number>": "edit name of existing student",
                    "DELETE <id_number>": "delete student from the table",
                    "PRINT <id_number>": "print name of existing student",
                    "SAVE": "save changes in the table",
                    "FILL": "import students from file"}
        print("STUDENT <options>")
        for func in commands.keys():
            print("{:<5}{:<20}{:<50}".format(" ", func, commands[func]))

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
                fullname = [st.strip().title() for st in input().split(' ')]
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
