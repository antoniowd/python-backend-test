from pydantic import BaseModel

class ProfileBase(BaseModel):
    img: str
    first_name: str
    last_name: str
    phone: str
    address: str
    city: str
    state: str
    zipcode: str
    available: bool = True

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    id: int

class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True
