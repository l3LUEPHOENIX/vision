# Data models for Heimdall to validate and manipulate API data.
from pydantic import BaseModel, model_validator
from typing_extensions import Literal

from config import *

class viewerApi(BaseModel):
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
        return self
        
class archiveApi(BaseModel):
    pass
