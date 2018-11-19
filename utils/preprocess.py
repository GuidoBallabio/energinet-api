"""Preprocess the data and insert in DB."""

import pandas as pd
import sqlalchemy as sa
import pathlib as pathlib

# Parameters

PROJECT_DIR = pathlib.Path(__file__).parent.parent
DB_FILE = PROJECT_DIR / "data" / "db.sqlite"

DB_URI = f'sqlite:///{DB_FILE.absolute().as_posix()}'
TABLE_NAME = 'CO2'


## Places of the measurements as columns of the DataFrame
## obtained from on onlinedata file as:
## import codecs
## with codecs.open("20181104_onlinedata.txt", "r", "latin1") as f:
##   t = f.read()
## t=t.splitlines()[20:0]
## col = [s[3:] for s in t[:20]]

col = ['Centrale kraftværker DK1',
       'Centrale kraftværker DK2',
       'Decentrale kraftværker DK1',
       'Decentrale kraftværker DK2',
       'Vindmøller DK1',
       'Vindmøller DK2',
       'Udveksling Jylland-Norge',
       'Udveksling Jylland-Sverige',
       'Udveksling Jylland-Tyskland',
       'Udveksling Sjælland-Sverige',
       'Udveksling Sjælland-Tyskland',
       'Udveksling Bornholm-Sverige',
       'Udveksling Fyn-Sjaelland',
       'Temperatur i Malling',
       'Vindhastighed i Malling',
       'CO2 udledning',
       'Havmøller DK',
       'Landmøller DK',
       'Solceller DK1',
       'Solceller DK2']

def preprocess_file(file_name):
    '''
    Preprocess accepts a file that should be formatted as *onlinedata.txt and returns a DataFrame of its content.
    '''

    # Create DataFrame from file
    df = pd.read_csv(file_name, sep=';', skiprows=21, skip_blank_lines=True)
    
    # Remove useless columns and prettify it
    
    ## Remove useless column
    df.drop(['Unnamed: 21'], axis=1, inplace=True)
    ## Remove whitespace from columns' name
    df.rename(str.strip, axis='columns', inplace=True)
    ## Rename datetime column
    df.rename(index=str, columns={df.columns[0]: "Timestamp"}, inplace=True)
    ## Cast Timestamp column to datetime type and format for improved functionalties
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
    ## Set Timestamp column as index (useless?)
    df.set_index(df.columns[0], inplace=True)

    df.columns = col

    return df

def add_to_db(df, db_uri, table_name):
    '''
    Add DataFrame (returned by preprocess) to the database
    '''

    en = sa.create_engine(db_uri)

    df.to_sql(table_name, en, if_exists='append')
