import requests
import pandas as pd
import os

states = pd.read_csv('state.csv')

params = {
    'format':'csv',
    'categories[]':'local',
    'active':'yes'
}


os.chdir('local')

places = states.name.unique()

for place in places:

    request = requests.get('https://openei.org/services/api/place/' + place + '/incentives/v1', params=params)

    with open(place+'_local.csv', 'wb') as f:
        f.write(request.content)
        f.close()

nevada = pd.read_csv('Nevada.csv')

incentivedf = pd.DataFrame(columns=nevada.columns)

os.listdir()

for f in os.listdir():
    df = pd.read_csv(f)
    df['state'] = f[:-4]
    incentivedf = incentivedf.append(df,ignore_index=True)


incentivedf.to_csv('StateIncentives.csv')

incentivedf.head()
