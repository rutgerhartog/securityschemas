from pydantic import BaseModel, validator



class NetworkPort(BaseModel):
    port: int 
    @validator('port')
    def cap_check(cls, v):
        assert 0 <= v < 65536