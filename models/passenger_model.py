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

    class Config:
        arbitrary_types_allowed = True

class Passenger_filter(BaseModel):
    id:Optional[str|ObjectId] = None
    first_name:Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    place: Optional[str]= None
    phone_no: Optional[str]= None
    email: Optional[str]= None
    package_id: str | ObjectId= None
    status: Optional[str]= None
    date_of_travel: Optional[datetime.datetime]= None

    class Config:
        arbitrary_types_allowed=True
        json_schema_extra = {"example":
                                 {
                                     "_id":"",
                                     "first_name":"",
                                     "last_name":"",
                                     "age":"",
                                     "place":"",
                                     "phone_no":"",
                                     "email":"",
                                     "package_id":"",
                                     "status":"",
                                     "date_of_travel":""
                                 }}

