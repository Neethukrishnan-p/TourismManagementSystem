from fastapi import APIRouter,Body
from db_config import PACKAGE
from bson import ObjectId
from models.package_model import Packages,PackageFilter,RatedPackage
from typing import Annotated

package = APIRouter()

@package.post('/create/',description="Adding packages")
async def create_packages(package:Packages):
    package = RatedPackage(**package.model_dump())
    PACKAGE.insert_one(package.model_dump())
    return {"data":"package data has been created"}

@package.put('/',description="Updating the details")
async def update_package_details(package_filter:PackageFilter,doc_id:str=Body(...)):
    PACKAGE.update_one({"_id":ObjectId(doc_id)},{"$set":package_filter.model_dump(exclude_unset=True,exclude="_id")})
    return {"data":"The data has been successfully updated"}

@package.post('/show_package',description="Displaying all the packages")
async def show_packages(package_filter:Annotated[PackageFilter,Body(),]):
    res = []
    package_filter._id=ObjectId(package_filter._id)
    for document in PACKAGE.find(package_filter.model_dump(exclude_unset=True)):
        document['_id'] = str(document['_id'])
        res.append(document)
    print(len(res))
    return res

@package.get('/',description="Displaying the package by using id")
async def get_package(id:str):
        res = PACKAGE.find_one({"_id":ObjectId(id)})
        res["_id"] = str(res["_id"])
        print(res)
        return res

@package.get('/check_availability/',description="Displaying the availability of seats")
async def get_available_seats(name:str):
    res = PACKAGE.find_one({"name": name})
    if res["availability"] > 0:
        return {"available seats":res["availability"]}
    else:
        return "The seats are full"

@package.get('/check_destinations/',description="Displaying the destinations in the package")
async def get_destinations(name:str):
    res = PACKAGE.find_one({"name":name})
    print(res["destination"])
    return res["destination"]

@package.get('/length/',description="Diaplaying the length of the package")
async def get_length(name:str):
    res = PACKAGE.find_one({"name":name})
    days = res["end_date"] - res["start_date"]
    return str(days)

@package.get('/amount',description="Displaying the packages within the budget")
async def get_amount(amount:float):
    res = []
    for document in PACKAGE.find({"amount":{"$lte":amount}}).sort({"amount":-1}):
        document["_id"] = str(document["_id"])
        res.append(document)
    return res

@package.delete('/',description="Deleting packages")
async def delete_packages(id:str):
    PACKAGE.delete_one({"_id":ObjectId(id)})
    return {"data":"data has been successfully deleted"}

