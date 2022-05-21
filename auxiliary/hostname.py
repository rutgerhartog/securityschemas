from pydantic import BaseModel, validator
import re

class Hostname(BaseModel):
    name: str 
    tld: str 
    @validator('name')
    def check_hostname(cls, v):
        assert len(re.findall('[a-zA-Z0-9.]*', v)) == 2