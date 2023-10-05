# Data models for Heimdall to validate and manipulate API data.

class publisher:
    def __init__(self, incoming_data, db):
        self.incoming_data = incoming_data
        self.db = db
        self.post = {}
        self.channel = ''

    def validPost(self, minimum_version) -> tuple:
        if isinstance(self.incoming_data, dict):
            try:
                version = self.incoming_data["version"]
                authentication = self.incoming_data["authentication"]
                content = self.incoming_data["content"]
            except:
                return (False, "Fields Unsatisfied")
        else:
            return (False, f"Wrong Data Type")
        
        if int(version) < minimum_version:
            return (False, "Version too old")
        
        try:
            if authentication["apikey"]:
                for i, dic in enumerate(self.db):
                    if dic["apikey"] == authentication["apikey"]:
                        provided_key = self.db[i]
                try:
                    provided_key
                except:
                    return (False, "Bad Key")
        except:
            return (False, "No Key Provided")

        try:
            message = content["message"]
            containerId = content["containerId"]
            containers = provided_key["containerIds"]
            
            if containerId not in containers:
                return (False, "Bad ContainerId")
            
        except:
            return (False, "Content fields unsatisified")
        
        self.post = {
            'message': message,
            'containerId': f"{provided_key['displayname']}:{containerId}"
        }

        self.channel = f"{provided_key['displayname']}:{containerId}"

        return (True, f"\nSuccessful POST to: {content['containerId']}\n\n")
    
    def createSource(self):
        pass

    def updateSource(self):
        pass

    def deleteSource(self):
        pass

class archivistPost:
    def __init__(self):
        pass

