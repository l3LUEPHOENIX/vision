# Data models for Heimdall to validate and manipulate API data.
from pydantic import BaseModel, model_validator
from typing_extensions import Literal
import pymongo
import os

# Create a mongodb client
CLIENT = pymongo.MongoClient(os.environ['MONGODB_HOSTNAME'], 27017, username=os.environ['MONGODB_USERNAME'],password=os.environ['MONGODB_PASSWORD'])

# Get the Vision database from mongodb
DB = CLIENT["viewer_db"]
# Get/Create the sources collection in monogdb
VISION_VIEWER_SOURCES = DB["vision_viewer_sources"]

class viewerApi(BaseModel):
    version: int
    authentication: dict[Literal['apikey'], str]
    content: dict[Literal['message','containerId'], str]
    display_name: str = None
    post: dict = None
    channel: str = None

    @model_validator(mode='after')
    def valid_keys_and_containers (self):
        key = self.authentication['apikey']
        container = self.content['containerId']
        mongo_document = VISION_VIEWER_SOURCES.find_one({'apikey':key})
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
