# Data models for Heimdall to validate and manipulate API data.
import pymongo

class publisherPost:
    def __init__(self, incoming_data, db):
        self.incoming_data = incoming_data
        self.db = db

        if self.authentication["apikey"]:
            self.db.find_one()

        def valid(self) -> bool:
            try:
                self.version = self.incoming_data["version"]
                self.authentication = self.incoming_data["authentication"]
                self.content = self.incoming_data["content"]
            except:
                return False
            
            return True

        # if not isinstance(self.incoming_data, dict):
        #     raise TypeError(f"Expected dict, not {type(self.incoming_data)}")
        
        # if not isinstance(self.db, collection):
        #     raise TypeError(f"Expected MongoDB Collection, not {type(self.db)}")

class archivistPost:
    def __init__(self):
        pass

