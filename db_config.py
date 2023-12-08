import datetime

from pymongo import MongoClient


conn = MongoClient("mongodb://localhost:27017")

PACKAGE = conn["tourism"]["package"]
PASSENGER = conn["tourism"]["passenger"]



