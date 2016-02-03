import json
import geojson
import requests
import time
import os
import csv
from geopy import geocoders
from collections import defaultdict

currentDir = os.getcwd()
geoJSONDir = os.path.join(currentDir, 'outGeoJSON')
outFailedAddresses = os.path.join(currentDir, 'failedAddresses.csv')

g = geocoders.GoogleV3()

teamList =  ['ANA', 'BOS', 'BUF', 'CAR', 'CBJ', 'CGY', 'CHI', 'COL', 'DAL', 'DET', 'EDM', 'FLA', 'LAK',
   'MIN', 'MTL', 'NJD', 'NYR', 'OTT', 'PHI', 'PHX', 'PIT', 'SJS', 'STL', 'TBL', 'TOR', 'VAN',
   'WPG',  'WSH']

jsonLink = r'http://nhlwc.cdnak.neulion.com/fs1/nhl/league/teamroster/{0}/iphone/clubroster.json'

examplePlayerResponse = {u'birthplace': u'Ancienne-Lorette, QC, CAN', u'name': u'Patrice Bergeron', u'weight': 194, \
                         u'imageUrl': u'http://1.cdn.nhle.com/photos/mugs/8470638.jpg', u'number': 37, u'birthdate': u'July 24, 1985', \
                         u'height': u'6\' 2"', u'age': 29, u'position': u'Center', u'id': 8470638}

recursivedict = lambda: defaultdict(recursivedict)
placeDict_AllNHL = recursivedict()

def writeToGeoJSON(inPlaceDict, outFile):
    featList = []
    
    for placeKey, placeVals in inPlaceDict.iteritems():
        coords = geojson.Point((placeKey[1], placeKey[0]))
        propDict = {'placeName': placeVals['placeName']}

        playersList = []
        playerCount = 0
        
        for playerInfo in placeVals['players']:
            playerCount += 1
            playersList.append("{0}, {1}, {2}".format(playerInfo['name'], playerInfo['position'], playerInfo['team']))

        propDict['players'] = '<br>'.join(playersList)
        propDict['playerCount'] = playerCount
        
        featureStr = geojson.Feature(properties=propDict, geometry=coords)
        featList.append(featureStr)

    outFC = geojson.FeatureCollection(featList)

    geojson.dump(outFC, open(outFile,'wb'))


countryDict = {'LTU':'Lithuania', 'SVK': 'Slovakia', 'EST':'Estonia', 'FRA':'France', 'SVN':'Slovenia', 'ITA':'Italy', \
               'DNK':'Denmark', 'DEU':'Germany', 'SWE':'Sweden', 'HRV':'Croatia', 'CHE':'Switzerland', 'AUT':'Austria', \
               'LVA':'Latvia', 'KAZ':'Kazakhstan', 'BRN':'Bahrain', 'NOR':'Norway', 'CZE':'Czech Republic', 'BRA':'Brazil',\
               'FIN':'Finland', 'RUS':'Russia'}

with open(outFailedAddresses, 'wb') as failedCSV:
    csvWriter = csv.writer(failedCSV)
    
    for teamVal in teamList:
        placeDict = recursivedict()
        url = jsonLink.format(teamVal)
        resp = requests.get(url=url)
        data = json.loads(resp.text)

        for posType in ['forwards', 'goalie', 'defensemen']:
            for player in data[posType]:
                playerDict = {'name': player['name'], 'team': teamVal, 'position': player['position']}
                time.sleep(0.25)

                addressVal = player['birthplace']
                addressSplit = addressVal.split(',')

                if len(addressSplit) > 2:
                    if addressSplit[2] == ' CAN' or addressSplit[2] == ' USA':
                        addressVal = ','.join(addressSplit[0:2])
                    else:
                        pass
                elif len(addressSplit[1]) == 4:
                    countryAbbr = addressSplit[1].strip()
                    countryText = countryDict[countryAbbr]
                    addressVal = ', '.join([addressSplit[0], countryText])
                else:
                    csvWriter.writerow([addressVal.encode('utf-8', 'ignore')])

                try:
                    place, (lat, lng) = g.geocode(addressVal)
                    coords = (lat, lng)
                    print player['name'], addressVal, lat, lng

                except:
                    coords = (9999, 9999)

                if coords == (9999, 9999):
                    csvWriter.writerow([playerDict['name'], playerDict['position'], playerDict['team'], addressVal.encode('utf-8', 'ignore')])

                else:

                    try:
                        placeDict[coords]['players'].append(playerDict)

                    except:
                        placeDict[coords]['players'] = [playerDict]

                    try:
                        placeDict_AllNHL[coords]['players'].append(playerDict)
                        
                    except:
                        placeDict_AllNHL[coords]['players'] = [playerDict]

                    placeDict[coords]['placeName'] = addressVal
                    placeDict_AllNHL[coords]['placeName'] = addressVal

        outFilePath = os.path.join(geoJSONDir, '{0}.geojson'.format(teamVal))
        writeToGeoJSON(placeDict, outFilePath)
    
writeToGeoJSON(placeDict_AllNHL, os.path.join(geoJSONDir, 'All_NHL.geojson'))
