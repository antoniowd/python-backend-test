from pydantic import BaseModel, ConfigDict

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
    model_config = ConfigDict(from_attributes=True)

class ProfileUpdate(ProfileBase):
    id: int

class Profile(ProfileBase):
    id: int
