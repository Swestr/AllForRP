import pymongo
from pymongo.message import update

class MongoConnection:
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    db = client.allForRP
    characterList = {}

    def updateCharacterList(self):
        self.characterList = list(self.db.characters.find())

    def getCharacters(self):
        if (self.characterList == {}):
            self.updateCharacterList()        
        return self.characterList

    def getCharacter(self, id):
        return list(filter(lambda character: character["_id"] == id, self.getCharacters()))[0]

    def removeCharacter(self, id):
        self.db.characters.delete_one({"_id": id})

    def removeAllCharacters(self):
        self.db.characters.remove({})

    def saveCharacter(self, characterDocument):
        data = self.db.characters.count_documents({"_id": characterDocument["_id"]})
        if (data == 0):
            self.db.characters.insert_one(characterDocument)
        
        self.db.characters.replace_one({"_id": characterDocument["_id"]}, characterDocument)
        self.updateCharacterList()
        
    def updateCharacter(self, id, values):
        self.db.characters.update_one({"_id": id}, {"$set": values})
        self.updateCharacterList()
        return self.getCharacter(id)

    def getDistinctCharacters(self):
        characterNames = list(self.db.characters.find({},{"_id":1}))
        return [key["_id"] for key in characterNames]
