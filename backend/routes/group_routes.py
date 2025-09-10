from fastapi import APIRouter, HTTPException, Request
from firebase_admin import firestore

router = APIRouter()

# Get Firestore client
db = firestore.client()

@router.post("/groups")
async def create_group(request: Request):
	data = await request.json()
	name = data.get("name")
	members = data.get("members", [])  # List of user IDs
	if not name:
		raise HTTPException(status_code=400, detail="Group name is required.")
	group_data = {
		"name": name,
		"members": members
	}
	try:
		doc_ref = db.collection("groups").add(group_data)
		return {"group_id": doc_ref[1].id, "name": name, "members": members}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
