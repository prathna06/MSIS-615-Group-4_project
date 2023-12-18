import sqlite3
import pandas as pd
conn = sqlite3.connect('university_data.db')
university_data = pd.read_sql('SELECT * FROM university_data',conn)
print(university_data)

