from fastapi import APIRouter
from db_config import PASSENGER,PACKAGE
from models.passenger_model import Passenger
from bson import ObjectId

passenger = APIRouter()

@passenger.post('/add/',description="Creating and adding Passenger details")
async def create_passenger(passenger:Passenger):
    passenger.package_id = ObjectId(passenger.package_id)
    PASSENGER.insert_one(passenger.model_dump())

    res = PACKAGE.find_one({"_id":passenger.package_id})
    PACKAGE.update_one({"_id":passenger.package_id},{"$set":{"availability":res["availability"]-1}})
    return {"data":"passenger data has been created"}

@passenger.get('/',description="Displaying all passenger details")
async def show_passengers():
    res = []
    for document in PASSENGER.find():
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

@passenger.delete('/',description="Deleting passenger details")
async def delete_passenger(id:str):
    PASSENGER.delete_one({"_id":ObjectId(id)})
    return {"data":"data has been successfully deleted"}

