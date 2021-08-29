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
    
    def __limitValidation(self, limit, offset) -> bool:
        print("__makeTokenExpTime()")
        if limit > 100 or limit < 0:
            return False
        if offset < 0:
            return False
        return True
    
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

    # get users profile
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
    
    # get list of followed manga
    def userFollowsManga(self, limit = 100, offset = 0):
        if not self.__limitValidation(limit, offset):
            raise ValueError("limit must be between 0 and 100. offset must be 0 or greater.")

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

    # get list of followed groups
    def userFollowsGroup(self, limit = 100, offset = 0):
        if not self.__limitValidation(limit, offset):
            raise ValueError("limit must be between 0 and 100. offset must be 0 or greater.")

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
    
    # get list of followed users
    def userFollowsUser(self, limit = 100, offset = 0):
        if not self.__limitValidation(limit, offset):
            raise ValueError("limit must be between 0 and 100. offset must be 0 or greater.")

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

    # change user password
    def userPassword(self, password, newPassword) -> None:
        # Check if session needs to be refreshed first
        if self.__tokenExp < int(time.time()):
            self.authRefresh()
        
        # make url and headers
        url = f"{MdApi.baseUrl}/user/password"
        headers = {
			'accept':'application/json',
			'content-type':'application/json',
            'Authorization':f"Bearer {self.__token['session']}"
		}

        print(f"calling {url}")
        response = requests.post(url=url,headers=headers,json={'oldPassword':password,'newPassword':newPassword})

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")

    # change user email
    def userEmail(self, newEmail) -> None:
        # Check if session needs to be refreshed first
        if self.__tokenExp < int(time.time()):
            self.authRefresh()
        
        # make url and headers
        url = f"{MdApi.baseUrl}/user/password"
        headers = {
			'accept':'application/json',
			'content-type':'application/json',
            'Authorization':f"Bearer {self.__token['session']}"
		}

        print(f"calling {url}")
        response = requests.post(url=url,headers=headers,json={'email':newEmail})

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")
        
    
    def getToken(self):
        return self.__token