import csv
import requests
import os.path

url = 'http://localhost:80/users/'

x = requests.get(url).json()                                # put the data into a json object

List = list()   # create a list

if not os.path.isfile('export.csv'):                        # if export file do not exist then we put the first row in the list 
    List.insert(0,["ID","FirstName", "LastName"])

for i in x:
    List.append([i['id'],i['firstName'],i['lastName']])     # put the data from json obj in the list with correct order

    
with open('export.csv', 'a', newline='') as csvfile:        # open the csv file as csvile which is a file-like obj
    writer = csv.writer(csvfile)                            # writer object responsible for converting our data into delimited strings on the given file-like obj
    writer.writerows(List)                                  # write the data from the list into csv file

    csvfile.close()                                         # close the file-like obj

print("Data exported successfully!")










