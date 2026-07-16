from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


@app.get("/")
def home():
    return {
        "message": "Portfolio Backend Running"
    }


@app.post("/contact")
def save_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):

    new_contact = models.Contact(
        name=contact.name,
        email=contact.email,
        message=contact.message
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return {
        "message": "Message Sent Successfully"
    }


@app.get("/contacts")
def get_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).all()