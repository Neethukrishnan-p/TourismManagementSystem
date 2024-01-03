from fastapi import APIRouter,HTTPException,status,Body
from db_config import PASSENGER,PACKAGE
from models.passenger_model import Passenger,Passenger_filter
from bson import ObjectId
import datetime


passenger = APIRouter()


@passenger.post('/add/',description="Creating and adding Passenger details",status_code=status.HTTP_201_CREATED)
async def create_passenger(passenger:Passenger):
    passenger.package_id = ObjectId(passenger.package_id)
    user = passenger.model_dump()
    user["rating"] = 0
    res = PACKAGE.find_one({"_id": passenger.package_id})
    print(type(res["start_date"]))
    if res["availability"]:
        if passenger.date_of_travel.replace(tzinfo=None) >= res["start_date"] and passenger.date_of_travel.replace(tzinfo=None) < res["end_date"]:
            PACKAGE.update_one({"_id": passenger.package_id}, {"$set": {"availability": res["availability"] - 1}})
            PASSENGER.insert_one(user)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Enter the travel date between {res['start_date']} and {res['end_date']}")
    else:
        return "The seats are full"
    user["_id"] = str(user["_id"])
    user["package_id"] = str(user["package_id"])
    return user

@passenger.put('/update/',description="Updating the passenger details")
async def update_passenger_details(passenger_filter:Passenger_filter,doc_id:str=Body(...)):
    passenger = PASSENGER.find_one({"_id": ObjectId(doc_id)})
    if passenger:
        res1 = PACKAGE.find_one({"_id": passenger["package_id"]})
        PACKAGE.update_one({"_id": passenger["package_id"]},{"$set": {"availability": res1["availability"] + 1}})
    if passenger_filter.package_id:
        passenger_filter.package_id = ObjectId(passenger_filter.package_id)
        res2 = PACKAGE.find_one({"_id":passenger_filter.package_id})
        PACKAGE.update_one({"_id":passenger_filter.package_id},{"$set":{"availability":res2["availability"]-1}})
    PASSENGER.update_one({"_id": ObjectId(doc_id)}, {"$set": passenger_filter.model_dump(exclude_unset=True)})
    res = []
    for document in PASSENGER.find({"_id":ObjectId(doc_id)}):
        document["_id"] = str(document["_id"])
        document["package_id"] = str(document["package_id"])
        res.append(document)
        return res


@passenger.post('/',description="Displaying the passenger details")
async def show_passengers(passenger_filter:Passenger_filter):
    res = []
    if passenger_filter.id:
        passenger_filter.id = ObjectId(passenger_filter.id)
    filter_dict = passenger_filter.model_dump(exclude_unset=True)
    if "id" in filter_dict:
        filter_dict["_id"] = filter_dict["id"]
        del filter_dict["id"]
    if "package_id" in filter_dict:
        passenger_filter.package_id = ObjectId(passenger_filter.package_id)
        filter_dict["package_id"] = passenger_filter.package_id
    for document in PASSENGER.find(filter_dict):
        document['_id'] = str(document['_id'])
        document['package_id'] = str(document['package_id'])
        res.append(document)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no passengers")
    return res

@passenger.get('/package',description="Displaying the passenger details using the package_id")
async def passenger_enrolled(package_id:str):
    res = []
    for document in PASSENGER.find({"package_id":ObjectId(package_id)}):
        document['package_id'] = str(document['package_id'])
        document['_id'] = str(document['_id'])
        res.append(document)
    print(len(res))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is no passenger with the package_id {package_id}")
    return res

@passenger.post('/rating',description="Displaying the average rating and the total ratings")
async def rate_package(id:str,value:float):
    res1 = PASSENGER.find_one({"_id":ObjectId(id)})
    current_time = datetime.datetime.now()
    if (current_time < res1["date_of_travel"]) or res1["rating"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can't rate the package")
    if value <= 5 and value >0:
        PASSENGER.update_one({"_id":ObjectId(id)},{"$set":{"rating":value}})

        res2 = PACKAGE.find_one({"_id":res1["package_id"]})
        new_value = (sum(res2["total_rating"])+value)/(len(res2["total_rating"])+1)

        PACKAGE.update_one({"_id":res1["package_id"]},{"$set":{"rating":new_value},"$push":{"total_rating":value}})
        res = PACKAGE.find_one({"_id":res1["package_id"]})
        res["_id"] = str(res["_id"])
        return res
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Enter a value less than 5")


@passenger.get('/bypackages',description="Displaying no.of passengers for each package")
async def get_no_of_passenger():
    res = []
    for document in PASSENGER.aggregate([{"$group":{"_id":"$package_id","no of passengers":{"$count":{}}}}]):
        package = PACKAGE.find_one({"_id":document["_id"]})
        document["name"] = package["name"]
        document["_id"] = str(document["_id"])
        res.append(document)
        print(document)
    return res


@passenger.delete('/',description="Deleting passenger details",status_code=status.HTTP_200_OK)
async def delete_passenger(id:str):
    passenger = PASSENGER.find_one({"_id":ObjectId(id)})
    if passenger:
        package = PACKAGE.find_one({"_id": passenger["package_id"]})
        PACKAGE.update_one({"_id":passenger["package_id"]},{"$set":{"availability": package["availability"] + 1}})
        PASSENGER.delete_one({"_id":ObjectId(id)})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no such passenger")
    return {"data":"data has been successfully deleted"}

