import sys
import csv
import sqlite3

def parse_csv(location_identifier):
    file_path = f"{location_identifier}.csv"

    try:
        # TODO: Move this to common code
        dbPath = '/Users/scottjarvi/dev/sqllite/'
        conn = sqlite3.connect(dbPath + 'belize_mackinnon_data.sqlite')
        cur = conn.cursor()
        
        with open(file_path, "r", newline='', encoding='utf-8') as csv_file:
            #csv_reader = csv.DictReader(csv_file)
            csv_reader = csv.reader(csv_file)
            print('CSV File Opened', csv_reader)
            for row in csv_reader:
                #survey_id = row.get('survey_id')
                #species_name = row.get('species_name')
                survey_id = row[0]
                species_name = row[1]

                # skip header
                if (survey_id.endswith('survey_id')):
                    continue

                if survey_id and species_name:
                    if (int(survey_id) < 10 and len(survey_id) == 1):
                        survey_id = '0' + survey_id

                    print(f"Survey ID: {survey_id}, Species Name: {species_name}")
                    cur.execute('SELECT survey_id, species_name FROM SPECIES_SURVEY WHERE location_id = ? and survey_id = ? and species_name = ? ', (location_identifier, survey_id, species_name))
                    row = cur.fetchone()
                    if row is None:
                        cur.execute('''INSERT INTO SPECIES_SURVEY (location_id, survey_id, species_name)
                                VALUES (?, ?, ?)''', (location_identifier, survey_id, species_name))
                    else:
                        print('WARN: Records already exist')
                    conn.commit()

        cur.close()

    except FileNotFoundError:
        print(f"CSV file for location '{location_identifier}' not found.")
    except Exception as e:
        print(f"An error occurred while processing the CSV file: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python csv_parser.py <location_identifier>")
    else:
        location_identifier = sys.argv[1]
        parse_csv(location_identifier)
