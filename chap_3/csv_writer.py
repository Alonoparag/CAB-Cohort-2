from csv import writer
from re import L
from faker import Faker


with open('my_csv.csv', mode='w') as output:
    mywriter=writer(output)
    fake=Faker()
    header=['name','age','street','city','state','zip','lng','lat']
    mywriter.writerow(header)
    for r in range (1000):
        row = [
            fake.name(),
            fake.random_int(min=18,max=80, step=1),
            fake.street_address(),
            fake.city(),
            fake.zipcode(),
            fake.longitude(),
            fake.latitude(),
            ]
        mywriter.writerow(row)
    


      