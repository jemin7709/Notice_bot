import requests
import bs4
import datetime
import time


def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer "+token},
                             data={"channel": channel, "text": text}
                             )


def checkNotice(link, day, Type):
    response = requests.get(link)
    html = response.text

    if day.month < 10:
        if day.day < 10:
            today = str(day.year) + ".0" + str(day.month) + \
                ".0" + str(day.day) + "."
        elif day.day >= 10:
            today = str(day.year) + ".0" + str(day.month) + \
                "." + str(day.day) + "."
    elif day.month >= 10:
        if day.day < 10:
            today = str(day.year) + "." + str(day.month) + \
                ".0" + str(day.day) + "."
        elif day.day >= 10:
            today = str(day.year) + "." + str(day.month) + \
                "." + str(day.day) + "."
    if Type == "Cse":
        today = today[:-1]

    bs = bs4.BeautifulSoup(html, 'html.parser')
    tr = bs.find_all("tr")

    if Type == "Inha":
        message = "`" + today + " 전체 공지사항`"
    elif Type == "Cse":
        message = "`" + today + " 컴퓨터공학과 공지사항`"
    post_message(myToken, "#학교-공지", message)
    # print(message)

    for elem1 in tr:
        if str(elem1.get("class")) != "['headline']":
            tdDay = elem1.find_all("td", {"class": "_artclTdRdate"})
            for elem2 in tdDay:
                if elem2.get_text() == today:
                    tdTitle = elem1.find("td", {"class": "_artclTdTitle"})
                    title = tdTitle.find("a")

                    message = title.get_text().strip()
                    message = message.replace("새글", '')
                    post_message(myToken, "#학교-공지", message)
                    # print(message)

                    if Type == "Inha":
                        message = "https://www.inha.ac.kr" + title.get("href")
                    elif Type == "Cse":
                        message = "https://cse.inha.ac.kr" + title.get("href")
                    post_message(myToken, "#학교-공지", message)
                    # print(message)

                
while True:
    try:
        myToken = ""
        linkInha = "https://www.inha.ac.kr/kr/950/subview.do"
        linkCse = "https://cse.inha.ac.kr/cse/888/subview.do"
    
        day = datetime.datetime.now()
        start_time = day.replace(hour=20, minute=0, second=0, microsecond=0)
        end_time = day.replace(hour=21, minute=0, second=0, microsecond=0)
        if start_time < cur_time < end_time:
            checkNotice(linkInha, day, "Inha")
            checkNotice(linkCse, day, "Cse")
        time.sleep(3600)
    except Exception as e:
        # print(e)
        post_message(myToken, "#공지봇-에러로그", e)
        time.sleep(3600)
