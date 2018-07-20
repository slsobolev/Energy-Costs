import pandas as pd
import os
import glob
from sqlalchemy import create_engine

pw = input('PW:')
path = input('Folder Path:')

params = {
    'dbname':'energycosts',
    'user':'energycosts',
    'password': pw,
    'host':'georgetownenergycosts.cr1legfnv0nf.us-east-1.rds.amazonaws.com',
    'port': 5432
}

engine = create_engine('postgresql+psycopg2://energycosts:'+ pw +'@georgetownenergycosts.cr1legfnv0nf.us-east-1.rds.amazonaws.com:5432/energycosts')
conn = engine.raw_connection()

os.chdir(path)
filelist = glob.glob('*.csv')

print('Uploading ' + str(filelist))

for f in filelist:
    df = pd.read_csv(f)
    df.to_sql(f,engine,if_exists='fail')
