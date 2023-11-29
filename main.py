import uvicorn
from fastapi import FastAPI
from routes.package_route import package
from routes.passenger_route import passenger



app = FastAPI()
app.include_router(package,prefix='/packages',tags=["Package"])
app.include_router(passenger,prefix='/passenger',tags=["Passenger"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

