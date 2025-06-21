
from pydantic import BaseModel

class AddCompany(BaseModel):
    name: str
    description: str
    phone_number: str
    email: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    subscription_status: bool = True