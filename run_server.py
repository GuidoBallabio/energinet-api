#!/home/daibak/.virtualenvs/iot/bin/python

import re
import sys

from datasette.cli import cli

from utils import DB_FILE, download_recent, RepeatedTimer

def run_daily_fetch():
    return RepeatedTimer(60*60*24, download_recent)

def main():  
    with run_daily_fetch() as deamon:
        sys.argv += [DB_FILE.as_posix(), "-m", "metadata.json"]
        exit_code = cli()
        
    return exit_code
        

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())    
