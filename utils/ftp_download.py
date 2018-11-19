"""Download new files through FTP."""

from datetime import datetime

import ftputil
import sqlalchemy as sa

from .preprocess import DB_URI, TABLE_NAME, preprocess_file, add_to_db

# FTP parameters

server = '194.239.2.174'
username = 'ftp000148'
password = '?4xesufevuyEta'

def ftp():
    return ftputil.FTPHost(server, username, password)

def in_db(date):
    en = sa.create_engine(DB_URI)
    
    s = sa.text(
            "SELECT count(*) "
            "FROM CO2 as c "
            "WHERE c.Timestamp = :x")
               
    timestamp = date.strftime("%Y-%m-%d %H:%M:%S.%f")
    res = en.execute(s, x=timestamp)
    found = res.fetchall()[0][0] != 0
    res.close()

    return found
    

def download_recent():
    with ftp() as conn:
        last = conn.listdir("onlinedata")[-1]
        date = datetime.strptime(last[:8], "%Y%m%d")

        if not in_db(date):
            dest = "data/" + last
            conn.download("onlinedata/" + last, dest)
         
            df = preprocess_file(dest)
            add_to_db(df, DB_URI, TABLE_NAME)
