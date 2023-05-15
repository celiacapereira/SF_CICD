import os
import snowflake.connector
from snowflake.connector import *
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

account = os.environ['SF_ACCOUNT']
password = os.environ['SF_PASSWORD']
username= os.environ['SF_USERNAME']


print(f"SF ACCOUNT IS:  {account}")
print(f"SF PASSWORD IS:  {password}")
print(f"SF USERNAME IS:  {username}")

print("Vamos testar a connecção")

connection = snowflake.connector.connect (
    user=username,
    password=password,
    account=account
)

cursor = connection.cursor()
cursor.execute("SELECT * FROM DEV.RAW.TITANIC_TRAIN_RAW")
df = cursor.fetch_pandas_all()
# cursor.close()

df_drop = df.drop(['NAME', 'TICKET', 'FARE', 'CABIN', 'EMARKED'], axis = 1)

#Calcular a média da mulher: 
mulher = pd.DataFrame(df_drop.loc[df_drop.SEX == 'female']['AGE'])
mulher_drop_na = mulher.dropna(subset = ["AGE"], inplace=True)
media_mulher = int(mulher[["AGE"]].mean())

#Calcular a média para homens:
homem = pd.DataFrame(df_drop.loc[df_drop.SEX == 'male']['AGE'])
homem_drop_na= homem.dropna(subset = ["AGE"], inplace=True)
media_homem = int(homem[["AGE"]].mean())

def Fill_Age(data):
    age = data[0]
    sex = data[1]

    if pd.isnull(age):
        if sex == 'male': 
            return media_homem
        else:
            return media_mulher
    else:
        return age
df_drop['AGE'] = df_drop[['AGE','SEX']].apply(Fill_Age,axis=1)        

#Criar coluna por gruposde idades
bins = [10, 20, 30, 40, 50, 60, 70, 80]
labels = ['0-10', '10-29', '30-39', '40-49', '50-59', '60-69', '70-80']

age = df_drop['AGE']
df_drop['AgeRange'] = pd.cut(age, bins, labels = labels, include_lowest = True)

df_drop.rename(columns = {'AgeRange':'AGERANGE'}, inplace = True)


connection.cursor().execute("USE WAREHOUSE COMPUTE_WH;")

connection.cursor().execute("CREATE OR REPLACE SCHEMA DEV.REPORT; ")

connection.cursor().execute(""" CREATE TABLE DEV.REPORT.TITANIC_REPORT_STAGING (
    PASSENGERID INT,
    SURVIVED INT, 
    PCLASS INT, 
    SEX VARCHAR(6), 
    AGE INT, 
    SIBSP INT, 
    PARCH INT, 
    AGERANGE VARCHAR(5)
    )""")


success, num_chunks, num_rows, output = write_pandas(
            conn=connection,
            df=df_drop,
            table_name='TITANIC_REPORT_STAGING',
            database='DEV',
            schema='REPORT'
        )
cursor.close()
