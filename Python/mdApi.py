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
    
    def __limitValidation(self, limit: int, offset: int) -> bool:
        print("__makeTokenExpTime()")
        if limit > 100 or limit < 0:
            return False
        if offset < 0 or offset > 9999:
            return False
        return True
    
    def __parseOrder(self, order:dict) -> dict:
        orderQuery = {}
        for key, value in order.items():
            orderQuery[f"order[{key}]"] = value
        return orderQuery
    
    # authenticate user
    # Deprecated
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
    # Deprecated
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
    # Deprecated
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
    
    # Get users
    def userGet(self, limit = 100, offset = 0, userIds = [], username = "", order = {}):
        if not self.__limitValidation(limit, offset):
            raise ValueError("limit must be between 0 and 100. offset must be 0 or greater.")
        
        # Check if session needs to be refreshed first
        if self.__tokenExp < int(time.time()):
            self.authRefresh()
        
        # make url and headers
        url = f"{MdApi.baseUrl}/user"
        headers = {
			'accept':'application/json',
			'content-type':'application/json',
            'Authorization':f"Bearer {self.__token['session']}"
		}

        queryOrder = self.__parseOrder(order)

        parameters = {
            **{
                'limit':limit,
                'offset':offset,
                'ids[]':userIds,
                'username':username
            },
            **queryOrder
        }

        print(f"calling {url}\n{parameters}")
        response = requests.get(url=url,headers=headers,params=parameters)

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")

        return response.json()
    
    # Get users
    def userGetById(self, userId):
        # make url and headers
        url = f"{MdApi.baseUrl}/user{userId}"
        headers = {
			'accept':'application/json',
			'content-type':'application/json'
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

        print(f"calling {url}\n{parameters}")
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

        print(f"calling {url}\n{parameters}")
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

        print(f"calling {url}\n{parameters}")
        response = requests.get(url=url,headers=headers,params=parameters)

        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")

        return response.json()

    # change user password
    # Deprecated
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
    # Deprecated
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
    
    # get MD@H url
    def athomeServer(self, chapterId, force443=False):
        # make url and headers
        url = f"{MdApi.baseUrl}/at-home/server/{chapterId}"
        headers = {
			'accept':'application/json',
			'content-type':'application/json'
		}
        parameters = {
            'forcePort443' : force443
        }

        print(f"calling {url}\n{parameters}")
        response = requests.get(url=url,headers=headers,params=parameters)
    
        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")
        
        return response.json()

    # get chapter
    def chapterGet(self, chapterId):
        # make url and headers
        url = f"{MdApi.baseUrl}/chapter/{chapterId}"
        headers = {
			'accept':'application/json',
			'content-type':'application/json'
		}

        print(f"calling {url}")
        response = requests.get(url=url,headers=headers)
    
        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")
        
        return response.json()
    
    # get page
    def getPage(self, baseUrl, chapterHash: str, fileName:str, dataSaver = False ):
        qualityMode = 'dataSaver' if dataSaver else 'data'
        # make url and headers
        url = f"{baseUrl}/{qualityMode}/{chapterHash}/{fileName}"
        headers = {
			'accept':'application/json',
			'content-type':'application/json'
		}

        print(f"calling {url}")
        response = requests.get(url=url,headers=headers)
    
        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")
        
        return response.content

    # Create new title
    def mangaCreate(self):
        # Check if session needs to be refreshed first
        if self.__tokenExp < int(time.time()):
            self.authRefresh()
        
        # make url and headers
        url = f"{MdApi.baseUrl}/manga"
        headers = {
			'accept':'application/json',
			'content-type':'application/json',
            'Authorization':f"Bearer {self.__token['session']}"
		}

        print(f"calling {url}")

        raise NotImplementedError()

        response = requests.post(url=url,headers=headers,json={})
    
        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")
        
        return response.json()
    
    def mangaGet(self, titleId):
        # make url and headers
        url = f"{MdApi.baseUrl}/manga/{titleId}"
        headers = {
			'accept':'application/json',
			'content-type':'application/json'
		}

        print(f"calling {url}")
        response = requests.get(url=url,headers=headers)
    
        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")
        
        return response.json()

    def mangaFeed(self, titleId, limit = 100, offset = 0, translatedLanguage = [], originalLanguage = [], excludedOriginalLanguage = [],
                  contentRating=["safe", "suggestive", "erotica"], excludedGroups = [], includes = [], order = {}):
        if not self.__limitValidation(limit, offset):
            raise ValueError("limit must be between 0 and 100. offset must be 0 or greater.")
        # make url and headers
        url = f"{MdApi.baseUrl}/manga/{titleId}/feed"
        headers = {
			'accept':'application/json',
			'content-type':'application/json'
		}

        orderParams = self.__parseOrder(order)

        parameters = {
            **{
                'limit':limit,
                'offset':offset,
                'translatedLanguage[]': translatedLanguage,
                'originalLanguage[]': originalLanguage,
                'excludedOriginalLanguage[]': excludedOriginalLanguage,
                'excludedGroups[]': excludedGroups,
                'contentRating[]': contentRating,
                'includes[]': includes,
            }, 
            **orderParams
        }

        print(f"calling {url}\n{parameters}")
        response = requests.get(url=url,headers=headers,params=parameters)
    
        if not response.ok:
            raise requests.HTTPError(f"Error response returned. {response.status_code} {url}: {response.reason}")
        
        return response.json()
    
    def getToken(self):
        return self.__token
