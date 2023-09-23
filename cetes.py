import datetime as dt
from typing import Optional

import pandas as pd
import requests

url_template = "https://www.banxico.org.mx/SieInternet/consultaSerieGrafica.do?s={serie}&versionSerie=LA-MAS-RECIENTE&l=es"

class Cetes:
    
    tags = {
        "28": "SF43936,CF107,5",
        "91": "SF43939,CF107,9",
        "182": "SF43942,CF107,13",
        "364": "SF43945,CF107,17"  
    }
    
    def __init__(self, tag: Optional[str]="28"):
        if tag not in self.tags.keys():
            raise ValueError(f"Tags must be one of the following: {list(self.tags.keys())}")
        self.tag = tag
        self.data = None
        
    @classmethod
    def c28(cls):
        return cls(tag="28")
    
    @classmethod
    def c91(cls):
        return cls(tag="91")
    
    @classmethod
    def c182(cls):
        return cls(tag="182")
    
    @classmethod
    def c364(cls):
        return cls(tag="364")
        
    @property
    def url(self) -> str:
        return url_template.format(serie=self.tags[self.tag])
    
    def is_cache_updated(self) -> bool: 
        if self.data is None:
            return False
        reference = dt.datetime.utcnow() - dt.timedelta(days=7)
        latest_timestamp = dt.datetime.strptime(self.data.date.max(), "%Y-%m-%d")
        return reference <= latest_timestamp
    
    @property
    def latest_rate(self) -> float:
        return self.get_historical_data().value.values[-1]
    
    @property
    def latest_date(self) -> dt.datetime:
        return dt.datetime.strptime(self.get_historical_data().date.values[-1], "%Y-%m-%d")
    
    def get_historical_data(self) -> pd.DataFrame:
        if self.is_cache_updated():
            return self.data
        response = requests.get(url = self.url)
        if not response.ok:
            raise ValueError("Response was not ok.")
        self.data = pd.DataFrame(response.json()["valores"], columns = ["date", "value"]).query("value != -989898.0").reset_index(drop=True)    
        
        return self.data
    
    def get_data(self, date_start: Optional[str] = None, date_end:  Optional[str] = None) -> pd.DataFrame:
        # Historical data
        data = self.get_historical_data()
        # Format dates 
        date_start = dt.datetime.strptime(date_start or self.data.date.min(), "%Y-%m-%d").strftime("%Y-%m-%d")
        date_end = dt.datetime.strptime(date_end or self.data.date.max(), "%Y-%m-%d").strftime("%Y-%m-%d")
        # Filter data
        return data.query(f"{repr(date_start)} <= date <= {repr(date_end)}").reset_index(drop=True)
