from pydantic import BaseModel

class Original(BaseModel):
    original: str 


class Agent(BaseModel):
    build: Original