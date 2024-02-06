from sanic_motor import BaseModel
import dataclasses
from models.base import BaseDataClass
from typing import Optional, List
import datetime as dt


class CompanyModel(BaseModel):
    __coll__ = 'company'
    __unique_fields__ = ['phone_no']


@dataclasses.dataclass
class Company(BaseDataClass):
    phone_no: str
    password: str
    created_at: Optional[dt.datetime]
    
    MODEL = CompanyModel
    
    @classmethod
    async def get_by_phone(cls, phone):
        res = await Company.MODEL.find_one({"phone_no": phone})
        if res is None:
            return None
        return Company.to_object(res)
    
    @classmethod
    def to_object(cls, data):
        c = Company(
            phone_no=data.phone_no,
            created_at=data.created_at,
            password=data.password
        )
        return c

    async def insert_one(self):
        from auth import hash_password
        self.password = hash_password(self.password)
        return await super().insert_one()
