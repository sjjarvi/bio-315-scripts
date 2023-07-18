import sqlite3

dbPath = '/Users/scottjarvi/dev/sqllite/'
conn = sqlite3.connect(dbPath + 'belize_mackinnon_data.sqlite')
cur = conn.cursor()

print('Dropping table SPECIES_SURVEY ...')

cur.execute('DROP TABLE IF EXISTS SPECIES_SURVEY')

print('Creating table SPECIES_SURVEY ...')

cur.execute('''
CREATE TABLE SPECIES_SURVEY (location_id TEXT, survey_id TEXT, species_name TEXT)''')

print('Table SPECIES_SURVEY created!')

conn.commit()
cur.close()
