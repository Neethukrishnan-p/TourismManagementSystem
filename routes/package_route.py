from fastapi import APIRouter,Body
from db_config import PACKAGE
from bson import ObjectId
from models.package_model import Packages,PackageFilter

package = APIRouter()

@package.post('/create/',description="Adding packages")
async def create_packages(package:Packages):
    PACKAGE.insert_one(package.model_dump())
    return {"data":"package data has been created"}

@package.put('/',description="Updating the details")
async def update_package_details(package_filter:PackageFilter,id:str=Body(...)):
    PACKAGE.update_one({"_id":ObjectId(id)},{"$set":package_filter.model_dump(exclude_unset=True)})
    return {"data":"The data has been successfully updated"}

@package.get('/',description="Displaying all the packages")
async def show_packages():
    res = []
    for document in PACKAGE.find():
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
async def get_available_seats(p_name:str):
    res = PACKAGE.find_one({"p_name": p_name})
    if res["availability"] > 0:
        return {"available seats":res["availability"]}
    else:
        return "The seats are full"

@package.get('/check_destinations/',description="Displaying the destinations in the package")
async def get_destinations(p_name:str):
    res = PACKAGE.find_one({"p_name":p_name})
    print(res["destination"])
    return res["destination"]




@package.delete('/',description="Deleting packages")
async def delete_packages(id:str):
    PACKAGE.delete_one({"_id":ObjectId(id)})
    return {"data":"data has been successfully deleted"}

