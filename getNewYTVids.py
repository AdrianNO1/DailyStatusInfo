from urllib.request import Request, urlopen
import json, datetime
from browser_history import get_history
import sys, os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

def checkChannels():

    printformatting = { # if a youtuber dont have their own subdirectory on socialblade, you can add it here together with their actual channel name
        "UCNJ1Ymd5yFuUPtn21xtRbbw": "AI Explained"
    }

    history = [x[1] for x in get_history().histories[-1000:]]

    newvids = []

    def get_last_video(socialbladelink):
        req = Request(
            url=socialbladelink, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        webpage = str(urlopen(req).read())

        start = '"youtube-video-embed-recent" id = "'
        url = webpage[webpage.find(start)+len(start):]
        return "https://www.youtube.com/watch?v=" + url[:url.find('"')]

    links = list(filter(lambda x: x != "\n" and len(x) != 0, open("YTflags.txt", "r").read().split("\n")))

    try:
        data = json.loads(open("lastYTvids.json", "r").read())
    except Exception as e:
        if type(e) == json.decoder.JSONDecodeError:
            data = {}
    try:
        today = json.loads(open("lastYTvidsToday.json", "r").read())
    except Exception as e:
        if type(e) == json.decoder.JSONDecodeError:
            today = {"date": str(datetime.date.today())}

    if today["date"] != str(datetime.date.today()):
        for key in today:
            data[key] = today[key]

    for link in links:
        print("searching link", link)

        lastvid = get_last_video(link)

        index = link.split("/")[-1]

        if (not index in today or lastvid != today[index]) and (not index in data or lastvid != data[index]):
            if today["date"] == str(datetime.date.today()):
                today[index] = lastvid
                if not lastvid in history:
                    if index in printformatting:
                        printingindex = printformatting[index]
                    else:
                        printingindex = index
                    newvids.append(f'new {printingindex} video!\n{today[index]}')
        
        elif index in today and today["date"] == str(datetime.date.today()):
            if not lastvid in history:
                if index in printformatting:
                    printingindex = printformatting[index]
                else:
                    printingindex = index
                newvids.append(f'new {printingindex} video!\n{today[index]}')

        if today["date"] != str(datetime.date.today()):
            today = {"date": str(datetime.date.today())}

        with open("lastYTvids.json", "w") as f:
            f.write(json.dumps(data))
        with open("lastYTvidsToday.json", "w") as f:
            f.write(json.dumps(today))
    
    return newvids

if __name__ == "__main__":
    print("\n\n", checkChannels())