from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Content(BaseModel):
    name: str
    description: Optional[str] = None

class Subject(BaseModel):
    name: str
    level: int
    UC: int
    price: float
    description: Optional[str] = None
    contents: List[Content] = []

class Student(BaseModel):
    name: str
    lastname: str
    birthDate: str
    phoneNumber: str
    address: str
    academicRecord: List[Subject] = []

students: List[Student] = []

@app.post("/estudiantes/")
async def add_students(student: Student):
    students.append(student)
    return {"msg": "Estudiante agregado exitosamente", "estudiante": student}

@app.get("/estudiantes/{index}")
async def search_student(index: int):
    if index < 0 or index >= len(students):
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return students[index]

@app.get("/estudiantes/")
async def list_students():
    studentsI = [
        {"index": index, "estudiante": student}
        for index, student in enumerate(students)
    ]
    return studentsI

#agrega una materia a un estudiante
@app.post("/estudiantes/{index}/materias/")
async def add_subject(index: int, subject: Subject):
    if index < 0 or index >= len(students):
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    students[index].academicRecord.append(subject)
    return {"msg": "Materia agregada exitosamente", "subject": subject}

#agrega un contenido a una materia de un estudiante
@app.post("/estudiantes/{index}/materias/{subjectIndex}/contenidos/")
async def add_content(index: int, subjectIndex: int, content: Content):
    if index < 0 or index >= len(students):
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    student = students[index]
    if subjectIndex < 0 or subjectIndex >= len(student.academicRecord):
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    student.academicRecord[subjectIndex].contents.append(content)
    return {"msg": "Contenido agregado exitosamente", "content": content}

#modificar un estudiante
@app.put("/estudiantes/{index}")
async def update_student(index: int, updStudent: Student):
    if index < 0 or index >= len(students):
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    students[index] = updStudent
    return {"msg": "Estudiante modificado exitosamente", "student": updStudent}

#eliminar un estudiante
@app.delete("/estudiantes/{index}")
async def delete_student(index: int):
    if index < 0 or index >= len(students):
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    deletedStudent = students.pop(index)
    return {"msg": "Estudiante eliminado exitosamente", "student": deletedStudent}