import uvicorn
from fastapi import FastAPI
from routes.package_route import package
from routes.passenger_route import passenger

tags_metadata = [
    {
        "name":"Package",
        "description":"Doing several operations using **package**.",
    },
    {
        "name":"Passenger",
        "description":"Doing several operations using **passenger**.",
    },
]

app = FastAPI(
    title="Holidays Tourism App",
    openapi_tags=tags_metadata,
    description="""Holidays Tourism App is a tour management system for Holidays Tourism Company to keep track of all the tour packages and details of the customers.<br><br>
    **Package**<br>
    <br>
    You will be able to:<br>
    <br>
    * _Create packages_<br>
    * _Read packages_<br>
    * _Update package details_<br>
    * _Delete packages_<br>
    <br>
    **Passenger**<br>
    <br>
    You will be able to:<br>
    <br>
    * _Add passengers to the packages_<br>
    * _Read passenger details_<br>
    * _Update passenger details_<br>
    * _Delete passengers_<br>
    """,
)
app.include_router(package,prefix='/packages',tags=["Package"])
app.include_router(passenger,prefix='/passenger',tags=["Passenger"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

