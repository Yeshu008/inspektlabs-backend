from pydantic import BaseModel, field_validator

class SignupSchema(BaseModel):
    username: str
    password: str

    @field_validator('username', 'password')
    @classmethod
    def validate_fields(cls, v: str, info) -> str:
        v = v.strip()
        if not v:
            raise ValueError(f"{info.field_name.capitalize()} cannot be blank")
        if info.field_name == 'username' and len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if info.field_name == 'password' and len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class LoginSchema(BaseModel):
    username: str
    password: str

    @field_validator('username', 'password')
    @classmethod
    def validate_fields(cls, v: str, info) -> str:
        v = v.strip()
        if not v:
            raise ValueError(f"{info.field_name.capitalize()} cannot be blank")
        return v
