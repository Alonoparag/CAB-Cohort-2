import csv

with open('my_csv.csv') as infile:
    myreader=csv.DictReader(infile)
    headers=next(myreader)
    for row in myreader:
        print(row.name)
    