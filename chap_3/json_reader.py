import pandas as pd
import pandas.io.json as pd_json

infile=open('my_json.json')

data=pd_json.loads(infile.read())
df=pd_json.json_normalize(data,record_path='records')
print(df)
