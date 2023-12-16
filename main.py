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
description = '''
    Holidays Tourism App is a tour management system for Holidays Tourism Company to keep track of all the tour packages and details of the customers.

    Packages

    You will be able to:

    Create packages.
    Read packages.
    Update package details.
    Delete packages.

    Passenger

    You will be able to:
    
    Add passengers to the packages.
    Read passenger details.
    Update passenger details.
    Delete passengers.
    '''

app = FastAPI(
    title="Holidays Tourism App",
    openapi_tags=tags_metadata,
    description=description,
)
app.include_router(package,prefix='/packages',tags=["Package"])
app.include_router(passenger,prefix='/passenger',tags=["Passenger"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

