from urllib.parse import urlencode, urlparse
from string import Formatter
import pandas as pd

#TODO: init (from not setting correctly)
class Url:
    #parse string if init
    def __init__(self, base, base_params={}, params={}):
        self.__base = base
        self.__base_params = base_params
        self.__params = params

    #TODO: unnamed base_keys
    def __str__(self):        
        if isinstance(self.__base, str) == False:
            raise TypeError 
        
        out = str(self.__base.format(**self.__base_params))
        if len(self.__params) > 0:
            out += "?" + urlencode(self.__params)

        return out

    def keys(self):
        yield "source"
        yield "params"

    def __getitem__(self, key):
        if key == "source":
            url = str(self) 
            url = "//" + url if url.startswith("www.") else url #// for urlparse to get host without (netloc?) 
            return urlparse(url).hostname #host = .hostname, path = .path, query = .query, params = .params
        elif key == "params":
            return self.__base_params | self.__params
        else:
            raise KeyError("invalid key:", str(key))


    # def __repr__(self):
    #     return {
    #         "source" : urlparse(str(self)).hostname, #host = .hostname, path = .path, query = .query, params = .params
    #         "params" : self.__base_params | self.__params
    #     }
    #TODO
    
    def parse(str):
        return Url("https://www.google.de")
        

    @classmethod
    def from_file(path_to_file):
        output = pd.DataFrame()

        if path_to_file.endswith(".csv"):
            data = pd.read_csv(path_to_file)
        elif path_to_file.endswith(".json"):
            data = pd.read_json(path_to_file)
        else:
            raise Exception("unrecognized input type")

        if ("url" in data ) == False:
            data["url"] = ""
            
        #remove None?#

        output["url"] = output["url"].apply(lambda x: Url(x))
        
        output["keys"] = data.apply(lambda x: x in Url(x).keys(),  axis=1) 
        #data = [ x for x in data.to_dict("records") ]

        return data


    def base_param(self, key, value):
        self.__base_params[key] = value
        return self

    def param(self, key, value):
        self.__params[key] = value
        return self


    # def keys(self):
    #     return [ fname for _, fname, _, _ in Formatter().parse(self.__base) ], self.__params.keys()

    # def values(self):
    #     return [ x for x in self.__base_params.values() if x in self.keys()[0] ], self.__params.values()
