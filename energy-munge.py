import pandas as pd
import os
import datetime
import glob
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


params = {
    'dbname':'energycosts',
    'user':'energycosts',
    'password':'Georgetown2018!',
    'host':'georgetownenergycosts.cr1legfnv0nf.us-east-1.rds.amazonaws.com',
    'port': 5432
}

engine = create_engine('postgresql+psycopg2://energycosts:Georgetown2018!@georgetownenergycosts.cr1legfnv0nf.us-east-1.rds.amazonaws.com:5432/energycosts')

zcta = pd.read_sql_table('zip_to_zcta',engine)
zipdens = pd.read_sql_table('zipdens', engine)
openpv = pd.read_sql_table('openpv',engine)

openpv['zipcode'].fillna(0, inplace=True)
openpv['zipcode'] = openpv['zipcode'].astype('int64',inplace=True)
type(openpv['zipcode'][1])

pvz, cz = openpv['zipcode'].unique(), zcta['ZIP_CODE'].unique()
zipcheck = [z for z in pvz if z not in cz]

zipdens.set_index('zip',inplace=True)
z1 = zcta.join(zipdens, on='ZIP_CODE',how='left')

z1.set_index('ZIP_CODE',inplace=True)
openpvjoin = openpv.join(z1,on='zipcode',how='right')

openpvjoin.to_csv('energy_munge_checkpoint')

iourates = pd.read_sql_table('iourates',engine)
noniourates = pd.read_sql_table('noniourates',engine)

iourates['zip'] = iourates['zip'].astype('int64',inplace=True)
noniourates['zip'] = noniourates['zip'].astype('int64',inplace=True)

iourates.set_index('zip',inplace=True)
noniourates.set_index('zip',inplace=True)

all_rates = iourates.join(noniourates, how='outer',rsuffix='_noniou')
all_rates.to_sql('all_rates',engine)

openei = pd.read_sql_table('openei',engine)

openpv['cost_per_watt'] = openpv['cost_per_watt'].astype(float)

openpv['cost_per_watt'].max()
openpv['cost_per_watt'].min()

list(openpv.columns)


openpvnew = openpv[openpv['year'] > 2015]

plt.rcParams['figure.figsize'] = (10.0, 8.0)
plt.hist(openpv['cost_per_watt'].dropna(), bins=30,label='Cost Per Watt',color='indianred')

boxlist=[iourates['comm_rate'],iourates['ind_rate'],iourates['res_rate']]

plt.boxplot(boxlist)


os.chdir('Energy-Costs/fixtures')
openpv = pd.read_csv('openpv_cln.csv',low_memory=False)

openpv = openpv[openpv['Year Installed'] >= 2014]

zipcosts = openpv.groupby(['zipcode','install_type','Year Installed']).mean()
zipcosts.head()

zipcosts.to_sql('openpv_cln_avg_by_zip',engine)



openpv['install_type'].unique()
it =

zcta.head()

zipcosts.set_index('zipcode')
zcta = zcta.set_index('ZIP_CODE')


zipcosts = zipcosts.join(zcta, on=['zipcode'])
zipcosts = zipcosts.join(zipdens,on=['ZCTA'])

zipcosts = zipcosts.join(iourates, on=['zipcode'], rsuffix='_iou')


zipcosts.join(noniourates, on=zipcosts.index[0],rsuffix='_noniou')

type(noniourates.index[1])

os.getcwd()

zipcosts.index.names
zipcosts.index.names=['zipcode','install_type','Year Installed']
zipcosts.to_csv('LabeledDataJoin.csv')

os.chdir(r'C:\Users\Sebastian Sobolev\Desktop\Georgetown Data Science\Energy-Costs\Incentives')

state_inc = pd.read_csv('StateIncentives.csv')

os.chdir(r'C:\Users\Sebastian Sobolev\Desktop\Georgetown Data Science\Energy-Costs\fixtures')
zipcosts = pd.read_csv('LabeledDataJoin.csv')

state_inc.incentive_type.unique()
statefip = state_inc[state_inc['incentive_type'] == 'Financial Incentive Programs']
statefip = statefip.groupby('state_abb').count()

statefip = statefip.iloc[:,:1]
statefip.to_csv('Financial_incentive_programs.csv')

zipcosts = zipcosts.join(statefip,on='STATE')

staterrp = state_inc[state_inc['incentive_type'] == 'Rules Regulations Policies Incentive Programs']
staterrp = staterrp.groupby('state_abb').count()
staterrp.to_csv('Rules_regs_policies.csv')

staterrp = staterrp.iloc[:,:1]
staterrp.columns = ['no_rules_reg_pol_incentive']

zipcosts = zipcosts.join(staterrp,on='STATE')

zipcosts[:5]['STATE']


income = pd.read_csv('ACS_Income.csv')
income.set_index('ZCTA', inplace=True)

zipcosts = zipcosts.join(income,on='ZCTA')

payroll = pd.read_csv('ZIP_employment_payroll.csv')
payroll.set_index('Zip',inplace=True)

zipcosts = zipcosts.join(payroll)

hhs = pd.read_csv('ZCTA_Households.csv')
hhs.set_index('ZCTA',inplace=True)

zipcosts = zipcosts.join(hhs,on='ZCTA')

zipcosts.to_csv('Labeled_Data_08Jul.csv')
zipcosts.to_sql('labeled_data_08Jul',engine)
