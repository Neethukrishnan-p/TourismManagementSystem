import datetime
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Passenger(BaseModel):
    first_name:str
    last_name:str
    age:int
    place:str
    phone_no:str
    email:str
    package_id:str|ObjectId
    status:str
    date_of_travel:datetime.datetime
    rating:Optional[float]=None

    class Config:
        arbitrary_types_allowed = True