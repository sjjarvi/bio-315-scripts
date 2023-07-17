
surveys = [
    {'b1', 'b2', 'b3', 'b4', 'b5'},
    {'b4', 'b5', 'b6', 'b7', 'b8'},
    {'b4', 'b5', 'b6', 'b7', 'b9'},
    {'b6', 'b7', 'b9', 'b10', 'b11'}
]

cumulativeCount = 0
previousSurvey = None
currentSurvey = None
allItems = set()

for survey in surveys:
    currentCount = len(allItems)
    print("Current Count:", currentCount)
    allItems |= survey
    newCount = len(allItems)
    print("New Count:", newCount)
    difference = newCount - currentCount
    print("Difference:", difference)
    cumulativeCount = newCount

print('-----------------------------')
print("Final count:", cumulativeCount)