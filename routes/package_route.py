from fastapi import APIRouter,Body,status,HTTPException
from db_config import PACKAGE
from bson import ObjectId
from models.package_model import Packages,PackageFilter,RatedPackage
from typing import Annotated
from datetime import datetime


package = APIRouter()

@package.post('/create/',description="Adding packages",status_code=status.HTTP_201_CREATED)
async def create_packages(package:Packages):
    packages = [doc for doc in PACKAGE.find({"name": package.name})]
    if packages:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"{package.name} already exists")
    package = RatedPackage(**package.model_dump())
    PACKAGE.insert_one(package.model_dump())
    return package

@package.put('/update',description="Updating the details")
async def update_package_details(package_filter:PackageFilter,doc_id:str=Body(...)):
    if package_filter.name:
        packages =  PACKAGE.find_one({"name": package_filter.name})
        if packages:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"{package_filter.name} already exists")
    PACKAGE.update_one({"_id":ObjectId(doc_id)},{"$set":package_filter.model_dump(exclude_unset=True)})
    res = []
    for document in PACKAGE.find({"_id":ObjectId(doc_id)}):
        document["_id"] = str(document["_id"])
        res.append(document)
    return res

@package.post('/show_package',description="Displaying all the packages")
async def show_packages(package_filter:Annotated[PackageFilter,Body(),]):
    res = []
    if package_filter.id:
        package_filter.id=ObjectId(package_filter.id)
    filter_dict=package_filter.model_dump(exclude_unset=True)
    if "id" in filter_dict:
        filter_dict["_id"]=filter_dict["id"]
        del filter_dict["id"]
    print(filter_dict)

    for document in PACKAGE.find(filter_dict):
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
        return {"available seats are ":res["availability"]}
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
    print(type(days))
    return days//86400

@package.get('/amount',description="Displaying the packages within the budget")
async def get_amount(amount:float):
    res = []
    for document in PACKAGE.find({"amount":{"$lte":amount}}).sort({"amount":-1}):
        document["_id"] = str(document["_id"])
        res.append(document)
    return res

@package.delete('/',description="Deleting packages",status_code=status.HTTP_200_OK)
async def delete_packages(id:str):
    PACKAGE.delete_one({"_id":ObjectId(id)})
    return {"data":"data has been successfully deleted"}

