import uvicorn
from fastapi import FastAPI
import mysql.connector

app = FastAPI()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="python_rest_api"
)


@app.get("/employees")
def get_employees():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM employees")
    result = cursor.fetchall()
    return {"employees": result}


@app.get("/employees/{id}")
def get_employee(id: int):
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM employees WHERE eid = {id}")
    result = cursor.fetchone()
    return {"employee": result}


@app.post("/employees/add")
def add_employee(name: str, email: str):
    cursor = mydb.cursor()
    sql = "INSERT INTO employees (ename, email) VALUES (%s, %s)"
    val = (name, email)
    cursor.execute(sql, val)
    mydb.commit()
    return {"message": "Employee added successfully"}


@app.delete("/employees/delete/{id}")
def delete_employee(id: int):
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM employees WHERE eid = {id}")
    mydb.commit()
    return {"message": "Employee deleted successfully"}


@app.put("/employees/change/{id}")
def delete_employee(id: int, name: str, email: str):
    cursor = mydb.cursor()
    sql = "UPDATE employees SET ename=%s, email=%s WHERE eid = %s"
    val = (name, email, id)
    cursor.execute(sql, val)
    mydb.commit()
    return {"message": "Employee Updated successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
