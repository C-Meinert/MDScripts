import getpass
import json
from mdApi import MdApi

try:
    api = MdApi()

    chapterId = '478a3742-b70a-4f4c-892b-b9b1b6ad4fb1'
    chapterData = api.chapterGet(chapterId)
    serverData = api.athomeServer(chapterId,0)

    page = api.getPage(serverData['baseUrl'],'data',((chapterData['data'])['attributes'])['hash'],(((chapterData['data'])['attributes'])['data'])[0])

    open(f"../{(((chapterData['data'])['attributes'])['data'])[0]}",'wb').write(page)

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