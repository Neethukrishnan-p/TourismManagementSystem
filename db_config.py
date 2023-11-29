import datetime

from pymongo import MongoClient


conn = MongoClient("mongodb://localhost:27017")

package = {
    "p_name":"Kerala Winter trip",
    "destination":["Munnar","Wagamon","Thekkady"],
    "description":"Experience the beauty and flavours of God's Own Country",
    "amount":5000,
    "start_date":"2023-11-23",
    "end_date":"2023-11-26",
    "rating":0,
    "availability":10
}

passenger = {
    "first_name":"Anjana",
    "last_name":"KT",
    "age":22,
    "phone_no":"9056467846",
    "email":"anjana@gmail.com",
    "place":"kochi",
    "package_id":"123",
    "status":"completed",
    "date_of_travel":datetime.datetime.now(),
    "rating":4
}


PACKAGE = conn["tourism"]["package"]
PASSENGER = conn["tourism"]["passenger"]


