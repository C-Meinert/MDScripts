import getpass
import os
import time
from mdApi import MdApi

try:
    api = MdApi()
    mangaId = "c52b2ce3-7f95-469c-96b0-479524fb7a1a"
    mangaFeedData = api.mangaFeed(mangaId, translatedLanguage=["en"], order= {"volume": "desc", "chapter": "desc"})

    chapterIds = []
    for chapterInfo in mangaFeedData["data"]:
        # print(chapterInfo["attributes"]["externalUrl"])
        if(chapterInfo["attributes"]["externalUrl"] is None or not chapterInfo["attributes"]["externalUrl"]):
            chapterIds.append(chapterInfo["id"])

    print("Number of chapters found:", len(chapterIds))
    chapterData = api.chapterGet(chapterIds[0])
    serverData = api.athomeServer(chapterIds[0])

    folderPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Chapters", chapterIds[0])
    os.makedirs(folderPath, exist_ok=True)

    for page in serverData["chapter"]["data"]:
        print(page)
        pageData = api.getPage(serverData['baseUrl'],serverData["chapter"]["hash"],page)
        with open(f"{os.path.join(folderPath, page)}", "wb") as f:
            f.write(pageData)
        time.sleep(1)

    # username = input("Enter username: ")
    # password = getpass.getpass(prompt="Enter password: ")

    # api.authLogin(username,password)

    # temp = api.authCheck()
    # print(temp)

    # temp = api.userMe()
    # print(temp)

    # temp = api.userFollowsGroup()
    # print(temp)

    # api.authLogout()
except Exception as e:
    print(f"Stuff happens\n{e}")
finally:
    password = ""
    username = ""