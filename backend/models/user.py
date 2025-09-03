from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class User(BaseModel):
   
    # Core identification
    id: Optional[str] = None  

    # Authentication & contact info
    email: EmailStr # Validated email format
    is_active: bool = True # Flag for account status (e.g., if a user deactivates their account)

    # Basic profile information
    display_name: str
    first_name: str
    last_name: str
    photo_url: Optional[str] = None
    birth_date: date  # Used to calculate age
    
    # Dating app-specific information
    is_looking_for_group: bool = True # Status for matching with groups
    current_location: Optional[dict] = None # Will store location data (e.g., {'latitude': 0, 'longitude': 0})

    # Group and event relationship
    current_group_id: Optional[str] = None # The ID of the group the user is currently in
    events_attended: list[str] = [] # IDs of past events for future recommendations

    # This allows you to add extra data to the model if needed, but it's good practice
    # to define all fields explicitly for clarity.
    class Config:
        extra = "allow"
