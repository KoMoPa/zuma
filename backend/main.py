from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from fastapi import FastAPI
from backend.routes.user_routes import router as user_router
from backend.routes.group_routes import router as group_router
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os

# --- Detect if we're running in emulator/test mode ---
USE_EMULATOR = os.getenv("FIREBASE_EMULATOR") == "true"

# --- Configure emulator host/ports ---
if USE_EMULATOR:
    os.environ["FIRESTORE_EMULATOR_HOST"] = os.getenv("FIRESTORE_EMULATOR_HOST", "localhost:8080")
    os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = os.getenv("FIREBASE_AUTH_EMULATOR_HOST", "localhost:9099")
    print("⚡ Using Firebase Emulators: Firestore + Auth")

# --- Path to service account key for real Firebase (not used in tests) ---
SERVICE_ACCOUNT_KEY_PATH = "./keys/zuma-1776b-firebase-adminsdk-fbsvc-dedc84521d.json"

# --- Initialize Firebase Admin SDK ---
try:
    if USE_EMULATOR:
        # Emulator mode: no credentials needed
        firebase_admin.initialize_app(options={"projectId": "demo-project"})
        print("Firebase Admin SDK initialized using emulator.")
    else:
        # Real Firebase: only if not testing
        if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
            raise FileNotFoundError(f"Service account key file not found at {SERVICE_ACCOUNT_KEY_PATH}")
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)
        print(f"Firebase Admin SDK initialized successfully for project {firebase_admin.get_app().project_id}")
except Exception as e:
    print(f"ERROR: Failed to initialize Firebase Admin SDK: {e}")
    if not USE_EMULATOR:
        raise e  # Only fail hard if not in emulator mode

# --- Firestore & Auth clients ---
db = firestore.client()
auth_sdk = auth

print("--- Firebase App Initialization Complete ---")

# --- FastAPI setup ---
app = FastAPI()
app.include_router(user_router, prefix="/api/users")
app.include_router(group_router, prefix="/api/groups")


@app.get("/hello-firestore")
async def hello_firestore():
    print("\n--- /hello-firestore endpoint hit ---")
    doc_ref = db.collection('settings').document('general')
    print(f"Attempting to get document: Collection 'settings', Document 'general'")
    try:
        doc = doc_ref.get()
        if doc.exists:
            print(f"Document found! Data: {doc.to_dict()}")
            return {"message": "Settings found!", "data": doc.to_dict()}
        else:
            print("Document DOES NOT EXIST.")
            return {"message": "No settings document found."}
    except Exception as e:
        print(f"ERROR fetching document: {e}")
        return {"message": f"Error fetching settings: {e}"}
