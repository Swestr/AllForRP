import re, random

def loadCharacterSheetTemplate():
    with open('confs/characterSheetTemplate', encoding="utf-8") as characterSheetTemplate:
        return characterSheetTemplate.read()

def loadEquipmentTemplate():
    with open('confs/equipmentsLine', encoding="utf-8") as equipmentsLine:
        return equipmentsLine.read()

def loadCompetencesTemplate():
    with open('confs/competencesLine', encoding="utf-8") as comptencesLine:
        return comptencesLine.read()

def getArguments(message):
    return message.split()[1:]

def getCommand(message):
    return message.split()[0]

def getDoNotDeleteRoles(env):
    role_names = []
    for role_id in env.getDoNotDeleteRoles():
        role_names.append(env.getServerRole(role_id))
    return role_names

def getDoNotDeleteTextChannels(env):
    textChannel_names = []
    for textChannel_id in env.getDoNotDeleteTextChannels():
        textChannel_names.append(env.getServerTextChannel(textChannel_id))
    return textChannel_names

def getDoNotDeleteCategories(env):
    category_names = []
    for category_id in env.getDoNotDeleteCategories():
        category_names.append(env.getServerCategory(category_id))
    return category_names

def checkRollDef(rollDef):
    pattern = re.compile("^[0-9]*(d|D)[0-9]+$")
    return pattern.search(rollDef) != None

def getRandomValue(diceVal):
    return random.randint(1, diceVal)

def getDiceRollResponse(rollDef):
    (diceCpt, diceVal) = re.split("d|D", rollDef)
    if (diceCpt == ""):
        diceCpt = 1
    return [str(getRandomValue(int(diceVal))) for x in range(int(diceCpt))]
    