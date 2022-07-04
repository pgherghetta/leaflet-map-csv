# To run this app type "python3 <file name>" in the terminal.
# import required module
import os
import csv
import folium


# assign directory
directory = 'Raw Sensor Data'
files = []
# Iterate over files in the "Raw Sensor Data" directory.
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # Check if f is a file.
    if os.path.isfile(f):
        print(f)
        files.append(f)

csvFilesRows = []
fileIndex = 1;
csvFileRowsIndex = 0;
while (fileIndex != len(files)):
    with open(files[fileIndex], 'r') as csv_file:
        csvFileRows = []
        count = 0;
        reader = csv.reader(csv_file)
        for row in reader:
            csvFileRows.append(row)
        csvFilesRows.append(csvFileRows)
    fileIndex += 1

anomalyStatusIndexPosition = 0
index = 0
# Find the index of where the anomaly status is located in a row.
for attribute in csvFileRows[0]:
    if attribute == "anomalyStatus":
        anomalyStatusIndexPosition = index
    index += 1

latitudeIndexPosition = 0
index = 0
# Find the index of where the latitude is located in a row.
for attribute in csvFileRows[0]:
    if attribute == "lat":
        latitudeIndexPosition = index
    index += 1

longitudeIndexPosition = 0
index = 0
# Find the index of where the longitude is located in a row.
for attribute in csvFileRows[0]:
    if attribute == "long":
        longitudeIndexPosition = index
    index += 1




# Iterate through the rows of the files to collect the anomaly status of 1 rows.
anomalyStatusOf1List = []
fileIndex = 1
for listOfRows in csvFilesRows:
    for i in range(1,len(listOfRows)):
        if i == 0:
            continue
        if listOfRows[i][anomalyStatusIndexPosition] == '1':
            # Add a tuple of necessary information
            anomalyStatusOf1List.append((listOfRows[i][latitudeIndexPosition], 
            listOfRows[i][longitudeIndexPosition], fileIndex, 1))
    fileIndex += 1

# At this point anomalyStatusOf1List has tuples of the form 
# (lat, long, file index, number of occurrences accross all files (not counting the .DS_Store file))

# This is a final list of tuples.
finalTupleList = []
finalTupleList.append(anomalyStatusOf1List[0])
appendCheck = 1
# Iterate through anomalyStatusOf1List to remove duplicate locations.
# finalTupleList will contain unique locations with the number of files they appeared in.
for i in range (0, len(anomalyStatusOf1List)):
    for j in range(0, len(finalTupleList)):
        # If the location is a duplicate location and it is located in the same file, 
        # DO NOT add the tuple.
        if (finalTupleList[j][0] == anomalyStatusOf1List[i][0]) and \
            (finalTupleList[j][1] == anomalyStatusOf1List[i][1]) and \
            (finalTupleList[j][2] == anomalyStatusOf1List[i][2]):
            continue
        # If the location is a duplicate location and it is located in a different file, 
        # DO NOT add the tuple BUT increment the file count by 1.
        elif (finalTupleList[j][0] == anomalyStatusOf1List[i][0]) and \
            (finalTupleList[j][1] == anomalyStatusOf1List[i][1]) and \
            (finalTupleList[j][2] != anomalyStatusOf1List[i][2]):
            finalTupleList[j][3] += 1
        # Otherwise, add the tuple to finalTupleList. The appendCheck is needed so that the
        # location is not added for multiple iterations of the j loop.
        else:
            if (appendCheck == 1):
                finalTupleList.append(anomalyStatusOf1List[i])
                appendCheck = 0;
    
    appendCheck = 1           

# At this point we have a list of unique locations that can put on a map.

# Declare a folium map.
m = folium.Map(location=[finalTupleList[0][0], finalTupleList[0][1]], zoom_start=12, tiles="Stamen Terrain")

# Add the locations in finalTupleList to the map as markers.
for i in range(0, len(finalTupleList)):
    folium.Marker(
        location=[finalTupleList[i][0], finalTupleList[i][1]],
        popup="Occurs in " + str(finalTupleList[i][3]) + " of the files.",
        icon=folium.Icon(icon="blue"),
    ).add_to(m)


# This command generates an html file for displaying the map.
# I think a new html file has to be generated each time so previous html files
# should be deleted.
m.save('map.html')





