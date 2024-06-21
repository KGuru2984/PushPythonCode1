# import asyncio

import uvicorn
from fastapi import FastAPI, HTTPException, APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
database = client["testAPI"]
collection = database["employees"]


class Employees(BaseModel):
    name: str
    email: str
    eid: int = None


def emp_serializer(emp) -> dict:
    return {
        'id': str(emp["_id"]),
        'name': emp["name"],
        'email': emp["email"],
        'eid': emp["eid"]
    }


async def create_employee(emp: Employees) -> dict:
    # Generate unique eid for the employee
    emp_dict = emp.dict()
    emp_id = await generate_unique_eid()
    emp_dict["eid"] = emp_id
    result = await collection.insert_one(emp_dict)
    inserted_id = result.inserted_id
    inserted_emp = await collection.find_one({"_id": inserted_id})
    if inserted_emp:
        return emp_serializer(inserted_emp)
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


async def generate_unique_eid() -> int:
    # Find the maximum value of the eid field in the collection
    max_eid = await collection.find_one(sort=[("eid", -1)])
    if max_eid:
        return max_eid["eid"] + 1  # Increment the maximum eid by 1
    else:
        return 1  # If no records exist, start from 1


@app.post("/employees/add")
async def create_user(emp: Employees):
    return {"status": "Ok", "data": await create_employee(emp)}


@app.get("/employees")
async def read_employees():
    employees = []
    async for emp in collection.find():
        employees.append(emp_serializer(emp))
    return employees


@app.get("/employees/{employee_eid}")
async def read_employee(employee_eid: int):
    print(f"Searching for employee with eid: {employee_eid}")
    employee = await collection.find_one({"eid": employee_eid})  # Query based on eid
    print(f"Employee found: {employee}")
    if employee:
        return emp_serializer(employee)
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@app.put("/employees/change/{employee_eid}")
async def update_employee(employee_eid: int, emp: Employees):
    # Remove eid from the updated data
    emp_dict = emp.dict(exclude={"eid"})
    result = await collection.update_one(
        {"eid": employee_eid},
        {"$set": emp_dict}
    )
    if result.modified_count == 1:
        return {"status": "Ok", "message": "Employee updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@app.delete("/employees/delete/{employee_eid}")
async def delete_employee(employee_eid: int):
    result = await collection.delete_one({"eid": employee_eid})
    if result.deleted_count == 1:
        return {"status": "Ok", "message": "Employee deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
