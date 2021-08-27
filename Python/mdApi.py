import requests
import time
from datetime import datetime, timedelta

class MdApi:
    baseUrl = "https://api.mangadex.org"

    def __init__(self):
        self.__token = None
        self.__tokenExp = None
        self.__refreshTokenAfterInMins = 14
    
    # create timestamp of when session tokens should be refreshed 
    def __makeTokenExpTime(self) -> int:
        print("__makeTokenExpTime()")
        expTime = datetime.today() + timedelta(minutes=self.__refreshTokenAfterInMins)
        unixtime = time.mktime(expTime.timetuple())
        return int(unixtime)
    
    # authenticate user
    def authLogin(self, username, password) -> None:
        # make url and headers
        url = f"{MdApi.baseUrl}/auth/login"
        headers = {
			'accept':'application/json',
			'content-type':'application/json'
		}

        print(f"calling {url}")
        response = requests.post(url=url,headers=headers,json={"username": username,"password":password})

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")
        
        self.__tokenExp = self.__makeTokenExpTime()
        self.__token = response.json()["token"]
    
    # end user session
    def authLogout(self) -> None:
        # Check if session needs to be refreshed first
        if self.__tokenExp < int(time.time()):
            self.authRefresh()
        
        # make url and headers
        url = f"{MdApi.baseUrl}/auth/logout"
        headers = {
			'accept':'application/json',
			'content-type':'application/json',
            'Authorization':f"Bearer {self.__token['session']}"
		}

        print(f"calling {url}")
        response = requests.post(url=url,headers=headers)

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")
        
        self.__token = None

    # Refresh user session
    def authRefresh(self) -> None:
        # make url and headers
        url = f"{MdApi.baseUrl}/auth/refresh"
        headers = {
			'accept':'application/json',
			'content-type':'application/json'
		}

        print(f"calling {url}")
        response = requests.post(url=url,headers=headers,json={"token": self.__token['refresh']})

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")
        
        self.__tokenExp = self.__makeTokenExpTime()
        self.__token = response.json()["token"]
    
    # check token
    def authCheck(self):
        # Check if session needs to be refreshed first
        if self.__tokenExp < int(time.time()):
            self.authRefresh()
        
        # make url and headers
        url = f"{MdApi.baseUrl}/auth/check"
        headers = {
			'accept':'application/json',
			'content-type':'application/json',
            'Authorization':f"Bearer {self.__token['session']}"
		}

        print(f"calling {url}")
        response = requests.get(url=url,headers=headers)

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")
        
        return response.json()

    def userMe(self):
        # Check if session needs to be refreshed first
        if self.__tokenExp < int(time.time()):
            self.authRefresh()
        
        # make url and headers
        url = f"{MdApi.baseUrl}/user/me"
        headers = {
			'accept':'application/json',
			'content-type':'application/json',
            'Authorization':f"Bearer {self.__token['session']}"
		}

        print(f"calling {url}")
        response = requests.get(url=url,headers=headers)

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")

        return response.json()
    
    def userFollowsManga(self, limit = 100, offset = 0):
        if limit > 100:
            limit = 100
        elif limit < 0:
            limit = 0
        
        if offset < 0:
            offset = 0

        # Check if session needs to be refreshed first
        if self.__tokenExp < int(time.time()):
            self.authRefresh()
        
        # make url and headers
        url = f"{MdApi.baseUrl}/user/follows/manga"
        headers = {
			'accept':'application/json',
			'content-type':'application/json',
            'Authorization':f"Bearer {self.__token['session']}"
		}
        parameters = {
            'limit':limit,
            'offset':offset
        }

        print(f"calling {url}")
        response = requests.get(url=url,headers=headers,params=parameters)

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")

        return response.json()

    def userFollowsGroup(self, limit = 100, offset = 0):
        if limit > 100:
            limit = 100
        elif limit < 0:
            limit = 0
        
        if offset < 0:
            offset = 0

        # Check if session needs to be refreshed first
        if self.__tokenExp < int(time.time()):
            self.authRefresh()
        
        # make url and headers
        url = f"{MdApi.baseUrl}/user/follows/group"
        headers = {
			'accept':'application/json',
			'content-type':'application/json',
            'Authorization':f"Bearer {self.__token['session']}"
		}
        parameters = {
            'limit':limit,
            'offset':offset
        }

        print(f"calling {url}")
        response = requests.get(url=url,headers=headers,params=parameters)

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")

        return response.json()
    
    def userFollowsUser(self, limit = 100, offset = 0):
        if limit > 100:
            limit = 100
        elif limit < 0:
            limit = 0
        
        if offset < 0:
            offset = 0

        # Check if session needs to be refreshed first
        if self.__tokenExp < int(time.time()):
            self.authRefresh()
        
        # make url and headers
        url = f"{MdApi.baseUrl}/user/follows/user"
        headers = {
			'accept':'application/json',
			'content-type':'application/json',
            'Authorization':f"Bearer {self.__token['session']}"
		}
        parameters = {
            'limit':limit,
            'offset':offset
        }

        print(f"calling {url}")
        response = requests.get(url=url,headers=headers,params=parameters)

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")

        return response.json()
        
    
    def getToken(self):
        return self.__token