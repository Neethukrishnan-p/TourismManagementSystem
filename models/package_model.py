import datetime
from pydantic import BaseModel
from typing import List,Optional
from bson import ObjectId

class Packages(BaseModel):
    name:str
    description:str
    destination:List[str]
    amount:float
    availability:int
    start_date:datetime.datetime
    end_date:datetime.datetime

class PackageFilter(BaseModel):
    id:Optional[str|ObjectId] = None
    name: Optional[str]=None
    description: Optional[str]=None
    destination: Optional[List[str]]=None
    amount: Optional[float]=None
    availability: Optional[int]=None
    start_date: Optional[datetime.datetime]=None
    end_date: Optional[datetime.datetime]=None
    class Config:
        arbitrary_types_allowed=True
        json_schema_extra={"example":
                               {
                                   "id":"",
                                   "name":"",
                                   "description":"",
                                   "destination":[],
                                   "amount":"",
                                   "availability":"",
                                   "start_date":"",
                                   "end_date":""
                               }
        }



class RatedPackage(Packages):
    rating:float=0
    total_rating:list[float]=[]

