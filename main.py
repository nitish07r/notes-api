from fastapi import Depends, FastAPI
from pydantic_models import Note
import database_models
import json
from http import HTTPStatus
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

#here database_models.Note is different from pydantic_models.Note,we use database_models.Note to create tables in database and pydantic_models.Note to validate the data coming from the user,we cant write from database_models import Note because it will create confusion between the two Note classes, so we use different names for them,instead we can use from database_models import Note as DatabaseNote to avoid confusion
app = FastAPI()

# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# list of notes with 5 Note objects
notes = [
    Note(created_by="User1", name="Meeting Notes", description="Discussion about project timeline", priority=8),
    Note(created_by="User2", name="Todo List", description="Tasks for the week", priority=5),
    Note(created_by="User3", name="Ideas", description="Brainstorming new features", priority=3),
    Note(created_by="User1", name="Code Review", description="Review pull request #123", priority=9),
    Note(created_by="User4", name="Documentation", description="Update API documentation", priority=6),
]




def init_db():
    db = SessionLocal()

    existing_count = db.query(database_models.Note).count()

    if existing_count == 0:
        for note in notes:
            db.add(database_models.Note(**note.model_dump()))
        db.commit()
        print("Database initialized with sample notes.")
        
    db.close()

init_db()    

database_models.Base.metadata.create_all(bind=engine)
#create note
@app.post("/notes") 
def create_note(note: Note,db:Session= Depends(get_db)):
    #u can use model_dump() method to convert pydantic model to dictionary and then pass it to database model also
    db_note=database_models.Note(
        created_by=note.created_by,
        name=note.name,
        description=note.description,
        priority=note.priority
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return {"message":"note created","Note":db_note}
    #region JSON POST implementation    
    # with open("Notes.json", "r") as file:
    #     data = json.load(file)

    # new_note = {
    #     "id": len(data) + 1,
    #     "created_by": note.created_by,
    #     "name": note.name,
    #     "description": note.description,
    #     "priority": note.priority
    # }

    # data.append(new_note)

    # with open("Notes.json", "w") as file:
    #     json.dump(data, file, indent=4)

    # return {"message": "Note created", "note": new_note}
    # #return new_note
    #endregion    

#get all notes
@app.get("/notes")
def greet(db: Session = Depends(get_db)):
    db_notes= db.query(database_models.Note).all()
    if db_notes:
        return db_notes
    return {"message":"no notes found"}
    #region JSON GET implementation
    # with open("Notes.json", "r") as file:
    #     data = json.load(file)
    # #return "hii welcome to my fastapi server"
    # return data
    #endregion

#get note by id
@app.get("/notes/{note_id}")
def get_note_byId(note_id:int,db: Session= Depends(get_db)):

    db_note=db.query(database_models.Note).filter(database_models.Note.id==note_id).first()
    if db_note:
        return db_note
    return {"message":"note not found"}
    #region JSON GET implementation
    # with open("Notes.json","r") as file:
    #     data=json.load(file)
    # for i in range(len(data)):
    #     if data[i]["id"]==note_id:
    #         return {"message":"note fetched succesfully","note":data[i]}
    # return {"message":"note not found"}
    #endregion


#edit note by id
@app.put("/notes/{note_id}")
def modify_note(note_id:int,note:Note,db:Session=Depends(get_db)):
    db_note=db.query(database_models.Note).filter(database_models.Note.id==note_id).first()
    if db_note:
        db_note.created_by = note.created_by
        db_note.name = note.name
        db_note.description = note.description
        db_note.priority = note.priority
        db.commit()
        db.refresh(db_note)
        return {"message":f"note with id-{note_id} is updated","note":db_note}
    return {"message":"note not found"}
    #region JSON PUT implementation
    # with open("Notes.json","r") as file:
    #     data=json.load(file)
    # for i in range(len(data)):
    #     if data[i]["id"]==note_id:
    #         data[i]={
    #             "id":note_id,
    #             "created_by":notes.created_by,
    #             "name":notes.name,
    #             "description":notes.description,
    #             "priority":notes.priority
    #         }
    #         with open("Notes.json","w") as file:
    #             json.dump(data,file,indent=4)
    #         return {"message": "note updated", "note": data[i]}
    # return{"message":"note not found to update"}
    #endregion

#delete note by id           
@app.delete("/notes/{note_id}")
def delete_note(note_id:int,db:Session=Depends(get_db)):
    db.delete(database_models.Note).filter(database_models.Note.id==note_id)
    db.commit()
    return {"message":f"note with id-{note_id} deleted"}
    #region JSON DELETE implementation
    # with open("Notes.json","r") as f:
    #     data=json.load(f)
    # for i in range(len(data)):
    #     if data[i]["id"]==note_id:
    #         del data[i]
    #         with open("Notes.json","w") as file:
    #             json.dump(data,file,indent=4)
    #         return{"message":f"note with id-{note_id} deleted"}
    # return {"message":"note not found"}
    #endregion
            
