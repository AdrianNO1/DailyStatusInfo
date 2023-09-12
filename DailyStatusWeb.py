getemails = False

import os, time, sys, json, datetime, webbrowser, subprocess
from getNewYTVids import checkChannels
from getGmailFlags import get_unread_emails


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

def open_txt_with(text):
    with open("DailyStatusViewer.txt", "w", encoding="utf-8") as f:
        f.write(text)
    os.startfile("DailyStatusViewer.txt")

def errorProtocol(e):
    import sys
    exc_type, exc_obj, exc_tb = sys.exc_info()[:]
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    basic_err_info = f"Error: {exc_type}\nFile: {fname}\nLine: {exc_tb.tb_lineno}"
    open_txt_with(f"HELLO! THERE WAS A PROBLEM RUNNING DAILYSTATUSINFO, PLEASE OPEN AN ISSUE ON THE GITHUB WITH THE FOLLOWING INFORMATION\n\n{e}\n{basic_err_info}\n\n\nLOCALS (no idea if this is useful or not): {str(locals())}\nGLOBALS (cant hurt to make the error file look cool): {str(globals())}\n{time.time()}")
    sys.exit()

def get_things(date, things, raw=False):
    current_date = date
    retuned = []
    for v in things:
        if v == "\n" or len(str(v)) == 0:
            continue

        if str(v)[2] == "#":
            continue

        if len(v) == 2:
                new_current_date = current_date[::]
                new_current_date.pop(-1)
                new_current_date = ".".join(new_current_date)
                if v[0] == new_current_date:
                    if raw:
                        retuned.append("\n" + " : ".join(v[0:2]).replace("\n", "") + " har bursdag!!\n")
                    else:
                        retuned.append("\n" + v[1].replace("\n", "") + " har bursdag!!\n")

        else:
            if v[0] == "OD":
                new_current_date = current_date[::]
                new_current_date.pop(-1)
                new_current_date = ".".join(new_current_date)
                if v[1] == new_current_date:
                    if raw:
                        retuned.append(" : ".join(v[1:3]).replace("\n", ""))
                    else:
                        retuned.append(v[2].replace("\n", ""))

            elif v[0] == "FD":
                new_current_date = current_date[::]
                new_current_date = ".".join(current_date)
                if v[1] == new_current_date:
                    if raw:
                        retuned.append(" : ".join(v[1:3]).replace("\n", ""))
                    else:
                        retuned.append(v[2].replace("\n", ""))
    return retuned


files_opened = []
things = []
quotes = []

nonUniversalThings = []

with open("DailyStatusMotivationalQuotes.txt", "r", encoding="utf8") as f:
    for v in f.readlines():
        if v != "\n":
            quotes.append(v.replace("\n", ""))

with open("DailyStatusInfo.txt", "r", encoding="utf8") as f:
    for v in f.readlines():
        things.append(v.split(" : "))
        nonUniversalThings.append(v.split(" : "))

with open("UniversalDates.txt", "r", encoding="utf8") as f:
    for v in f.readlines():
        things.append(v.split(" : "))

with open("Birthdays.txt", "r", encoding="utf8") as f:
    for v in f.readlines():
        things.append(v.split(" : "))
        nonUniversalThings.append(v.split(" : "))

#print(things)
#int("a")

def create_data_json(events, new_videos, emails, current_date):
    data = {
        "date": ".".join(current_date),
        "events": events,
        "new_videos": new_videos,
        "emails": emails
    }

    with open(os.path.join(dir_path, os.path.abspath(r"web\data.json")), 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    try:  
        current_date = str(datetime.datetime.now().date())
        current_date = current_date.split("-")
        current_date = current_date[::-1]

        events_data = []
        for day in range(31): # 31 days
            if day <= 14: # 2 weeks
                things2 = get_things(str(datetime.date.today() + datetime.timedelta(days=day)).split("-")[::-1], things, raw=True)
            else:
                things2 = get_things(str(datetime.date.today() + datetime.timedelta(days=day)).split("-")[::-1], nonUniversalThings, raw=True)
            for thing in things2:
                thing = thing.strip("\n")
                events_data.append({"name": " : ".join(thing.split(" : ")[1:]), "date": thing.split(" : ")[0] + "." + str(datetime.datetime.now().year)})

        new_videos = checkChannels()
        if getemails:
            try:
                unread_emails = get_unread_emails()
            except:
                os.remove("token.pickle")
                input("HELLO! PLEASE PRESS ENTER TO DO VERIFICATION STUFF")
                unread_emails = get_unread_emails()
        else:
            unread_emails = []

        new_videos_data = [{"title": video.split("\n")[0], "url": video.split("\n")[1]} for video in new_videos]
        emails_data = [{"sender": email.split(": ")[0], "email": email.split(": ")[1].split("\n")[0][:-1], "url": email.split("\n")[1]} for email in unread_emails]
        for v in emails_data:
            print(v)
        create_data_json(events_data, new_videos_data, emails_data, current_date)

        a = os.path.abspath(r'web\app.py')
        process = subprocess.Popen(f'python "{a}"', shell=True, stdout=sys.stdout, stderr=sys.stderr)

        with open(r"web\app.py", "r") as f:
            content = f.read()
            port = int(content.split("port=")[-1].split(")")[0])
        webbrowser.open(f"http://127.0.0.1:{port}/")
        time.sleep(4)
        process.terminate()

    except Exception as e:
        errorProtocol(e)

if __name__ == "__main__":
    main()