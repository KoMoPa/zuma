from fastapi import APIRouter, HTTPException, Request
from firebase_admin import auth

router = APIRouter()


@router.post("/register")
async def register_user(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    try:
        user = auth.create_user(email=email, password=password)
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Update user endpoint
@router.put("/update/{uid}")
async def update_user(uid: str, request: Request):
    data = await request.json()
    update_fields = {}
    if "email" in data:
        update_fields["email"] = data["email"]
    if "password" in data:
        update_fields["password"] = data["password"]
    if "display_name" in data:
        update_fields["display_name"] = data["display_name"]
    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid fields to update.")
    try:
        user = auth.update_user(uid, **update_fields)
        return {"uid": user.uid, "email": user.email, "display_name": user.display_name}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete user endpoint
@router.delete("/delete/{uid}")
async def delete_user(uid: str):
    try:
        auth.delete_user(uid)
        return {"message": f"User {uid} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))