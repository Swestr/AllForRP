import json

# ENVIRONMENT FUNCTIONS
class Environment:
    env = {}
    def retrieveEnv(self):
        with open('confs/env.json') as json_file:
            self.env = json.load(json_file)

    # TOKEN
    def getToken(self):
        return self.env["TOKEN"]

    # CONSTANTS
    def getConstants(self, id):
        return self.env["constants"][id]

    # COMMANDS
    def getCommandsPrefix(self):
        return self.env["commands"]["commandPrefix"]

    def getGeneralAdminCommand(self, id):
        return self.env["commands"]["general"]["admin"][id]

    def getGeneralGameMasterCommand(self, id):
        return self.env["commands"]["general"]["gameMaster"][id]

    def getGeneralPlayerCommand(self, id):
        return self.env["commands"]["general"]["player"][id]

    def getGeneralCommonCommand(self, id):
        return self.env["commands"]["general"]["common"][id]


    # SERVER
    def getDoNotDeleteTextChannels(self):
        return self.env["server"]["textChannelsDoNotDelete"]

    def getDoNotDeleteCategories(self):
        return self.env["server"]["categoriesDoNotDelete"]

    def getDoNotDeleteRoles(self):
        return self.env["server"]["rolesDoNotDelete"]

    def getServerCategory(self, id):
        return self.env["server"]["categories"][id]

    def getServerRole(self, id):
        return self.env["server"]["roles"][id]

    def getServerTextChannel(self, id):
        return self.env["server"]["textChannels"][id]

    def getCharacterChannelName(self, id):
        return self.env["server"]["textChannels"]["character"][id]

    # CHARACTER SHEET
    def getCharacterSheetNumericFields(self):
        return self.env["characterSheet"]["numericFields"]
    
    def getCharacterSheetNumericField(self, id):
        for elm in self.env["characterSheet"]["numericFields"]:
            if elm["name"] == id:
                return elm
    
    def getCharacterSheetNumericFieldsInterval(self):
        return self.env["characterSheet"]["numericFieldsInterval"]
        
    def getCharacterSheetNumericFieldsDefaultValues(self):
        return self.env["characterSheet"]["numericFields"]

    # DICE BUTTONS
    def getDiceButtonsDefinition(self):
        return (self.env["diceButtons"]["diceInterval"], self.env["diceButtons"]["diceValues"])

    # ERROR MESSAGES 
    def getErrorMessage(self, id):
        return self.env["messages"]["error"][id]