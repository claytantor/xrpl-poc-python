from pydantic import BaseModel

# ===== schemas
class MessageSchema(BaseModel):
    message: str

class ApiInfoSchema(BaseModel):
    version: str

