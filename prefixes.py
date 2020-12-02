import csv
import subprocess

class Prefixes:
    prefixInfo = []

    def __init__(self):
        super().__init__()
        prefixInfo = self.csvHelper('prefixes.csv')

    def getPrefix(self, guild):
        for data in self.prefixInfo:
            if data[0] == str(hash(guild)):
                return data[1]
        return "!"

    def setPrefix(self, guild, prefix):
        count = 0
        for data in self.prefixInfo:
            if data[0] == hash(guild):
                self.prefixInfo.pop(count)
                self.prefixInfo.append([str(hash(guild)), prefix])
                break
            else:
                count = count + 1
        
        self.prefixInfo.append([str(hash(guild)), prefix])

        # Delete existing version of prefix.
        lines = self.csvHelper('prefixes.csv')
        for line in lines:
            if lines == [[]]:
                break
            else:
                if line[0] == str(hash(guild)):
                    lines.remove(line)
                    break

        with open('prefixes.csv', 'w', newline='') as prefix_file:
            # Repopulate file with item removed and fixes formatting
            prefix_writer = csv.writer(prefix_file, lineterminator='\r')
            prefix_writer.writerows(lines)
        
        with open('prefixes.csv', mode='a+', newline='') as prefix_file:
            # Use of 'a+' allows generation of file where nonexistant. Refer to csv library.
            prefix_writer = csv.writer(prefix_file, lineterminator='\r')
            item = [hash(guild), prefix]
            prefix_writer.writerow(item) # Appends new addition

        self.prefixInfo = self.csvHelper('prefixes.csv')

        self.commit("Refresh prefixes.csv")

        return prefix

    def commit(self, message):
        commit_message = f'{message}'

        run("commit", "-am", commit_message)
        run("push", "-u", "origin", "master")

    def showPrefixes(self):
        print(self.prefixInfo)

    # HELPER FUNCTION
    def csvHelper(self, filename):
        ''' Generates list of items.
            Inputs: filename : macro file
            Outputs: List of items in file '''
    
        lines = list()
        with open(filename, 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lines.append(row)
        return lines
