import dataclasses

class BaseDataClass():
    def to_dict(self):
        return dataclasses.asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        print("---------------")
        print(data)
        print(type(data))
        print(cls, type(cls))
        return cls(**data)
    
    async def insert_one(self):
        model = self.__class__.MODEL
        await model.insert_one(self.to_dict())

    @classmethod
    def to_object(cls, data):
        return cls.from_dict(data)
