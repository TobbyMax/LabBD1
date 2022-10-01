from students import checkargs

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

    def help(self, args):
        commands = {"ADD <variant name>": "add new variant to the table",
                    "EDIT <id_number>": "edit name of existing variant",
                    "DELETE <id_number>": "delete variant from the table",
                    "PRINT <id_number>": "print name of existing variant",
                    "SAVE": "save changes in the table",
                    "FILL": "import variants from file",
                    "HELP": "show list of options"}
        print("VAR <options>")
        for func in commands.keys():
            print("{:<5}{:<20}{:<50}".format(" ", func, commands[func]))
        print()

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
