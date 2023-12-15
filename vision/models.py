# Data models for Heimdall to validate and manipulate API data.
from pydantic import BaseModel, model_validator
from typing_extensions import Literal

from config import *


class publisherApi_v1_0(BaseModel):
    version: int
    authentication: dict[Literal["apikey"], str]
    content: dict[Literal["message", "containerId"], str]
    post: dict = None
    channel: str = None

    @model_validator(mode="after")
    def validate_keys_and_containers(self):
        container = self.content["containerId"]
        mongo_document = mongo_document_validator(self.authentication["apikey"])
        if not mongo_document.valid_key():
            raise ValueError("Invalid Key")

        if container not in mongo_document.document["containerIds"]:
            raise ValueError("Invalid Container ID")

        self.channel = f"{mongo_document.document['displayname']}:{container}"
        self.post = {"message": self.content["message"], "containerId": self.channel}
        del mongo_document
        return {"data": self.post, "type": "event", "channel": self.channel}


class indexerApi_v1_0(BaseModel):
    version: int
    authentication: dict[Literal["apikey"], str]
    content: dict[Literal["action_type", "file_name", "file_size"], str]

    @model_validator(mode="after")
    def validate_key(self):
        mongo_document = mongo_document_validator(self.authentication["apikey"])
        if not mongo_document.valid_key():
            raise ValueError("Invalid Key")

        return {
            "authentication": self.authentication["apikey"],
            "content": self.content,
        }


class archivistApi_v1_0(BaseModel):
    authentication: dict[Literal["apikey"], str]
    content: dict[Literal["message", "containerId"], str]
    channel: str = None
    post: dict = None

    @model_validator(mode="after")
    def validate_key(self):
        mongo_document = mongo_document_validator(self.authentication["apikey"])
        if not mongo_document.valid_key():
            raise ValueError("Invalid Key")

        self.channel = f"{mongo_document.document['displayname']}:archivist"
        self.post = {"message": self.content["message"], "containerId": self.channel}
        del mongo_document
        return {"data": self.post, "type": "event", "channel": self.channel}
