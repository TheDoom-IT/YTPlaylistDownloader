# Why?
---
I recently started learning Python(early 2021). As a summary of learning I created Python application.
In the past I spent so much time on downloading YouTube's videos manually. Now I only have to create YouTube playlist. It saves me a lot of time 😊
### Necessary technologies
---
* [ffmpeg](https://ffmpeg.org) - 2021-02-13-git-d5d6751a55-essentials_build-www.gyan.dev revision
* pytube - 10.5.0
* requests - 2.25.1
* [YouTube API](https://developers.google.com/youtube/v3)

### How to use
---
Install python packages:
```
pip install pytube
pip install requests
```

Download ffmpeg and put it to the folder with application.
Get YouTube API key and put it into **key.txt** file.
### How it works
---
The application, using YouTube API, gets URLs of the videos on the playlist and then downloads them using pytube.
