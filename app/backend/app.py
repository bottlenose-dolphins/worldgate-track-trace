import pandas as pd
from sqlalchemy import create_engine

oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'

engine = create_engine(
    oracle_connection_string.format(
        username='wg',
        password='wgdemo*()',
        hostname='202.73.56.175',
        port='1521',
        database='efprod',
    )
)

data = pd.read_sql("SELECT * FROM IMPORT", engine)
print(data)