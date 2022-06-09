from fastapi import FastAPI,Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


students = {
	1: {
		"name": "John",
		"age": 18,
		"year": "year 22"
	}
}

class Student(BaseModel):
	name: str
	age: int
	year: str


class UpdateStudent(BaseModel):
	name: Optional[str] = None
	age: Optional[int] = None
	year: Optional[str] =None



# Static call
@app.get("/")
def index():
	return {"name": "First Data"}


# dynamically call
# @app.get("/get-students/{student_id}")
# def get_student(student_id: int):
# 	return students[student_id]


# Path Parameter
@app.get("/get-students/{student_id}")
def get_student(student_id: int = Path(None, description = "Enter the id of stuent that you want to see",gt=0,lt=3)):  # the ip should be greater than 0 and less than 3
	return students[student_id]


# Query Parameter
@app.get("/get-by-name")
def get_student(*, name: Optional[str] = None,test : int):  # In python optional parameter shold not come before required parameter so * is used
	for student_id in students:
		return students[student_id]
	return {"Data": "Not found"}


# Combining Path and Query parameter
@app.get("/get-by-name1/{student_id}")
def get_student(*, student_id : int, name : Optional[str]= None, test : int):
	for student_id in students:
		if students[student_id]["name"] == name:
			return students[student_id]
	return {"Data": "Not found"}



# Request body and the POST method. From pydantic import BaseModel. Create
@app.post("/create-student/{student_id}")
def create_student(student_id : int,student: Student):
	if student_id in students:
		return {"Error": "Student exists"}

	students[student_id]= student
	return students[student_id]


# Put Method ->Update something that already exists
# If we perform put operation using:- class Student(BaseModel) , all the data should be entered like name, age, year.
# socreate a new class for updating particular field
@app.put("/update-students/{student-id}")
def update_student(student_id: int, student:UpdateStudent):
	if student_id not in students:
		return{"Error": "Student does not exist"}

	# students[student_id] = student  -> If we update student like this then the field that we dont want to update will be automatically get null.eg:
	# Response body
	# {
	#   "name": "tim",
	#   "age": null,
	#   "year": null
	# }

	if student.name != None:
		students[student_id].name = student.name

	if student.age != None:
		students[student_id].age = student.age

	if student.year != None:
		students[student_id].year = student.year

	return students[student_id]


# Delete method
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
	if student_id not in students:
		return {"Error": "Student does not exist"}

	del students[student_id]
	return {"Message": "Students deleted succesfully"}


# Type uvicorn myapi:app --reload to the cmd for running the api using uvicorn the 'app' here is coming from [app = FastAPI()] 
# For seeing the output in uvicorn browser add docs at theendpoint of url like:- http://127.0.0.1:8000/docs
