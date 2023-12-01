from fastapi import APIRouter,HTTPException,status,Body
from db_config import PASSENGER,PACKAGE
from models.passenger_model import Passenger,Passenger_filter
from bson import ObjectId
from typing import Annotated

passenger = APIRouter()

@passenger.post('/add/',description="Creating and adding Passenger details")
async def create_passenger(passenger:Passenger):
    passenger.package_id = ObjectId(passenger.package_id)
    user = passenger.model_dump()
    user["rating"] = 0
    res = PACKAGE.find_one({"_id": passenger.package_id})
    if res["availability"]:
        PACKAGE.update_one({"_id": passenger.package_id}, {"$set": {"availability": res["availability"] - 1}})
        PASSENGER.insert_one(user)
    else:
        return "The seats are full"
    return {"data":"passenger data has been created"}

@passenger.post('/',description="Displaying all passenger details")
async def show_passengers(passenger_filter:Annotated[Passenger_filter,Body()]):
    res = []
    passenger_filter._id = ObjectId(passenger_filter._id)
    for document in PASSENGER.find(passenger_filter.model_dump(exclude_unset=True)):
        document['_id'] = str(document['_id'])
        document['package_id'] = str(document['package_id'])
        res.append(document)
    print(len(res))
    return res

@passenger.get('/package')
async def passenger_enrolled(package_id:str):
    res = []
    for document in PASSENGER.find({"package_id":ObjectId(package_id)}):
        document['package_id'] = str(document['package_id'])
        document['_id'] = str(document['_id'])
        res.append(document)
    print(len(res))
    return res

@passenger.post('/rating',description="Displaying the average rating and the total ratings")
async def rate_package(id:str,value:float):
    res1 = PASSENGER.find_one({"_id":ObjectId(id)})
    if (not res1["status"] == "prior") and res1["rating"] == 0:
        if value <= 5:
            PASSENGER.update_one({"_id":ObjectId(id)},{"$set":{"rating":value}})

            res2 = PACKAGE.find_one({"_id":res1["package_id"]})
            new_value = (sum(res2["total_rating"])+value)/(len(res2["total_rating"])+1)

            PACKAGE.update_one({"_id":res1["package_id"]},{"$set":{"rating":new_value},"$push":{"total_rating":value}})
            res = PACKAGE.find_one({"_id":res1["package_id"]})
            res["_id"] = str(res["_id"])
            return res
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Enter a value less than 5")
    else:
        return "You can't rate the package"

@passenger.get('/bypackages',description="Displaying no.of passengers for each package")
async def get_no_of_passenger():
    res = []
    for document in PASSENGER.aggregate([{"$group":{"_id":"$package_id","no of passengers":{"$count":{}}}}]):
        document["name"] = PACKAGE.find_one({"_id":document["_id"]})["name"]
        document["_id"] = str(document["_id"])
        res.append(document)
        print(document)
    return res


@passenger.delete('/',description="Deleting passenger details")
async def delete_passenger(id:str):
    PASSENGER.delete_one({"_id":ObjectId(id)})
    return {"data":"data has been successfully deleted"}

