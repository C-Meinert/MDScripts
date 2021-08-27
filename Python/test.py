import getpass
from mdApi import MdApi

try:
    api = MdApi()

    username = input("Enter username: ")
    password = getpass.getpass(prompt="Enter password: ")

    api.authLogin(username,password)

    temp = api.authCheck()
    print(temp)

    temp = api.userMe()
    print(temp)

    temp = api.userFollowsGroup()
    print(temp)

    api.authLogout()
except Exception as e:
    print(f"Stuff happens\n{e}")
finally:
    password = ""
    username = ""