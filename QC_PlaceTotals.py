import json
import requests

teamList =  ['ANA', 'BOS', 'BUF', 'CAR', 'CBJ', 'CGY', 'CHI', 'COL', 'DAL', 'DET', 'EDM', 'FLA', 'LAK',
   'MIN', 'MTL', 'NJD', 'NYR', 'OTT', 'PHI', 'PHX', 'PIT', 'SJS', 'STL', 'TBL', 'TOR', 'VAN',
   'WPG',  'WSH']

##teamList = ['NJD']

jsonLink = r'http://nhlwc.cdnak.neulion.com/fs1/nhl/league/teamroster/{0}/iphone/clubroster.json'

countryDict = {'LTU':'Lithuania', 'SVK': 'Slovakia', 'EST':'Estonia', 'FRA':'France', 'SVN':'Slovenia', 'ITA':'Italy', \
               'DNK':'Denmark', 'DEU':'Germany', 'SWE':'Sweden', 'HRV':'Croatia', 'CHE':'Switzerland', 'AUT':'Austria', \
               'LVA':'Latvia', 'KAZ':'Kazakhstan', 'BRN':'Bahrain', 'NOR':'Norway', 'CZE':'Czech Republic', 'BRA':'Brazil',\
               'FIN':'Finland', 'RUS':'Russia'}

playerCount = 0
placeDict = {}

for teamVal in teamList:
    url = jsonLink.format(teamVal)
    resp = requests.get(url=url)
    data = json.loads(resp.text)

    for posType in ['forwards', 'goalie', 'defensemen']:
        for player in data[posType]:
            playerCount += 1
            playerDict = {'name': player['name'], 'team': teamVal, 'position': player['position']}

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
                print addressVal.encode('utf-8', 'ignore')

            try:
                placeDict[addressVal] = placeDict[addressVal] + 1
            except:
                placeDict[addressVal] = 1
                

print playerCount