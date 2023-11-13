# Data models for Heimdall to validate and manipulate API data.
from pydantic import BaseModel, model_validator
from typing_extensions import Literal

from config import *

class publisherApi_v1_0(BaseModel):
    version: int
    authentication: dict[Literal['apikey'], str]
    content: dict[Literal['message','containerId'], str]
    display_name: str = None
    post: dict = None
    channel: str = None

    @model_validator(mode='after')
    def valid_keys_and_containers (self):
        key = hashed_key(self.authentication['apikey'])
        container = self.content['containerId']
        mongo_document = VISION_VIEWER_SOURCES.find_one({'apikey_sum':key})
        if not mongo_document:
            raise ValueError("Invalid Key")
        
        if container not in mongo_document['containerIds']:
            raise ValueError('Invalid Container ID')
        
        self.display_name = mongo_document['displayname']
        self.channel = f"{self.display_name}:{container}"
        self.post = {
            'message': self.content['message'],
            'containerId': self.channel
        }
        return {'data': self.post, 'type': 'event', 'channel': self.channel}

class indexerApi_v1_0(BaseModel):
    version: int
    authentication: dict[Literal['apikey'], str]
    content: dict[Literal['action_type','file_name','file_size'], str]

    @model_validator(mode='after')
    def validate_key(self):
        key = hashed_key(self.authentication['apikey'])
        mongo_document = VISION_VIEWER_SOURCES.find_one({'apikey_sum':key})
        if not mongo_document:
            raise ValueError("Invalid Key")
        
        return {'authentication' : self.authentication['apikey'], 'content' : self.content}

class archivistApi_v1_0(BaseModel):
    pass
