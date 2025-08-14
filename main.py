from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/todos", response_model=list[schemas.TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(models.ToDo).all()
    return todos

@app.post("/todos", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    try:
        if not todo.name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")

        new_todo = models.ToDo(
            name=todo.name,
            is_active=todo.is_active,
            user_id=todo.user_id
        )
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/todos/{id}", status_code=status.HTTP_200_OK)
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).filter(models.ToDo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

# --- User Endpoints ---

@app.get("/users", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        if not user.name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        existing = db.query(models.User).filter(models.User.name == user.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Name must be unique")
        new_user = models.User(
            name=user.name,
            email=user.email
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
