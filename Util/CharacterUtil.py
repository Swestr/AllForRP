from . import Util, DiscordUtil

async def updateCharacterSheet(guild, character, env):
    await updateCharacterSheetChannel(guild, character)
    await updateCharacterStatisticsChannel(guild, character, env)

async def updateCharacterSheetChannel(guild, character):
    characterMessage = await DiscordUtil.getMessage(guild, character["sheetChannelId"], character["sheetMessageId"])
    characterSheetTemplate = Util.loadCharacterSheetTemplate()
    equipmentTemplate, competencesTemplate = Util.loadEquipmentTemplate(), Util.loadCompetencesTemplate()
    characterEquipment, characterCompetences = character["equipments"], character["competences"]
    equipments, competences  = "", ""
    if (len(characterEquipment) != 0):
        equipments = "\n".join([equipmentTemplate.format(equipment) for equipment in characterEquipment])
    if (len(characterCompetences) != 0):
        competences = "\n".join([competencesTemplate.format(competence) for competence in characterCompetences])

    magicResistance = int((character["strength"]["value"] + character["intelligence"]["value"] + character["bravery"]["value"]) / 3)
    await characterMessage.edit(
        content=characterSheetTemplate.format(character, equipments, competences, magicResistance)
    )

async def updateCharacterStatisticsChannel(guild, character, env):
    characterSheetNumericFields = env.getCharacterSheetNumericFields()
    for keyElm in characterSheetNumericFields:
        key = keyElm["name"]
        value = keyElm["label"] + " : " + str(character[key]["value"])
        maxValue = keyElm["label"] + " : " + str(character[key]["maxValue"])
        statsValueMessage = await DiscordUtil.getMessage(guild, character["statsChannelId"], character[key]["valueMessageId"])
        await statsValueMessage.edit(content=value)
        if (character[key]["hasMax"]):
            statsMaxValueMessage = await DiscordUtil.getMessage(guild, character["statsChannelId"], character[key]["maxMessageId"])
            await statsMaxValueMessage.edit(content="**__MAX__** " + maxValue)

async def updateOneCharacterStatisticValue(guild, character, key, env):
    messageId = character[key]["valueMessageId"]
    channelId = character["statsChannelId"]
    message = await DiscordUtil.getMessage(guild, channelId, messageId)

    statLabel, statNewValue = env.getCharacterSheetNumericField(key)["label"], character[key]["value"]
    await message.edit(content=statLabel + " : " + str(statNewValue))
