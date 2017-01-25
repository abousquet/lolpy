import requests, json, time
from enum import Enum, unique
from urllib.parse import quote
class lolPy:

    @unique
    class Region(Enum):
        BR = "br"
        EUNE = "eune"
        EUW = "euw"
        JP = "jp"
        KR = "kr"
        LAN = "lan"
        LAS = "las"
        NA = "na"
        OCE = "oce"
        TR = "tr"
        RU = "ru"
        PBE = "pbe"

        _regionHostMap = {BR: "br.api.pvp.net",
                         EUNE: "eune.api.pvp.net",
                         EUW: "euw.api.pvp.net",
                         JP: "jp.api.pvp.net",
                         KR: "kr.api.pvp.net",
                         LAN: "lan.api.pvp.net",
                         LAS: "las.api.pvp.net",
                         NA: "na.api.pvp.net",
                         OCE: "oce.api.pvp.net",
                         TR: "tr.api.pvp.net",
                         RU: "ru.api.pvp.net",
                         PBE: "pbe.api.pvp.net",
                         "GLOBAL": "global.api.pvp.net"
                         }
        _platformIdMap = {BR: "BR1",
                         EUNE: "EUN1",
                         EUW: "EUW1",
                         JP: "JP1",
                         KR: "KR",
                         LAN: "LA1",
                         LAS: "LA2",
                         NA: "NA1",
                         OCE: "OC1",
                         TR: "TR1",
                         RU: "RU",
                         PBE: "PBE1"
                         }

        def __init__(self, region = NA):
            self.region = region

        def toRegionHost(self):
            return self._regionHostMap[self.region]
        def toPlatformId(self):
            return self._platformIdMap[self.region]

    def __init__(self, string = "", region = Region.NA ):
        assert type(string) == str, "Argument must be str"
        self.apiKey = string
        self.region = region
        self.tenSecCalls = 0
        self.tenMinCalls = 0

    def keyDefined(self):
        assert self.apiKey != "", "The api key is not defined"

    def getAPIKeyString(self):
        self.keyDefined()
        return "api_key="+self.apiKey

    @staticmethod
    def formatParameter(name , value):
        assert type(name) == str, "Parameter Name must be a string"
        return name + "=" + str(value).lower()

    def getDomainURL(self):
        return "https://" + self.region.value + ".api.pvp.net/"

    def _callAPI(self, apiURL ):
        response = requests.get(self.getDomainURL() + apiURL )
        if response.status_code == requests.codes.too_many_requests :
            time.sleep(int(response.headers.get('Retry-After', 0)))
            return self._callAPI(apiURL)
        else:
            response.raise_for_status()
            return response

    #champion v1.2
    def getChampionList(self,  freeToPlay = False):
        apiURL = "api/lol/"+self.region.value+"/v1.2/champion?" + self.formatParameter("freeToPlay", freeToPlay) \
            + "&" + self.getAPIKeyString()
        response = self._callAPI(apiURL)
        return json.loads(response.content.decode('utf-8'))
    def getChampionById(self, id ):
        apiURL = "api/lol/"+self.region.value+"/v1.2/champion/" + str(id) \
            + "?" + self.getAPIKeyString()
        response = self._callAPI(apiURL)
        return json.loads(response.content.decode('utf-8'))

    #game v1.3
    def getRecentGamesById(self, summonerId):
        apiURL = "api/lol/"+self.region.value+"/v1.3/game/by-summoner/" + str(summonerId) \
                 + "/recent?" + self.getAPIKeyString()
        response = self._callAPI(apiURL)
        return json.loads(response.content.decode('utf-8'))

    #summoner v1.4
    def getSummonerProfileByName(self, summonerName):
        if type(summonerName) == list:
            summonerName = ','.join(requests.utils.quote(str(x)) for x in summonerName)
        else:
            summonerName =  requests.utils.quote(str(summonerName))
        apiURL = "/api/lol/" + self.region.value + "/v1.4/summoner/by-name/" \
                 + summonerName + "?" + self.getAPIKeyString()
        response = self._callAPI(apiURL)
        return json.loads(response.content.decode('utf-8'))
    def getSummonerProfileById(self, summonerId):
        if type(summonerId) == list:
            summonerId = ','.join(requests.utils.quote(str(x)) for x in summonerId)
        else:
            summonerId =  requests.utils.quote(str(summonerId))
        apiURL = "/api/lol/" + self.region.value + "/v1.4/summoner/" \
                 + requests.utils.quote(str(summonerId)) + "?" + self.getAPIKeyString()
        response = self._callAPI(apiURL)
        return json.loads(response.content.decode('utf-8'))
    def getSummonerNameById(self, summonerId):
        if type(summonerId) == list:
            summonerId = ','.join(requests.utils.quote(str(x)) for x in summonerId)
        else:
            summonerId =  requests.utils.quote(str(summonerId))
        apiURL = "/api/lol/" + self.region.value + "/v1.4/summoner/" \
                 + requests.utils.quote(str(summonerId)) + "/name?" + self.getAPIKeyString()
        response = self._callAPI(apiURL)
        return json.loads(response.content.decode('utf-8'))