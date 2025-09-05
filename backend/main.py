import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from fastapi import FastAPI
from routes.user_routes import router  
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os # Import os for checking file existence

# --- Initialization for LOCAL DEVELOPMENT ---
SERVICE_ACCOUNT_KEY_PATH = "./keys/zuma-1776b-firebase-adminsdk-fbsvc-dedc84521d.json"

print("--- Starting Firebase App Initialization Check ---")

if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
    print(f"ERROR: Service account key file not found at: {SERVICE_ACCOUNT_KEY_PATH}")
    print("Please ensure the path is correct and the file exists.")
    # You might want to exit here in a real app if the key is missing
    # exit(1)
else:
    print(f"Service account key file found at: {SERVICE_ACCOUNT_KEY_PATH}")


try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized successfully.")
    # Check the project ID the SDK is initialized with
    print(f"SDK initialized for project ID: {firebase_admin.get_app().project_id}")
except Exception as e:
    print(f"ERROR: Failed to initialize Firebase Admin SDK: {e}")
    print("This could be due to an invalid key file or other configuration issues.")
    # exit(1) # You might want to exit here if initialization fails


db = firestore.client()
# Note: The firestore.client() call connects to the *default* Firestore instance.
# If you created your 'settings/general' in 'northamerica-northeast2', you'd need to specify it.
# However, usually the default is where you'd put general app settings.
print(f"Firestore client obtained. It will connect to the default Firestore database.")
auth_sdk = auth

print("--- Firebase App Initialization Check Complete ---")


app = FastAPI()
app.include_router(router, prefix="/api/users")


@app.get("/hello-firestore")
async def hello_firestore():
    print("\n--- /hello-firestore endpoint hit ---")
    doc_ref = db.collection('settings').document('general')
    print(f"Attempting to get document: Collection 'settings', Document 'general'")

    try:
        doc = doc_ref.get() # This is where the actual network call to Firestore happens
        print(f"Firestore get() call completed.")

        if doc.exists:
            print(f"Document 'settings/general' found! Data: {doc.to_dict()}")
            return {"message": "Settings found!", "data": doc.to_dict()}
        else:
            print(f"Document 'settings/general' DOES NOT EXIST according to Firestore.")
            print("Possible reasons: Mismatch in project, typo in collection/document name, or document not actually created.")
            return {"message": "No settings document found."}
    except Exception as e:
        print(f"ERROR: An error occurred while fetching the document: {e}")
        return {"message": f"Error fetching settings: {e}"}

