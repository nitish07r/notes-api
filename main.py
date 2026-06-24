from fastapi import FastAPI
from pydantic import BaseModel
import json
from http import HTTPStatus
app = FastAPI()

class Note(BaseModel):
    name: str
    description: str
    created_by:str
    priority: int


@app.post("/notes")
def create_note(note: Note):
    with open("Notes.json", "r") as file:
        data = json.load(file)

    new_note = {
        "id": len(data) + 1,
        "created_by": note.created_by,
        "name": note.name,
        "description": note.description,
        "priority": note.priority
    }

    data.append(new_note)

    with open("Notes.json", "w") as file:
        json.dump(data, file, indent=4)

    return {"message": "Note created", "note": new_note}
    #return new_note

@app.get("/notes")
def greet():
    with open("Notes.json", "r") as file:
        data = json.load(file)
    #return "hii welcome to my fastapi server"
    return data

@app.get("/notes/{note_id}")
def get_note_byId(note_id:int):
    with open("Notes.json","r") as file:
        data=json.load(file)
    for i in range(len(data)):
        if data[i]["id"]==note_id:
            return {"message":"product fetched succesfully","note":data[i]}
    return {"message":"product not found"}
    
@app.put("/notes/{note_id}")
def modify_note(note_id:int,notes:Note):
    with open("Notes.json","r") as file:
        data=json.load(file)
    for i in range(len(data)):
        if data[i]["id"]==note_id:
            data[i]={
                "id":note_id,
                "created_by":notes.created_by,
                "name":notes.name,
                "description":notes.description,
                "priority":notes.priority
            }
            with open("Notes.json","w") as file:
                json.dump(data,file,indent=4)
            return {"message": "note updated", "note": data[i]}
    return{"message":"note not found to update"}
            
@app.delete("/notes/{note_id}")
def delete_note(note_id:int):
    with open("Notes.json","r") as f:
        data=json.load(f)
    for i in range(len(data)):
        if data[i]["id"]==note_id:
            del data[i]
            with open("Notes.json","w") as file:
                json.dump(data,file,indent=4)
            return{"message":f"note with id-{note_id} deleted"}
    return {"message":"note not found"}
            
            
