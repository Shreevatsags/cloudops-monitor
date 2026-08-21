from pydantic import BaseModel, HttpUrl


class ApplicationCreate(BaseModel):
    name: str
    repository_url: HttpUrl