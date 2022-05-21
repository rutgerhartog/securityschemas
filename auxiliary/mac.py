from pydantic import BaseModel, validator 
import re 
import httpx 

class MACAddress(BaseModel):
    addr: str 
    oui: str = None
    @validator('addr')
    def hex_parts(cls, v):
        parts = re.split('-|:', v)
        assert len(parts) == 6 
        assert parts == re.findall(r'[a-f0-9][a-f0-9]', v)

    def __init__(self):
        parts = re.split('-|:', self.addr)
        self.oui = '-'.join(parts[:3])
        self.addr = '-'.join(parts)

    def resolve_oui(self):
        response = httpx.get(f"https://www.macvendorlookup.com/api/v2/{self.oui}").json()
        self.company = response.company        