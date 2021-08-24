from faker import Faker
import json

with open('my_json.json','w') as outfile:
    fake=Faker()
    alldata={}
    alldata['records']=[]
    for r in range (1000):
        data={
            'name':fake.name(),
            'age':fake.random_int(min=18,max=80, step=1),
            'street_address':fake.street_address(),
            'city':fake.city(),
            'zipcode':fake.zipcode(),
            'longitude':float(fake.longitude()),
            'latitude':float(fake.latitude()),
        }
        alldata['records'].append(data)
    json.dump(alldata,outfile)