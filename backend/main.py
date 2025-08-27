
from fastapi import FastAPI
import firebase_admin
from firebase_admin import firestore, auth 

firebase_admin.initialize_app()

db = firestore.client()
auth_sdk = auth 


app = FastAPI()


@app.get("/hello-firestore")
async def hello_firestore():
    doc_ref = db.collection('settings').document('general')
    doc = doc_ref.get()
    if doc.exists:
        return {"message": "Settings found!", "data": doc.to_dict()}
    else:
        return {"message": "No settings document found."}
