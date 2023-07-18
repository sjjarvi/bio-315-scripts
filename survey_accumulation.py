# This is a rudimentary script for parsing a CSV of Mackinnon list data
# and creating an output CSV of incremental and cummulative counts of species for each survey
#
# parameters: location identifier corresponding to an existing CSV of species survey data
#
# To run:
# python3 survey_accumulation.py <location_identifier>
# where <location_identifier> maps to a CSV file named <location_identifier>.csv.
# For example, for location identifier 'punta_gorda' you would run:
# python3 survey_accumulation.py punta_gorda
# and the script expects a file in the same directory with the name 'punta_gorda.csv'
import sys
import csv

# function to write accumulation data results to a csv file of the name
# <location_identifier>-results.csv
def write_accumulation_data(location_identifier, accumulation_data):
    csvFilename = f"{location_identifier}-results.csv"
    with open(csvFilename, 'w', newline='') as csvfile :
        csvWriter = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_MINIMAL)
        for row in accumulation_data:    
            csvWriter.writerow(row)

# Given a location identifier, will obtain the parsed data
# from 'parse_csv' and compute the cummulative counts for each 
# survey
def analyze_survey_data(location_identifier):
    speciesSurveyData = parse_csv(location_identifier)
    cumulativeCount = 0
    allItems = set()
    accumulationCounts = [('survey', '#new', 'cumulative')]

    for surveyId, species in sorted(speciesSurveyData.items()):
        # debugging, uncomment line below
        #print(surveyId, species)
        print(f"processing survey {surveyId} with {len(species)} species")
        currentCount = len(allItems)
        allItems |= species
        newCount = len(allItems)
        difference = newCount - currentCount        
        accumulationCounts.append((surveyId, difference, newCount))
        cumulativeCount = newCount

    print('-----------------------------')
    for row in accumulationCounts:
        print(row)
    
    print(f"Final count for {location_identifier}:", cumulativeCount)
    write_accumulation_data(location_identifier, accumulationCounts)

# Finds a local file named <location_identifier>.csv and parses it into 
# a dictionary object where the key is the survey id and the value is
# a Set of species
# returns the resulting dictionary object
def parse_csv(location_identifier):
    print('Location', location_identifier)
    file_path = f"{location_identifier}.csv"
    speciesSurveyData = dict()

    with open(file_path, "r", newline='', encoding='utf-8') as csv_file:
            # TODO: figure out issue with dictionary reader
            #csv_reader = csv.DictReader(csv_file)
            csv_reader = csv.reader(csv_file)
            print('CSV File Opened', csv_reader)
            for row in csv_reader:
                survey_id = row[0]
                species_name = row[1]

                # skip header row
                if (survey_id.endswith('survey_id')):
                    continue

                if survey_id and species_name:
                    if (int(survey_id) < 10 and len(survey_id) == 1):
                        survey_id = '0' + survey_id

                    # debugging, uncomment line below
                    #print(f"Survey ID: {survey_id}, Species Name: {species_name}")
                    recordedSpecies = speciesSurveyData.get(survey_id, set())
                    recordedSpecies.add(species_name)
                    speciesSurveyData[survey_id] = recordedSpecies
            
    return speciesSurveyData


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python survey_accumulation.py <location_identifier>")
    else:
        location_identifier = sys.argv[1]
        analyze_survey_data(location_identifier)
