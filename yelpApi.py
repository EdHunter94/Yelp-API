from yelpapi import yelpapi"
import requests
import pandas as pd
import csv
from collections import Counter

names = []
distance = []
addressInfo = []
address = []
prices = []
apiKey = "pfk6A-vauPgGp6FbNmXfJTOmdGlUs5S8SsAxPLdmy_L5Fp9F5R_xje3k2gGrGphweh3GklOnJf7x6KDqPRbOuOc1bt14oMrrD7ttXBLdWR0l9sK3QFlU9UjIk73cYHYx"
endpoint = "https://api.yelp.com/v3/businesses/search"



def search(term):

    """You can set the address to where ever you want"""
    parameters = {"term" : term, "location" : "550 W Van Buren St Chicago, IL", "radius" : 24140}

    header = {"Authorization" : "bearer " + apiKey}

    results = requests.get(url = endpoint, params = parameters, headers = header)


    for i in results.json()["businesses"]:
        names.append(i["name"])

    for i in results.json()["businesses"]:
        distance.append(int(i["distance"]))

    j = 0
    for i in results.json()["businesses"]:
        addressInfo.append(i["location"])
        address.append(addressInfo[j].get("address1"))
        j += 1



    data = {"Name" : names, "Distance" : distance, "Address" : address}

    df = pd.DataFrame(data, columns = ["Name", "Distance", "Address"])
    print(df)

    createCsv()

def createCsv():
    """You'll need to update this with your own file path"""
    with open("C:/Users/edhnt/Documents/Work/Python for work/Huron/output_yelp_japanese_data.csv", "w", newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Distance", "Address"])
        for i in range(0, len(names)):
            writer.writerow([names[i], distance[i], address[i]])

def searchWithLatLong(term, lat, long):
    names = []
    distance = []

    parameters = {"term" : term, "latitude" : lat, "longitude" : long, "radius" : 16093}

    header = {"Authorization" : "bearer " + apiKey}

    results = requests.get(url = endpoint, params = parameters, headers = header)


    for i in results.json()["businesses"]:
        names.append(i["name"])

    for i in results.json()["businesses"]:
        distance.append(int(i["distance"]))

    j = 0
    for i in results.json()["businesses"]:
        addressInfo.append(i["location"])
        address.append(addressInfo[j].get("address1"))
        j += 1

    data = {"Name" : names, "Distance" : distance, "Address" : address}

    df = pd.DataFrame(data, columns = ["Name", "Distance", "Address"])
    print(df)

def topZipCodes(term, location):
    parameters = {"term" : term, "location" : location}

    header = {"Authorization" : "bearer " + apiKey}

    results = requests.get(url = endpoint, params = parameters, headers = header)

    zips = []

    for i in results.json()["businesses"]:
        names.append(i["name"])

    for i in results.json()["businesses"]:
        dict = i["location"]
        zips.append(dict.get("zip_code"))

    topZips = findThreeMostCommon(zips)

    topZipLst = [topZips[0][0], topZips[1][0], topZips[2][0]]
    zipCounts = [topZips[0][1], topZips[1][1], topZips[2][1]]

    data = {"Zip Codes" : topZipLst, "Frequency" : zipCounts}

    df = pd.DataFrame(data, columns = ["Zip Codes", "Frequency"])
    print(df)

def findThreeMostCommon(ls):
    data = Counter(ls)
    return data.most_common(3)
