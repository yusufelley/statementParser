import PyPDF2
import re
import csv
import sys
import os

class Entry:
    def __init__(self, date, name, cost):
        self.date = date
        self.name = name
        self.cost = cost

def isDate(string): 
    return re.fullmatch('[0-2][1-9]/[0-3][1-9]', string)

def isCost(string):
    return re.fullmatch('([0-9]{1,3},)*[0-9]{1,3}.[0-9]{2}', string)


if len(sys.argv) > 1:
    folder = sys.argv[1]
else: 
    folder = 'input'   

sum = 0

for filename in os.listdir(folder):

    file = open('{folder}/{filename}'.format(folder=folder, filename=filename),'rb')
    pdfReader = PyPDF2.PdfFileReader(file)

    # creating a page object
    pageObj = pdfReader.getPage(2)
    # extracting text from page
    text = pageObj.extractText()
    start = text.find("Purchases and Adjustments")
    end = text.find("TOTAL PURCHASES AND ADJUSTMENTS FOR THIS PERIOD")

    table = text[start:end].split('\n')

    entries = []
    numWrote = 0
    for row in table:
        if(row != '' and row[0] == '0'):
            line = row.split()
            cost = line[len(line) - 1]
            date = line[0]
            name = ''
            for word in line[2:len(line) - 5]:
                name = name + ' ' + word
                name = name.lstrip()
            
            if(name and isCost(cost) and isDate(date)):
                entries.append(Entry(date, name, cost))
         

    with open('/home/yusuf/codeProjects/statementParser/output/{filename}.csv'.format(filename=filename[0:-4]), 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Date', 'Name', 'Cost'])
        for entry in entries:
            writer.writerow([entry.date, entry.name, entry.cost])
            numWrote += 1
            sum += float(entry.cost)

    print('Successfully wrote {numWrote} entries to csv file'.format(numWrote=numWrote))
  
    # closing the pdf file object
    file.close()

print(sum)




