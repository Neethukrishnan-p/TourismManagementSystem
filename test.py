import datetime

from db_config import PACKAGE,PASSENGER
from bson import ObjectId
packages = [{
    "name":"Kerala Winter trip",
    "destination":["Munnar","Wagamon","Thekkady"],
    "description":"Experience the beauty and flavours of God's Own Country",
    "amount":5000,
    "start_date":datetime.datetime(2023,12,6,12,10,31),
    "end_date":datetime.datetime(2023,12,8,12,10,31),
    "availability":9,
    "rating":0,
    "total_rating":[]
},
    {
    "name":"South India trip",
    "destination":["Kerala","Tamilnadu","Hyderabad","Karnataka"],
    "description":"Experience the beauty and flavours of states",
    "amount":8000,
    "start_date":datetime.datetime(2023,12,7,12,10,31),
    "end_date":datetime.datetime(2023,12,15,12,10,31),
    "availability":8,
    "rating":0,
    "total_rating":[],
    },
{
    "name":"All India trip",
    "destination":["Rajasthan","Kerala","Hyderabad","Kashmir"],
    "description":"Experience the beauty and flavours of India",
    "amount":20000,
    "start_date":datetime.datetime(2023,12,10,12,10,31),
    "end_date":datetime.datetime(2023,12,20,12,10,31),
    "availability":8,
    "rating":0,
    "total_rating":[],
},
    {
    "name":"Kashmir Trip",
    "destination":["Sri nagar","Pahalgam","Sonamarg"],
    "description":"Experience the beauty and flavours of India",
    "amount":10000,
    "start_date":datetime.datetime(2023,12,16,12,10,31),
    "end_date":datetime.datetime(2023,12,25,12,10,31),
    "availability":8,
    "rating":0,
    "total_rating":[],
    }
]


PACKAGE.insert_many(packages)



passengers =[ {
    "first_name":"Anjana",
    "last_name":"KT",
    "age":22,
    "phone_no":"9056467846",
    "email":"anjana@gmail.com",
    "place":"kochi",
    "package_id":"",
    "status":"completed",
    "date_of_travel":datetime.datetime(2023,12,6,12,10,31),
    "rating":0,
    "package_name":"Kerala Winter trip"
},
    {
    "first_name":"Ashish",
    "last_name":"Nair",
    "age":25,
    "phone_no":"9056463467",
    "email":"ashish@gmail.com",
    "place":"Delhi",
    "package_id":"",
    "status":"Completed",
    "date_of_travel":datetime.datetime(2023,12,7,12,10,31),
    "rating":0,
    "package_name":"South India trip"
    },
    {
    "first_name":"Nashith",
    "last_name":"KP",
    "age":30,
    "phone_no":"9056432465",
    "email":"nashith@gmail.com",
    "place":"Thrissur",
    "package_id":"",
    "status":"Travelling",
    "date_of_travel":datetime.datetime(2023,12,10,12,10,31),
    "rating":0,
    "package_name":"All India trip"
    },
    {
    "first_name":"Fiego",
    "last_name":"KP",
    "age":30,
    "phone_no":"9056432465",
    "email":"fiego@gmail.com",
    "place":"Thrissur",
    "package_id":"",
    "status":"Prior",
    "date_of_travel":datetime.datetime(2023,12,20,12,10,31),
    "rating":0,
    "package_name":"Kashmir Trip"
    }
]

for document in passengers:
    res = PACKAGE.find_one({"name":document["package_name"]})
    document["package_id"] = res["_id"]
    PASSENGER.insert_one(document)


