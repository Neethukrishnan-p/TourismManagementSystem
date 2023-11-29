import datetime
from pydantic import BaseModel
from typing import List,Optional


class Packages(BaseModel):
    p_name:str
    description:str
    destination:List[str]
    amount:float
    rating:Optional[List[float]]=None
    availability:int
    start_date:datetime.datetime
    end_date:datetime.datetime

class PackageFilter(BaseModel):
    p_name: Optional[str]=None
    description: Optional[str]=None
    destination: Optional[List[str]]=None
    amount: Optional[float]=None
    rating: Optional[List[float]] = None
    availability: Optional[int]=None
    start_date: Optional[datetime.datetime]=None
    end_date: Optional[datetime.datetime]=None

