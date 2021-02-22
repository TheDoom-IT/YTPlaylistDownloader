import requests
from pytube import YouTube
import os
import threading

def getVideosID(url, **kwargs):
    params = {**kwargs,'maxResults': 50, 'part':'contentDetails'}
    result = []

    while True:
        res = requests.get(url,params)
        #code 200 means that request was succesful
        if res.status_code != 200:
            print('API returned error:',res.status_code)
            return result

        data = res.json()
        #creating list of videos from obtained request
        videosID = [item['contentDetails']['videoId'] for item in data['items']]
        result.extend(videosID)
        
        #we can get up to 50 videos on one request
        #preparing next request if nextPageToken exists
        if 'nextPageToken' in data:
            params.update(pageToken = data['nextPageToken'])
        else:
            break
    return result

class LockedCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()
    def increase(self):
        with self.lock:
            self.count += 1
            return self.count
    def __str__(self):
        return str(self.count)

def downloadOne(videoUrl,counter):
    try:
        video = YouTube(videoUrl)
        video.streams.filter(mime_type="audio/webm").last().download()
        print(f'Downloaded {counter.increase()}.')
        return True
    except Exception as e:
        print(f'Unable to download file:', str(e))
        return False
    

def downloadVideos(videos):
    print(f'Downloading {len(videos)} videos...')

    #creating directiory for files
    if not os.path.isdir('Downloads'):
        os.mkdir('Downloads')
    os.chdir('Downloads')

    videoUrl = 'http://youtube.com/watch?v='

    counter = LockedCounter()
    
    threads = []
    
    for item in videos:
        while threading.active_count() > 12:
            pass

        p = threading.Thread(target = downloadOne, args = [videoUrl + item,counter,], daemon = True)
        p.start()
        threads.append(p)
        
    for thread in threads:
        thread.join(30)
    

    os.chdir('..')
    print(f'\nDone!\nDownloaded {counter}/{len(videos)}')


def convertOne(path,inputPath,outputPath, counter):
    os.system(path + ' -i "' + inputPath +'" "' + outputPath + '" -hide_banner -loglevel warning')
    print(f'Converted {counter.increase()}.')

def convertVideos():
    print('\nConverting...')

    path = os.path.join(os.getcwd(),'ffmpeg','bin','ffmpeg.exe')
    if not os.path.isdir('Converted'):
        os.mkdir('Converted')

    threads = []
    counter = LockedCounter()
    
    for video in os.listdir('Downloads'):
        inputPath = os.path.join(os.getcwd(),'Downloads',video)
        outputPath = os.path.join(os.getcwd(),'Converted',video.replace('.webm','.mp3'))

        while threading.active_count() > 10:
            pass
        p = threading.Thread(target = convertOne, args = [path,inputPath,outputPath,counter], daemon=True)
        p.start()
        threads.append(p)

    for thread in threads:
        thread.join(30)

    print(f'\nDone!\nConverted {counter} videos.')


if __name__ == '__main__':
    url = 'https://www.googleapis.com/youtube/v3/playlistItems?'
    with open('key.txt','rt') as file:
        key = file.read()
    
    
    playlistId = input('Enter ID of the playlist: ')

    videos = getVideosID(url,playlistId = playlistId,key = key)
    
    downloadVideos(videos)
    
    convertVideos()
    
    input('Press any button to close program...')


