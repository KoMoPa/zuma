from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, firestore, auth # Make sure to import credentials

# ---  Initialization for LOCAL DEVELOPMENT ---
# Only for testing locally.
# Replace 'path/to/your/serviceAccountKey.json' with actual path.
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
# --- End LOCAL DEVELOPMENT specific configuration ---

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
