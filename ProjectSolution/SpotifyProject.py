#import Spotipy
import ast
from typing import List
from os import listdir
import spotipy
import requests
import pandas as pd

def get_streamings(path: str = 'AData') -> List[dict]:
    
    files = ['AData/' + x for x in listdir(path)
             if x.split('.')[0][:-1] == 'StreamingHistory']
    
    all_streamings = []
    totalTimeByTrack = {}
    
    for file in files: 
        with open(file, 'r', encoding='UTF-8') as f:
            new_streamings = ast.literal_eval(f.read())
            for streaming in new_streamings:
                if streaming['trackName'] in totalTimeByTrack:
                    totalTimeByTrack[streaming['trackName']] += round(streaming['msPlayed']/60000)
                else:
                    totalTimeByTrack[streaming['trackName']] = round(streaming['msPlayed']/60000)
                all_streamings.append(streaming)
    return totalTimeByTrack
    

def get_id(track_name: str, token: str) -> str:
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer ' + token,
    }
    params = [
    ('q', track_name),
    ('type', 'track'),
    ]
    try:
        response = requests.get('https://api.spotify.com/v1/search', 
                    headers = headers, params = params, timeout = 5)
        json = response.json()
        first_result = json['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except:
        return None


def get_features(track_id: str, token: str) -> dict:
    sp = spotipy.Spotify(auth=token)
    try:
        features = sp.audio_features([track_id])
        return features[0]
    except:
        return None  
    
def trim_features(features: dict) -> dict:
    # TODO: Only grab certain features
    pass


#get_streamings()
    
username = 'qut9zcs5mbfdmc5cykwudcjtj'
client_id = '248c415c42004414acfa6cc8fe305bc3'
client_secret = 'acb2bbbec3184747b5851fa482419ade'
redirect_url = 'http://localhost:7777/callback'
scope = 'user-read-recently-played'

token = spotipy.util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_url)

streamings = get_streamings()
sortedListByStreamingTimes = sorted([x for x in streamings.values()])
topX = int(len(sortedListByStreamingTimes)*.5)
dataset = pd.DataFrame()

featureFinalValues = {}
for streamingName,timePlayed in streamings.items(): 
    if timePlayed < sortedListByStreamingTimes[topX]:
            continue
        
    ID = get_id(streamingName,token)
    
    # TODO: Make function to extract features we care about
    features = get_features(ID,token)
    
    # TODO: Grab genere
    
    # get averages for each value in feature_avgs
    for key,value in features.items():
        
        if key in featureFinalValues:
            featureFinalValues[key][0] += value*timePlayed
            featureFinalValues[key][1] += timePlayed
        else:
            featureFinalValues[key] = [value*timePlayed,timePlayed]
    
    
    # Associtae indexs
    bigFive = [50,50,50,50,50]
    
    
    

#print("Streamings:",streamings)
#print("\nID:",ID)
#print("\nfeatures",features)

# ID 1
# Dictionary where ID is the key
# the value will be a tuple
# two dictionaries
# Dict1 will have all a person songs that are in the top 75% of their listening.
# Keys for this dictioanry will be the song name and value will be a tuple of time listen to in total and the artist name


# ITF dictionary 2 od the tuple will be the quetion number ids and participant responses

