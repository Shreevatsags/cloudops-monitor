from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    name: str
    repository_url: str


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    name: str
    repository_url: str
    docker_image: str | None = None
    status: str

    class Config:
        from_attributes = True