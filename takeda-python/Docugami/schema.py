from pydantic import BaseModel

from typing import Optional

class IdResponse(BaseModel):
    id: str
    url: str

class ArtifactReference(BaseModel):
    id: str
    url: str
    name: str
    version: int
    document: Optional[IdResponse]

class TransformRequest(BaseModel):
    artifact: ArtifactReference
    accessToken: str
