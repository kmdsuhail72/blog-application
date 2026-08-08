from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

    model_config = {
        "extra": "ignore",
    }


class VerifyEmailRequest(BaseModel):
    token: str
