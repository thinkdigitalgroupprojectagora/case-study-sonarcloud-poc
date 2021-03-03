import csv
import requests


url = 'http://localhost:80/users/'


with open('input.csv', newline='') as csvfile:                      # open the csv file as csvfile which is a file-like obj
    reader = csv.reader(csvfile, delimiter=',')                     # read from csv file-like obj
    
    for row in reader:
       
        temp = {"firstName": row[0], "lastName": row[1]}            # create a json-like obj/dictionary
        x = requests.post(url, json = temp)                         # send the data to our app
        #print(x.text)


print("Data imported successfully!")